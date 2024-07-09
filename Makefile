all: install run

run:
	python3 main.py
.PHONY: run

install:
	pip3 install -r requirement.txt
.PHONY: install