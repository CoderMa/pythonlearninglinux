#!/bin/bash
if ! command -v pytest &> /dev/null
then
    echo "Error: pytest is not installed. Install it with 'pip install pytest'."
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Running all tests..."
    pytest
elif [ $# -eq 1 ] && [ -d ${1} ]; then
    echo "Running tests in directory: ${1}"
    pytest ${1}
elif [ $# -eq 1 ] && [ -f ${1} ]; then
    echo "Running tests in file: ${1}"
    pytest ${1}
else
    echo "Running tests with markers: ${@:1}"
    pytest -m ${@:1}
fi
