.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: test
test:
	cd demo && python3 manage.py test

.PHONY: lint
lint:
	cd demo && pylint demo store --rcfile=pylint.rc

.PHONY: security
security:
	safety check