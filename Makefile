LESSC = lessc
LESSCFLAGS = -x

all: clean build

clean:
	rm -rf ./css

build:
	mkdir css
	$(LESSC) $(LESSCFLAGS) less/debuild.me.less > css/debuild.css
