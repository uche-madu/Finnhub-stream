install:
	pip install -U pip &&\
	pip install -r requirements.txt

precommit:
	pre-commit install
	pre-commit run --all-files

test:
	pytest --cov=./ --cov-report=xml
