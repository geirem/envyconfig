#!/usr/bin/env bash
python3 setup.py bdist_wheel -d dist
twine upload dist/*.whl
