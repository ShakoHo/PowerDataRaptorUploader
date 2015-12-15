# Pull all dependencies for minionKevin

install: venv lib-install

venv:
ifndef VIRTUAL_ENV
		virtualenv env
endif

lib-install:
		. env/bin/activate; \
		python setup.py install;

clean:
		rm -rf env

