#

LESSCFLAGS = -x
STATIC = static
STATIC_CSS = $(STATIC)/css


all: build install
	@echo "Nice."


dev: lint all

devel:
	./devel.sh

lint:
	flake8 debuild


build: clean
	make -C less build

install:
	make -C less install

clean:
	rm -rf $(STATIC_CSS)
	mkdir -p $(STATIC_CSS)


.PHONY: lint build clean
