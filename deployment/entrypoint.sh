#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
# http://stackoverflow.com/questions/19622198/what-does-set-e-mean-in-a-bash-script
set -e

echo "Workdir: $(pwd)"

# Define help message
function show_help() {
    echo """
Usage: docker run <imagename> COMMAND

Commands

bash        : Start a bash shell
python      : Run a python command
upload      : Build & upload package to pypi

help        : Show this message
"""
}

# Run
case "$1" in
    bash)
        /bin/bash "${@:2}"
    ;;
    python)
        python "${@:2}"
    ;;
    upload)
        echo -e "\nCreating python wheel ..."
        rm -Rf dist/
        python3 setup.py sdist bdist_wheel

        echo -e "\nUploading wheel to pypi ..."
        python3 -m twine upload dist/*
    ;;
    upload_test)
        # Install it
        # pip3 install --extra-index-url https://test.pypi.org/legacy/ poeditor-client==0.0.10
        echo -e "\nCreating python wheel ..."
        rm -Rf dist/
        python3 setup.py sdist bdist_wheel

        echo -e "\nUploading wheel to pypi ..."
        python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    ;;
    *)
        show_help
    ;;
esac
