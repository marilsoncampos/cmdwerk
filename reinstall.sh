#!/bin/zsh -e

make
pipx uninstall cmdwerk
pipx install dist/cmdwerk-0.1.0.tar.gz
