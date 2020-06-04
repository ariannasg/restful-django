.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: test
test:
	cd demo && python3 manage.py test

.PHONY: coverage-report
coverage-report:
	cd demo && coverage run manage.py test && coverage report

.PHONY: coverage-html
coverage-html:
	cd demo && coverage run manage.py test && coverage html

.PHONY: lint
lint:
	cd demo && pylint demo store --rcfile=.pylintrc

.PHONY: security
security:
	safety check