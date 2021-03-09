dev: 
	python run.py
docker_host_dev: 
	flask run --host 0.0.0.0
tests: 
	python -m unittest discover tests 
docker_test: 
	docker-compose -f docker-compose.tests.yml up --exit-code-from bit 
docker_dev: 
	docker-compose up


	

