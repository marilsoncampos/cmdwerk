"""
This module contains implementations script reporting related commands.

Note: scrips need to be located inside the '~/bin' directory.
"""

import os
from collections import defaultdict, OrderedDict
from dataclasses import dataclass
from .libs.gen_utils import write_screen_cols as write_screen
from .libs.gen_utils import msg_and_exit
from .libs.gen_utils import BLUE, YELLOW, CYAN, RED, ScreenPos
from .libs.gen_utils import SCRIPT_PADDING, MAX_DESC, NUMBER_OF_COLS

# Document marker Tokens
CMDW_GROUP_TOKEN = 'CMDW_GROUP_NAME'
CMDW_HELP_BEGIN = 'CMDW_HELP_BEGIN'
CMDW_HELP_END = 'CMDW_HELP_END'


@dataclass
class ScriptRecord:
    """Helper class to store script information."""
    name: str
    short_help: str
    long_help: str


class ColumnPrinter:
    """helper class to print elements in columns."""

    @staticmethod
    def build_empty_cols(num_columns):
        """Creates an array with empty columns."""
        return [None for _ in range(num_columns)]

    def __init__(self, num_columns):
        """Initializes the number of columns and the column cache."""
        self._num_columns = num_columns
        self._column_objs = ColumnPrinter.build_empty_cols(num_columns)

    def is_full(self):
        """Returns true if there is data for all the columns."""
        return all(self._column_objs)

    def is_not_empty(self):
        """Returns true if still there is space for column data."""
        return any(self._column_objs)

    def reset(self):
        """
        Resets the object and allows starting with different
        number of columns.
        """
        self._column_objs = ColumnPrinter.build_empty_cols(self._num_columns)

    def add_column_data(self, new_obj):
        """
        Stores column data in the next available slot.
        Returns 'False' if none available.
        """
        if self.is_full():
            return False
        for idx, slot in enumerate(self._column_objs):
            if slot:
                continue
            self._column_objs[idx] = new_obj
            return True

    def map(self, call_func):
        """Calls function to each column object in the cache."""
        for col_obj in self._column_objs:
            if col_obj:
                call_func(col_obj)


class ScriptManager:
    """
    Class that reads the scripts from the bin directory and
    listing of scripts with various formats.
    """

    def __init__(self):
        """Initializes, set empty buffers, etc."""
        self.groups = defaultdict(list)
        self.buffer = []
        self.script_groups = None
        self.misconfigured_scripts = []
        self.script_files = None
        self.script_dir = os.path.expanduser('~/bin')
        self.global_vars = OrderedDict()

    def load_script_info(self, script_name):
        """Extracts the description and group"""

        def clean_line(line_str: str) -> str:
            temp = line_str.strip('\n').replace('\'', '')
            if temp and temp[0] == '#':
                temp = temp[1:].strip()
            return temp

        # pylint: disable=too-many-locals
        # -- State machine states --
        st_outside_help = 'out_help'
        st_inside_help = 'in_help'
        state = st_outside_help
        script_full_path = os.path.join(self.script_dir, script_name)
        help_lines = []
        group_name = 'No group'
        
        try:
            with open(script_full_path, 'r', encoding="utf-8") as in_file:
                for raw_line in in_file:
                    line = clean_line(raw_line)
                    if state == st_outside_help:
                        if line.startswith(CMDW_GROUP_TOKEN):
                            parts = line.split('=')
                            if len(parts) == 2:
                                group_name = parts[1]
                        elif line.startswith(CMDW_HELP_BEGIN):
                            state = st_inside_help
                    else:  # Case for state == st_inside_help:
                        if line.startswith(CMDW_HELP_END):
                            break
                        help_lines.append(line)
        except UnicodeDecodeError:
            # Skip binary files or files with encoding issues
            return None, None

        short_hlp = help_lines[0] if help_lines else ''
        if short_hlp:
            entry = ScriptRecord(
                name=script_name, short_help=short_hlp, long_help='\n'.join(help_lines[1:]))
            return group_name, entry
        return None, None

    def load_scripts_groups(self):
        """Loads scripts into groups."""

        def add_script_to_group(the_group, script_entry):
            """Adds script to a group."""
            if the_group in self.script_groups:
                temp = self.script_groups[the_group]
            else:
                temp = []
            temp.append(script_entry)
            self.script_groups[the_group] = temp

        self.script_groups = {}
        self.script_files = [
            f for f in os.listdir(self.script_dir)
            if os.path.isfile(os.path.join(self.script_dir, f))]
        self.script_files = filter(lambda x: not x.startswith('.'), self.script_files)
        for script_file in self.script_files:
            grp_name, entry = self.load_script_info(script_file)
            if grp_name:
                add_script_to_group(grp_name, entry)
            if not entry and not grp_name:
                self.misconfigured_scripts.append(script_file)

    def list_short_help(self, filter_str=None):
        """List all groups and the scripts belonging to the group."""

        def emit_script_entry(entry_record):
            script_name = entry_record.name.rjust(SCRIPT_PADDING)
            short_hlp = entry_record.short_help
            short_hlp = short_hlp.ljust(MAX_DESC)
            if len(short_hlp) > MAX_DESC:
                short_hlp = short_hlp[:MAX_DESC-3] + '...'
            else:
                short_hlp = short_hlp[:MAX_DESC]
            write_screen(script_name, BLUE)
            write_screen('  ' + short_hlp, CYAN)

        self.load_scripts_groups()
        sorted_keys = sorted(self.script_groups.keys())
        columns = ColumnPrinter(NUMBER_OF_COLS)
        for key in sorted_keys:
            if (filter_str is not None) and (filter_str not in key):
                continue
            write_screen(f"{key}", RED, ScreenPos.CENTERED)
            sorted_scripts = sorted(
                self.script_groups[key], key=lambda ent: ent.name)
            columns.reset()
            for a_script in sorted_scripts:
                if columns.is_full():
                    columns.map(emit_script_entry)
                    write_screen('\n')
                    columns.reset()
                columns.add_column_data(a_script)
            if columns.is_not_empty():
                columns.map(emit_script_entry)
                write_screen('\n')
            write_screen('\n')

    def list_long_help(self, group_name):
        """List all groups with a long help text."""

        def emit_script_entry(entry_record):
            script_name = entry_record.name.rjust(SCRIPT_PADDING) + '  '
            short_hlp = entry_record.short_help
            filer_str = ' ' * len(script_name)
            long_hlp_lst = entry_record.long_help.split('\n')
            write_screen(script_name, BLUE)
            write_screen(short_hlp + '\n', CYAN)
            for line in long_hlp_lst:
                write_screen(filer_str, CYAN)
                write_screen(line + '\n', CYAN)
            write_screen('\n')

        self.load_scripts_groups()
        columns = ColumnPrinter(1)
        group = self.script_groups.get(group_name, None)
        if not group:
            msg_and_exit(f'Group "{group_name}" not found')
        write_screen(f"{group_name}", RED, pos=ScreenPos.SEPARATOR)
        sorted_scripts = sorted(group, key=lambda ent: ent.name)
        columns.reset()
        for a_script in sorted_scripts:
            if columns.is_full():
                columns.map(emit_script_entry)
                columns.reset()
            columns.add_column_data(a_script)
        if columns.is_not_empty():
            columns.map(emit_script_entry)
        write_screen('\n')

    def report_script_registrations(self):
        """
        List the scripts reporting what group are they registered or if misconfigured.
        """
        self.load_scripts_groups()
        write_screen(' Registered scripts: \n', YELLOW)
        for group, scripts in sorted(self.script_groups.items(), key=lambda x: x[0]):
            for script in scripts:
                write_screen(f'   {script.name} (group:{group})\n', CYAN)
        write_screen('\n')
        write_screen(' Misconfigured scripts: \n', YELLOW)
        max_size = max(len(x) for x in self.misconfigured_scripts) + 2
        num_cols = 120 // max_size
        for idx, script in enumerate(self.misconfigured_scripts):
            fmt_script = script.ljust(max_size)
            write_screen(f'  {fmt_script}', RED)
            if (idx+1) % num_cols == 0:
                write_screen('\n')
        write_screen('\n\n')


class ScriptsCommands:
    """Command service for script management."""
    @classmethod
    def cmd_bin_group(cls, group_name):
        """List the scripts belonging to the group."""
        manager = ScriptManager()
        manager.list_long_help(group_name)

    @classmethod
    def cmd_bin_list(cls):
        """List all the scripts."""
        manager = ScriptManager()
        manager.list_short_help()

    @classmethod
    def cmd_report_bin_registrations(cls):
        """Report scripts registration status."""
        manager = ScriptManager()
        manager.report_script_registrations()
