VERSION := 0.0.1

setup:
	poetry install

run:
	hypercorn main:app --reload

lint:
	blue .

sort:
	isort .
