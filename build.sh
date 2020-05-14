#!/usr/bin/env bash

python3 setup.py clean --all
rm -rf dist
rm -rf build
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository testpypi dist/*
