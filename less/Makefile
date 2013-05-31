LESS_SCRIPTS = debuild.me.css

LESSC = lessc
LESSCFLAGS = -x

STATIC = ../static
STATIC_CSS = $(STATIC)/css

.SUFFIXES:
.SUFFIXES: .less .css


all: build install


build: $(LESS_SCRIPTS)


install:
	mv debuild.me.css $(STATIC_CSS)/debuild.me.css


.less.css:
	$(LESSC) $(LESSCFLAGS) $< > $@


.PHONY: build
