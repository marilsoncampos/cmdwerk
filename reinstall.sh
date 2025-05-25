#!/bin/zsh 

pdm build
pipx uninstall cmdwerk || echo "*** Skipped uninstall ***"
PACKAGE_FILE=$(ls -1t dist/*.whl | grep cmdwerk | head -n 1)
pipx install $PACKAGE_FILE

