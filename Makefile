install:
	pip install -r requirements.txt

run:
	PYTHONPATH=$(shell pwd) python API/fastapi_app.py

test:
	python -m unittest discover -p 'test*.py' -v

clean:
	rm -rf __pycache__
	rm -f *.pyc
	rm -f *.log
	rm -rf .pytest_cache

.PHONY: install run test clean