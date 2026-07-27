NAME = a_maze_ing.py

CONFIG = config.txt

CACHE = __pycache__ .mypy_cache mazegen/__pycache__ mlx/__pycache__

run:
	python3 $(NAME) $(CONFIG)

install:
	pip install -r requirements.txt

debug:
	python -m pdb $(NAME) $(CONFIG)

clean: 
	rm -rf $(CACHE)

lint:
	flake8
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: 
	flake8
	mypy . --strict

.PHONY: run install debug clean lint lint-strict