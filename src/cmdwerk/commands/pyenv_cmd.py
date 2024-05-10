
import subprocess
from .libs.gen_utils import YELLOW, CYAN, RED, ScreenPos
from .libs.gen_utils import write_screen_cols as write_screen

class PyEnvHelperCommands:
    """PyEnv helper commands available:
        - List python versions available in a compact format.
    """

    @classmethod
    def get_list_python_versions(cls):
        """Collects the official python versions available."""
        cmd = ["pyenv", "install", "-l"]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        payload = res.stdout
        if res.returncode != 0:
            print('Failed to get pyenv versions')
            return None
        temp = []
        for line in payload.split('\n'):
            line = line.strip()
            if 'Available versions:' in line:
                continue
            temp.append(line)
        result = []
        min_python_minor_version = 7
        for line in reversed(temp):
            if not line.startswith('3.'):
                continue
            sub_version_str = line.split('.')[1]
            sub_version = int(sub_version_str) if sub_version_str.isdigit() else 0
            if min_python_minor_version <= sub_version and '-dev' not in line:
                result.append(line)
        return result


    @classmethod
    def list_formatted(cls):
        cmd = cls()
        version_list = cmd.get_list_python_versions()
        last_major = None
        last_minor = None
        print(' ')
        write_screen('-- Pyenv python versions --', YELLOW)
        print(' ')
        for v in version_list:
            (major, minor, release) = v.split('.')
            version_fmt = f'{v:<9}'
            if major is not None and (major == last_major and minor == last_minor):
                print(version_fmt, end='')
            else:
                print(f'\n[{major}.{minor:<2}] ➜ {version_fmt}', end='')
            last_major = major
            last_minor = minor
        print('\n\n')




