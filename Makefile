all: install run

run:
	python3 watch_and_reload.py
.PHONY: run

install:
	pip3 install -r requirement.txt
.PHONY: install