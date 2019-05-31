#!/bin/bash

rm -rf build dist *.egg-info

python3 setup.py sdist
python3 setup.py bdist_wheel --universal