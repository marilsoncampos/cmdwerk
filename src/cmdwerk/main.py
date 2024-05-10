import click
from .commands.pyenv_cmd import PyEnvHelperCommands
from .commands.scripts_cmd import ScriptsCommands

@click.group()
def main():
    pass

@main.command()
def pyenv_list():
    PyEnvHelperCommands.list_formatted()

@main.command()
@click.option('--group', default='')
def bins(group: str):
    if group == '':
        ScriptsCommands.cmd_bin_list()
    else:
        ScriptsCommands.cmd_bin_group(group)


