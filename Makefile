#


lint:
	flake8 debuild

build:
	@echo "Nothing to build yet"


dev: lint build


all: build
