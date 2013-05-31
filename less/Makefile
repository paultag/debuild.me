LESS_SCRIPTS = debuild.me.css

LESSC = lessc
LESSCFLAGS = -x

.SUFFIXES:
.SUFFIXES: .less .css


all: build


build: $(LESS_SCRIPTS)


.less.css:
	$(LESSC) $(LESSCFLAGS) $< > $@


.PHONY: build
