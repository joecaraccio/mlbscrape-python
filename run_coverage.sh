#!/usr/bin/env bash

export PYTHONPATH=$(PYTHONPATH):$(pwd)

cd tdd
coverage run run_tests.py
coverage html -d coverage_files

