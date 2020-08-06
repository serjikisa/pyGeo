export FLASK_APP=main.py

dev:
	export FLASK_ENV=development && flask run

docker-build:
	docker build -t geo-rest-img .

docker-rmi:
	docker rmi -f geo-rest-img

test:
	export GOOGLE_API_KEY=some_key && python -m unittest discover
