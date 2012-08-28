LESSC = lessc
LESSCFLAGS = -x

all: clean build

clean:
	rm -rf ./static/css

build:
	mkdir static/css
	$(LESSC) $(LESSCFLAGS) less/debuild.me.less > static/css/debuild.css
