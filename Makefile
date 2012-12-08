LESSC = lessc
LESSCFLAGS = -x
DEPLOYMENT = dev

all: clean build

STATIC=./static

clean:
	rm -rf $(STATIC)/css

build: set-deployment-theme
	mkdir $(STATIC)/css
	$(LESSC) $(LESSCFLAGS) less/debuild.me.less > $(STATIC)/css/debuild.css

set-deployment-theme:
	rm -f less/config.deployment.less
	cp less/config.$(DEPLOYMENT).less less/config.deployment.less
