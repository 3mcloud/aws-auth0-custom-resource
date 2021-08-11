export DOCKER_BUILDKIT=1
AWS_DEFAULT_REGION?=us-east-1
IMAGE_NAME=aws-auth0-cr
PROJECT=src
flags?=
link?=

build-%:
	docker build \
		--ssh default \
		$(flags) \
		-t $(IMAGE_NAME):$* \
		--target $* .

develop:
	docker run -it --rm \
		-e AWS_DEFAULT_REGION=us-east-1 \
		-v ${PWD}:/app \
		-p 5566:5678 \
		-w /app \
		${IMAGE_NAME}:test \
		bash

test-%:
	docker run -it --rm \
	-v ${PWD}:/app \
	-e AWS_DEFAULT_REGION=us-east-1 \
	${IMAGE_NAME}:test \
	pytest -s -v tests/$*

unit:
	python -m pytest -vvv \
		-W ignore::DeprecationWarning \
		--cov-report term-missing \
		--cov=$(PROJECT) \
		--cov-fail-under=85 \
		tests/unit$(target)

e2e:
	python -m pytest -vvv \
		-W ignore::DeprecationWarning \
		--cov-report html \
		--cov-report term-missing \
		--cov=$(PROJECT) \
		tests/e2e$(target)

lint:
	python -m pylint src/**/*.py tests/**/*.py


security:
	# Static analysis on common python vulnerabilities
	bandit -r $(PROJECT) -x setup.py
	# Check dependencies for known CVEs
	safety check --full-report

debug-%:
    # allows you to attach the vscode debugger to a test.
	# Use the debug console and attach the debugger after
	# you run `make debug`
	python -m ptvsd --host 0.0.0.0  --port 5678 --wait \
		-m pytest -vvv \
		tests/$*$(target)

test:
ifeq ($(CI),)
	$(eval CMD=test-)
else
	$(eval CMD:=)
endif
	make $(CMD)lint
	make $(CMD)security
	make $(CMD)unit

.PHONY: develop test
