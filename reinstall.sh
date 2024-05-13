#!/bin/zsh -e


make
pipx uninstall cmdwerk
PACKAGE_FILE=$(ls dist/*.whl | grep cmdwerk | head -n 1)
pipx install $PACKAGE_FILE

