# pylint: disable=anomalous-backslash-in-string, too-few-public-methods
"""

 CmdWerk - A minimalist tool for developer productivity

"""
# pylint: enable=anomalous-backslash-in-string

import click
from .commands.pyenv_cmd import PyEnvHelperCommands
from .commands.bins_cmd import ScriptsCommands
from .commands.prompt_cmd import PromptCommand
from . import __version__ as app_version
from . import __title__ as app_title
from . import __description__ as app_description

PROGRAM_MSG = f'{app_title}, version {app_version},  {app_description}.'
EPILOG = f'{app_title} {app_version}'
CONTEXT_SETTINGS = {"help_option_names": ['-h', '--help']}


# class CustomHelpGroup(click.Group):
#     """A custom help group to show sub-command help"""
#     def format_help(self, ctx, formatter):
#         """Custom help formatter"""
#         parent = ctx.parent
#         help_text = ['X Options:']
#         for param in parent.command.get_params(ctx):
#             help_text.append(' '.join(param.get_help_record(parent)))
#         help_text.append("\n" + ctx.get_usage() + "\n")
#         help_text.append('Commands:\n')
#         help_text.extend([f'{command_name}' for command_name, command in self.commands.items()])
#         formatter.write('\n'.join(help_text))


@click.version_option(app_version, "--version", "-v", message=PROGRAM_MSG)
@click.group(epilog=EPILOG, context_settings=CONTEXT_SETTINGS)
def main():
    """The main command line interface group."""


# TODO: Try to expand sub-command help into main using: @main.group(cls=CustomHelpGroup)
@main.command(epilog=EPILOG)
def pyenv_list():
    """Shows compact PyEnv report with the official python versions"""
    PyEnvHelperCommands.list_python_versions()


@main.command(epilog=EPILOG)
@click.argument('sub-cmd', type=click.Choice(['docs', 'status'], case_sensitive=False),
                default='docs')
@click.option('--group', default='', metavar='<group_name>', show_default=True,)
def bins(sub_cmd: str, group: str):
    """Commands related to documenting your scripts.

        \b
        docs  : Show report listing scripts and help. (default)
        status: List the registered and not-registered scripts.
    """
    if sub_cmd == 'status':
        ScriptsCommands.cmd_report_bin_registrations()
        return
    # default argument makes it to list script help
    if group == '':
        ScriptsCommands.cmd_bin_list()
    else:
        ScriptsCommands.cmd_bin_group(group)


@main.command(epilog=EPILOG)
@click.argument('sub-cmd', type=click.Choice(['sync', 'run'], case_sensitive=False),
                default='run')
@click.option('--history', default='~/.zsh_history',
              metavar='<history_file>', show_default=True,)
def ppt(sub_cmd: str, history: str):
    """Interactive prompt completion related commands:

        \b
        sync: Update prompt data using zsh history.
        run : Enter interactive prompt. (default)
    """
    if sub_cmd == 'sync':
        PromptCommand.sync_with_history(history)
    else:
        PromptCommand.run()
