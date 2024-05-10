"""
Commands to organize and document your own scripts
Note: scrips need to be located inside the '~/bin' directory.
"""

import os
from collections import defaultdict, OrderedDict
from dataclasses import dataclass
from .libs.gen_utils import write_screen_cols as write_screen
from .libs.gen_utils import msg_and_exit
from .libs.gen_utils import BLUE, CYAN, RED, ScreenPos
from .libs.gen_utils import SCRIPT_PADDING, MAX_DESC, NUMBER_OF_COLS


LOCAL_VAR_PREFIX = 'CMDW_'
HERE_FILE_MARKER = 'CMDW_DOC_MARKER'



@dataclass
class ScriptRecord:
    """Helper class to store script."""
    name: str
    short_hlp: str
    long_hlp: str


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
        self.script_files = None
        self.script_dir = os.path.expanduser('~/bin')
        self.global_vars = OrderedDict()


    @classmethod
    def update_variable_values(cls, var_dict, line):
        """Update variable values in the dictionary"""
        line = line.strip().replace('\'', '')
        parts = line.split('=')
        if len(parts) == 2:
            var_name, var_value = parts
            var_dict[var_name.strip()] = var_value.strip()


    def load_script_info(self, script_name):
        """Extracts the description and group"""

        def clean_line(line_str: str) -> str:
            temp = line_str.strip('\n').replace('\'', '')
            if temp and temp[0] == '#':
                temp = temp[1:]
            return temp

        # pylint: disable=too-many-locals
        variables = dict()
        variables.update(self.global_vars)
        # -- State machine states --
        st_inside_code = 'code'
        st_short_hlp = 's_doc'
        st_long_hlp = 'l_doc'
        state = st_inside_code
        if script_name.startswith('.'):
            return None, None
        short_hlp = None
        long_hlp_lst = []
        with (open(os.path.join(self.script_dir, script_name), 'r',
                  encoding="utf-8") as in_file):
            for raw_line in in_file:
                line = clean_line(raw_line)
                if state == st_inside_code:
                    if line.startswith(LOCAL_VAR_PREFIX):
                        self.update_variable_values(variables, raw_line)
                    elif line.endswith(HERE_FILE_MARKER):
                        state = st_short_hlp
                elif state == st_long_hlp:
                    if line.endswith(HERE_FILE_MARKER):
                        break
                    long_hlp_lst.append(line)
                else:
                    short_hlp = line
                    state = st_long_hlp
        if not short_hlp:
            return None, None
        long_hlp = '\n'.join(long_hlp_lst)
        for v_name, v_value in variables.items():
            token = '${{{0}}}'.format(v_name)
            short_hlp = short_hlp.replace(token, v_value)
            long_hlp = long_hlp.replace(token, v_value)
        group_name = variables.get('CMDW_GROUP_NAME', 'No group')
        entry = ScriptRecord(
            name=script_name, short_hlp=short_hlp, long_hlp=long_hlp)
        return group_name, entry

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

        self.script_groups = dict()
        self.script_files = [
            f for f in os.listdir(self.script_dir)
            if os.path.isfile(os.path.join(self.script_dir, f))]
        for script_file in self.script_files:
            grp_name, entry = self.load_script_info(script_file)
            if grp_name:
                add_script_to_group(grp_name, entry)

    def list_short_help(self, filter_str=None):
        """List all groups and the scripts belonging to the group."""

        def emit_script_entry(entry_record):
            script_name = entry_record.name.rjust(SCRIPT_PADDING)
            short_hlp = entry_record.short_hlp
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
            write_screen("{0}".format(key), RED, ScreenPos.CENTERED)
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
            short_hlp = entry_record.short_hlp
            filer_str = ' ' * len(script_name)
            long_hlp_lst = entry_record.long_hlp.split('\n')
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
            msg_and_exit('Group "{0}" not found'.format(group_name))
        write_screen("{0}".format(group_name), RED, pos=ScreenPos.SEPARATOR)
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


class ScriptsCommands:

    @classmethod
    def cmd_bin_group(cls, group_name):
        manager = ScriptManager()
        manager.list_long_help(group_name)

    @classmethod
    def cmd_bin_list(cls):
        manager = ScriptManager()
        manager.list_short_help()
