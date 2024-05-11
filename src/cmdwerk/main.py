import click
from .commands.pyenv_cmd import PyEnvHelperCommands
from .commands.scripts_cmd import ScriptsCommands
from . import __version__ as app_version

EPILOG = f'CmdWerk {app_version}'
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

class CustomHelpGroup(click.Group):
    def format_help(self, ctx, formatter):
        parent = ctx.parent
        help_text = ['Greetings! Options:']
        for param in parent.command.get_params(ctx):
            help_text.append(' '.join(param.get_help_record(parent)))
        help_text.append("\n" + ctx.get_usage() + "\n")
        help_text.append('Commands:\n')
        help_text.extend([f'{command_name}' for command_name, command in admin.commands.items()])
        formatter.write('\n'.join(help_text))


@click.version_option(app_version,"--version", "-v")
@click.group(epilog=EPILOG, context_settings=CONTEXT_SETTINGS)
def main():
    pass


# @main.group(cls=CustomHelpGroup)
@main.command(epilog=EPILOG)
def pyenv_list():
    PyEnvHelperCommands.list_formatted()

@main.command(epilog=EPILOG)
@click.argument('sub-cmd', type=click.Choice(['status', 'docs']))
@click.option('--group', default='', metavar='<group_name>', show_default=True,)
def bins(sub_cmd: str, group: str):
    if sub_cmd == 'status':
        ScriptsCommands.cmd_report_bin_registrations()
        return 0
    # default argument makes it to list script help
    if group == '':
        ScriptsCommands.cmd_bin_list()
    else:
        ScriptsCommands.cmd_bin_group(group)



