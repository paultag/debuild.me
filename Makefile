#

LESSC = lessc
LESSCFLAGS = -x
STATIC = static
STATIC_CSS = $(STATIC)/css


all: build
	@echo "Nice."


dev: lint all


lint:
	flake8 debuild


build: clean
	$(LESSC) $(LESSCFLAGS) less/debuild.me.less > $(STATIC_CSS)/debuild.me.css


clean:
	rm -rf $(STATIC_CSS)
	mkdir -p $(STATIC_CSS)


.PHONY: lint build clean
