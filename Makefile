play:
	python3 main.py

debug:
	python3 main.py -v

insane:
	python3 main.py -c insane_set.json

test:
	python3 test_permutations.py
	python3 test_set.py

test_set:
	python3 test_set.py


# PEP8 Linting
LINTFILES=./
# PEP 8 Warning to ignore, when adding please add a comment on what we are ignoring
# E261 at least two spaces before inline comment
# E501 line too long (96 > 79 characters)
# E128 continuation line under-indented for visual indent
LINT_EXTEND_IGNORE=E501,E261,E128
# Files to exclude from linting
LINT_EXCLUDE=""
# per-file lint ignores
# see https://flake8.pycqa.org/en/latest/user/options.html?highlight=per-file-ignores#cmdoption-flake8-per-file-ignores
LINT_PER_FILE_EXCLUDE=""

.phony: lint
lint:
	flake8 $(LINTFILES) --extend-ignore=$(LINT_EXTEND_IGNORE) --exclude=$(LINT_EXCLUDE) --per-file-ignores=$(LINT_PER_FILE_EXCLUDE)

help:
	@echo "make test - run the tests"
	@echo "make lint - run the linter"
	@echo "make debug - run the simulator with verbose output"
