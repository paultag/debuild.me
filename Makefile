#

LESSCFLAGS = -x
STATIC = static
STATIC_CSS = $(STATIC)/css


all: build
	@echo "Nice."


dev: lint all


lint:
	flake8 debuild


build: clean
	make -C less
	mv less/debuild.me.css $(STATIC)/css


clean:
	rm -rf $(STATIC_CSS)
	mkdir -p $(STATIC_CSS)


.PHONY: lint build clean
