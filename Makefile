PROJECT_NAME=demo
APP_NAME=store

.PHONY: install
install:
	pip install pipenv
	pipenv install --dev

.PHONY: test
test:
	cd $(PROJECT_NAME) && pipenv run python3 manage.py test

PHONY: coverage
coverage:
	cd $(PROJECT_NAME) && pipenv run coverage run manage.py test

.PHONY: coverage-html
coverage-html:
	$(MAKE) coverage
	cd $(PROJECT_NAME) && pipenv run coverage html

.PHONY: coverage-report
coverage-report:
	$(MAKE) coverage
	cd $(PROJECT_NAME) && pipenv run coverage report

.PHONY: lint
lint:
	cd $(PROJECT_NAME) && pipenv run mypy --config-file mypy.ini .
	cd $(PROJECT_NAME) && pipenv run pylint $(PROJECT_NAME) $(APP_NAME) --rcfile=.pylintrc

.PHONY: security
security:
	pipenv run safety check