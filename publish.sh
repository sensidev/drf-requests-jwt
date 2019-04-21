#!/usr/bin/env bash

VIRTUALENV_PATH=$1
VIRTUALENV_PATH=${VIRTUALENV_PATH:="../virtualenv"}


function check() {
    if [[ $? -ne 0 ]]; then
        echo "FAILED!"
        exit 1
    fi
}

source ${VIRTUALENV_PATH}/bin/activate
check

pytest
check

echo "Building dist"
python setup.py sdist bdist_wheel
check

python -m twine upload dist/*
