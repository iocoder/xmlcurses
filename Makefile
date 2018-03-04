PPATH=$(shell pwd)

clean:
	sudo rm -rf build dist xmlcurses.egg-info

upload: clean
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*

docs:
    python setup.py build_sphinx

install2:
	sudo python2 setup.py install

install3:
	sudo python3 setup.py install

uninstall2:
	sudo pip2 uninstall xmlcurses

uninstall3:
	sudo pip3 uninstall xmlcurses

run:
	cd examples/$(EXAMPLE) && python $(EXAMPLE).py

run_local:
	cd examples/$(EXAMPLE) && PYTHONPATH=$(PPATH) python $(EXAMPLE).py

run2:
	cd examples/$(EXAMPLE) && python2 $(EXAMPLE).py

run2_local:
	cd examples/$(EXAMPLE) && PYTHONPATH=$(PPATH) python2 $(EXAMPLE).py

run3:
	cd examples/$(EXAMPLE) && python3 $(EXAMPLE).py

run3_local:
	cd examples/$(EXAMPLE) && PYTHONPATH=$(PPATH) python3 $(EXAMPLE).py

