#!/usr/bin/bash
# jupyter nbconvert --to markdown README.ipynb
rm -rf build/ dist/
python setup.py build
python setup.py sdist
twine upload dist/*
