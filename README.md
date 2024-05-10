
CmdWerk: A minimalist command-line tool to organize your scripts




### CMD Werk


#### 1. Introduction

CmdWerk is a minimalist tool to help manage your personal scripts.
It has capabilities to extend with the modules. As an example we
include a module to emit a compact pyenv version report.

Your shell scripts should be stored in your $HOME/bin.
Using CmdWerk you can organize them as groups.


#### 2. Getting Started

Use this command to package the project and install the newly built package in pipx with this command.

```console
$ ./reinstall.sh
```

Here are the commands included in the reinstall.sh

```bash
#!/bin/bash
make
pipx uninstall cmdwerk
pipx install dist/cmdwerk-0.1.0.tar.gz
```

You can get command help using this command.

```console
$ cmdw --help
```

#### 3. Adapting bash scripts to appear on reports


As an example, here is a small bash script without the config.

```bash
#!/bin/bash
vi ~/.ssh/config
```

And here is the same script documented.

```bash
#!/bin/bash

CMDW_GROUP_NAME='ssh'
DOC_STR=$(cat <<CMDW_DOC_MARKER
Edits ssh config file..

CMDW_DOC_MARKER
)

vi ~/.ssh/config
```

#### 4. Adapting python scripts to appear in reports


Here is the original python script code.

```python
#!/usr/bin/env python3
"""
A simple python password generator script configured for cmdwerk
"""

import random
import string

def generate_password(pass_length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(pass_length))

password = generate_password(15)
print(f' Your new password is: {password}')
```

Here is the modified code.

```python
#!/usr/bin/env python3
"""
A simple python password generator script configured for cmdwerk
"""

import random
import string

CMDW_GROUP_NAME='tools'
# CMDW_DOC_MARKER
# Generates passwords example.
# CMDW_DOC_MARKER


def generate_password(pass_length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(pass_length))


password = generate_password(15)
print(f' Your new password is: {password}')
```


#### 5. Commands to list scripts

##### 5.1. List the scripts with short details

```bash
$ cmdw bins
```

will produce the following results

![bins report](https://raw.githubusercontent.com/marilsoncampos/cmdwerk/master/docs/source/_static/list_all.png)


5.2. List the scripts of a group with long details

```bash
$ cmdw bins --group git
```

will produce the following results

![bins group report](https://raw.githubusercontent.com/marilsoncampos/cmdwerk/master/docs/source/_static/list_group.png)


#### 6. Commands to report on pyenv

##### 6.1. Commands to list scripts

The list will include only the official python versions
from version 3.7 or later.

```bash
$ cmdw pyenv-list
```

will produce the following results

.. image:: _static/pyenv_list.png
   :align: center


### Installation

We recommend using Python 3.11 or above.
To install use:

```console
$ pipx install cmd
```


### Usage

Check the command line help using:

```console
$ cmdw --help
```

Here is a list of commands.

```console
╒════════════════════════════════════════════════════════════════════════════════════╕
│ Command             │ Description                                                  │
╞═════════════════════╪══════════════════════════════════════════════════════════════╡
│ cmd --help          │ Print command line help for top commands                     │
├─────────────────────┼──────────────────────────────────────────────────────────────┤
│ cmdw bins --help    │ Print command line help for the 'bin' command                │
├─────────────────────┼──────────────────────────────────────────────────────────────┤
│                     │                                                              │
╘═════════════════════╧══════════════════════════════════════════════════════════════╛
```


# Credits

- Marilson Campos (marilson.campos@gmail.com)

