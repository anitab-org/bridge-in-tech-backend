dev: 
	python run.py
dockerdev: 
	flask run --host 0.0.0.0
dockertest: 
	python -m unittest discover tests
