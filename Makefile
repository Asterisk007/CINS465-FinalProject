all:
	docker build -t final-project .

run:
	docker run -it -p 8000:8000 final-project