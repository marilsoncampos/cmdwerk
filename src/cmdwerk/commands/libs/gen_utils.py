"""
Helper functions for the python scripts.
"""

import os
import sys
import subprocess
from enum import Enum


# Color constants for screen print.
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
# Screen Formatting.
MAX_STR_SCREEN = 100
# Screen Formatting for multi-column writes.
NUMBER_OF_COLS = 3
SCRIPT_PADDING = 12
MAX_DESC = 35
MIDDLE_SPACER = '  |  '


class ScreenPos(Enum):
    """Screen position constants"""
    PLAIN = 1
    CENTERED = 2
    SEPARATOR = 3


def has_colors(stream):
    """Detects if output supports colors."""
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False  # auto color only on TTYs
    try:
        # pylint: disable=import-outside-toplevel
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except IOError:
        # guess false in case of error.
        return False


# Sets the flag that decides if we are outputting colors.
HAS_COLORS = has_colors(sys.stdout)


def write_error(error_msg):
    """Writes an error message"""
    write_screen(f" ERROR: {error_msg}\n")


def msg_and_exit(msg, stderr=None):
    """Prints a message and exits the program with error code"""
    sys.stdout.write(f' ERROR: {msg}\n')
    if stderr:
        for line in stderr:
            sys.stdout.write(f'{line}\n')
    sys.stdout.flush()
    sys.exit(-1)


def yes_no(bool_value):
    """Returns 'Yes' if true and 'No' otherwise."""
    return 'Yes' if bool_value else 'No'


def encode_msg(msg_str, color):
    """Encode String with color"""
    # pylint: disable=consider-using-f-string
    return "\x1b[1;%dm" % (30 + color) + msg_str + "\x1b[0m"


def write_screen(text, color=WHITE, pos=ScreenPos.PLAIN, skip_line=False):
    """Print text with color."""
    if pos == ScreenPos.SEPARATOR:
        msg = ' ' + text + ' '
        spacer_size = (MAX_STR_SCREEN - len(msg)) // 4
        side_spacer = spacer_size * '. '
        msg = ' ' + side_spacer + msg + side_spacer[::-1] + '\n'
    elif pos == ScreenPos.CENTERED:
        msg = text   # To be implemented later.
    else:
        msg = text
    if skip_line:
        msg = '\n' + msg
    if HAS_COLORS:
        # seq = f"\x1b[1;%{30 + color}m{msg}\x1b[0m"
        # seq = "\x1b[1;%dm" % (30 + color) + msg + "\x1b[0m"
        sys.stdout.write(encode_msg(msg, color))
    else:
        sys.stdout.write(msg)


def write_screen_cols(
        text, color=WHITE, pos=ScreenPos.PLAIN, num_cols=NUMBER_OF_COLS):
    """Print text with color."""
    if pos == ScreenPos.CENTERED:
        char_per_line = num_cols * (SCRIPT_PADDING + MAX_DESC + 3)
        msg_str = ' ' + text.strip('\n') + ' '
        side_spacer = ((char_per_line - 2 * len(msg_str)) // 4) * '. '
        temp = side_spacer + msg_str + side_spacer[::-1]
        offset = (char_per_line - len(temp)) // 2 - 1
        msg = (' ' * offset) + temp + '\n'
    elif pos == ScreenPos.SEPARATOR:
        side_spacer = 25 * '- '
        msg = ' ' + side_spacer + ' ' + text + ' ' + side_spacer[::-1] + '\n'
    else:
        msg = text
    if HAS_COLORS:
        # seq = f"\x1b[1;%{30 + color}m{msg}\x1b[0m"
        # sys.stdout.write(seq)
        # seq = "\x1b[1;%dm" % (30 + color) + msg + "\x1b[0m"
        sys.stdout.write(encode_msg(msg, color))
    else:
        sys.stdout.write(text)


# noinspection PyBroadException
def run_bash_command(cmd_list):
    """Runs a shell command and capture exit_code, stdout, stderr."""
    # pylint: disable=subprocess-run-check
    try:
        result = subprocess.run(cmd_list, capture_output=True, cwd=os.getcwd())
    except TypeError:
        return -1, '', ''
    stdout = result.stdout.decode("utf-8").split('\n')
    stderr = result.stderr.decode("utf-8").split('\n')
    ret_code = result.returncode
    return ret_code, stdout, stderr


def read_txt_file(file_name):
    """Loads the contents of file and returns it as a list of strings."""
    with open(file_name, 'r', encoding='UTF-8') as f_handle:
        lines = f_handle.readlines()
    return [x.strip('\n') for x in lines]


def safe_make_dir(dir_path: str):
    """Makes a directory if it does not exist."""
    expanded_dir_path = os.path.expanduser(dir_path)
    os.makedirs(expanded_dir_path, exist_ok=True)
