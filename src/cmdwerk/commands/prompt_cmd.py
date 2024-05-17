"""
This module contains implementations for guided prompt from your history.
"""

import os
import shlex
import itertools
import unicodedata
import string
from collections import defaultdict
from typing import List, Tuple
import pickle
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import Completer, Completion
import pyperclip as paper
from .. import PROGRAM_CFG_DIR
from ..commands.libs.gen_utils import safe_make_dir


HISTORY_DATA_FILE = 'history.bin'
KEY_SEPARATOR = '|_|'
DEBUG = False


def build_cmd_key(parts):
    """Concatenate command parts to make a string key."""
    return KEY_SEPARATOR.join(parts)


def load_history_files_data(file_name: str) -> Tuple[List[str], int]:
    """
    Reads the history file, extracts the command line and returns them as a string list.
    :return: List of commands in history files.
    """
    def extract_command(a_line: str) -> str:
        parts = a_line.split(';')
        return ';'.join(parts[1:])

    lines = []
    loading_errors = 0
    with open(file_name, 'rb') as f:
        it = iter(f)
        for line in it:
            try:
                full_line = line.decode()
                while full_line.strip()[-1] == '\\':
                    next_chunk = next(it).decode(errors="ignore")
                    full_line += next_chunk
                lines.append(extract_command(full_line.strip()))
            except UnicodeDecodeError:
                # Error parsing one line skipping
                loading_errors += 1
    return lines, loading_errors


def build_history_data(cmd_list):
    """
    Builds dictionary with candidate completion at each stage from command list.
    """

    def remove_control_chars(a_string: str) -> str:

        # return filter(string.printable.__contains__, a_string)
        return "".join(ch for ch in a_string if unicodedata.category(ch)[0] != "C")

    results = defaultdict(set)
    for cmd in cmd_list:
        try:
            raw_parts = shlex.split(cmd)
        except ValueError:
            raw_parts = None
        if not raw_parts:
            continue
        # Ignore commands after a pipe
        parts = [remove_control_chars(x) for x in (itertools.takewhile(lambda x: x != '|', raw_parts))]
        parts = [x for x in parts if x]
        done_keys = [parts[0]]
        for idx1 in range(1, len(parts)):
            new_key = build_cmd_key(done_keys)
            results[new_key].add(parts[idx1])
            done_keys.append(parts[idx1])
    return results


def bottom_toolbar():
    """Python prompt toolkit bottom toolbar definition."""
    return [("class:bottom-toolbar", "Type 'q' to exit")]


# pylint: disable=too-few-public-methods
class CustomHistoryCompleter(Completer):
    """Custom completion class that completes from history data"""
    def __init__(self, completion_dict):
        self.completion_dict = completion_dict
        self.first_completion_dict = self._build_first_completion_dict()
        super().__init__()

    def _build_first_completion_dict(self):
        """Build first completion using substrings ."""
        first_cmds = {x.split(KEY_SEPARATOR)[0] for x in self.completion_dict}
        result = defaultdict(set)
        for cmd in first_cmds:
            for idx in range(len(cmd)):
                token = cmd[:idx+1]
                if token not in first_cmds:
                    result[token].add(cmd)
        return result

    def get_completions(self, document, _):
        """Yield the possible completions for the current text."""
        word = document.get_word_before_cursor()
        text_so_far = document.text
        parts = shlex.split(text_so_far)
        curr_key = build_cmd_key(parts)
        # If there is only one token string and the current token does not have
        # candidates then treat as simple word completion case.
        if len(parts) == 1 and curr_key not in self.completion_dict:
            # Single token command case.
            if curr_key in self.first_completion_dict:
                candidates = self.first_completion_dict[curr_key]
                for candidate in candidates:
                    yield Completion(candidate, start_position=-len(word))
        else:
            # Multiple token commands case.
            if curr_key in self.completion_dict:
                candidates = self.completion_dict[curr_key]
                for candidate in candidates:
                    yield Completion(candidate, start_position=-len(word))


def prompt_history_from_data(history_data):
    """
    Create the completion prompt interaction based on the history data.
    """
    history_completer = CustomHistoryCompleter(history_data)
    session = PromptSession(
        auto_suggest=AutoSuggestFromHistory(),
        completer=history_completer,
        bottom_toolbar=bottom_toolbar,
        style=Style.from_dict({"bottom-toolbar": "#333333 bg:#3333AA"})
    )
    user_input = session.prompt(">")
    # Moves command to paperclip so users can do a Ctrl-V to paste into shell terminal.
    if not user_input:
        return
    paper.copy(user_input)
    print('\n(Ctrl-V) to paste the command in the shell')


def prompt_history(cmd_list: List[str]):
    """
    Create the completion prompt interaction from a list of commands.
    """
    history_data = build_history_data(cmd_list)
    prompt_history_from_data(history_data)


class PromptCommand:
    """Command line prompt command class."""

    @classmethod
    def sync_with_history(cls, history: str):
        """
        Reads the history file, creates dictionary with the command completion candidates and
        stores them into a history_data pickle file.
        """
        history_file_path = os.path.expanduser(history)
        safe_make_dir(PROGRAM_CFG_DIR)
        output_file = os.path.join(PROGRAM_CFG_DIR, HISTORY_DATA_FILE)
        history_lines, loading_errors = load_history_files_data(history_file_path)
        history_data = build_history_data(history_lines)
        with open(output_file, 'wb') as history_fh:
            pickle.dump(history_data, history_fh)
        print(f'Saved history data to {output_file}')
        print(f'History lines : {len(history_lines)}')
        print(f'Loading errors: {loading_errors}')

    @classmethod
    def run(cls):
        """
        Reads history candidates from the history_data pickle file and
        creates the completion prompt interaction.
        """
        history_data_file = os.path.join(PROGRAM_CFG_DIR, HISTORY_DATA_FILE)
        try:
            with open(history_data_file, 'rb') as history_fh:
                history_data = pickle.load(history_fh)
        except FileNotFoundError as _:
            print('ERROR: History file not found.')
            print(' - To create it, use the command: cmdw ppt sync ')
            return
        if DEBUG:
            for key in sorted(history_data.keys()):
                value = history_data[key]
                print(key, value)
        prompt_history_from_data(history_data)
