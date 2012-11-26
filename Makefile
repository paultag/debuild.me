LESSC = lessc
LESSCFLAGS = -x

all: clean build

STATIC=debuild/static

clean:
	rm -rf $(STATIC)/css

build:
	mkdir $(STATIC)/css
	$(LESSC) $(LESSCFLAGS) less/debuild.me.less > $(STATIC)/css/debuild.css
