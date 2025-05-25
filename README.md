
CmdWerk: A minimalist command-line tool to organize your scripts


### CMD Werk

#### 1. Introduction

CmdWerk is a minimalist tool that helps you manage your scripts.
You can also extend it with new modules. 

As an example, we include two modules:
    1. An interactive prompt that learns from your command history.
    2. Pyenv report that shows a list of available versions 

It processes your shell scripts stored in your $HOME/bin.

With CmdWerk, you can effortlessly organize your scripts into groups, enhancing your workflow and making script management a breeze.

#### 2. Getting Started

To install it use this command to package the project and install the newly built package.

```console
$ ./reinstall.sh
```

**_NOTE:_**: We recommend installing it in pipx (https://github.com/pypa/pipx).

Here are the commands included in the 'reinstall.sh'

```bash
#!/bin/bash
uv venv --python=python3.11 .venv && 
source .venv/bin/activate && 
uv pip install -e .
```

You can get the make command help using this command.

```console
$ cmdw --help
```

#### 3. Adapting bash scripts to appear on reports


As an example, here is a small bash script without the config.

```bash
#!/bin/bash
vi ~/.ssh/config
```

And here is the same script that is ready to be registered by cmdw.

```bash
#!/bin/bash

# -- Cmd Werk Config --
# CMDW_GROUP_NAME='aws & ssh'
# CMDW_HELP_BEGIN
# Edits ssh config file.
# CMDW_HELP_END

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

# -- Cmd Werk Config --
# CMDW_GROUP_NAME='tools'
# CMDW_HELP_BEGIN
# Generates passwords example.
# CMDW_HELP_END


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


##### 5.2. List the scripts of a group with detailed descriptions

```bash
$ cmdw bins --group git
```

will produce the following results

![bins group report](https://raw.githubusercontent.com/marilsoncampos/cmdwerk/master/docs/source/_static/list_group.png)



##### 5.3. Report the status of script registrations

This report has two parts:
   a. List of registered scripts and the group its registered under.
   b. List the scripts not registered.

```bash
    $ cmdw bins status
```

will produce the following results


![bins report](https://raw.githubusercontent.com/marilsoncampos/cmdwerk/master/docs/source/_static/registeded_bins.png)

#### 6. Command to emit a Pyenv report

The list will include only the official Python versions
from version 3.7 or later.

```bash
$ cmdw pyenv-list
```

will produce the following results


![bins report](https://raw.githubusercontent.com/marilsoncampos/cmdwerk/master/docs/source/_static/pyenv_list.png)



#### 7. Commands for the interactive prompt

##### 7.1. Command to start the interactive prompt

```bash
    $ cmdw ppt
```

Start typying the command and use 'TAB' to navigate in the dropdown 
and 'SPACE' to select the current option.

'ENTER' exits the app and adds the current command text to the clipboard.

![bins report](https://raw.githubusercontent.com/marilsoncampos/cmdwerk/master/docs/source/_static/ppt_interactive.gif)


##### 7.2. Command to sync the prompt data with the history file.

```bash
    $ cmdw ppt sync
```

it will produce a summary report like below:

```bash
    Saved history data to /Users/mcampos/.cmdwerk/history.bin
    History lines : 2837
    Loading errors: 1
```

# Credits

- Marilson Campos (marilson.campos@gmail.com)

