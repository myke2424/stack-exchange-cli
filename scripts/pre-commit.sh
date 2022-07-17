#!/bin/sh

STAGED_PY_FILES=$(git diff --diff-filter=d --cached --name-only | grep -E '\.(py)$')

run_formatting_on_staged_files() {
    for file in $STAGED_PYTHON_FILES; do
        poetry run black --line-length=120 file
        poetry run isort --line-length=120 file
    done
}

pylint_analysis() {
    for file in $STAGED_PYTHON_FILES; do
        poetry run pylint --fail-under=5 $file

        if [ $? -ne 0 ]; then
            echo "Pylint failed on staged file ${file}"
        fi
    done
}

run_formatting_on_staged_files