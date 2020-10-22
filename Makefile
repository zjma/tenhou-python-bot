format:
	isort project/*
	black project/*

lint:
	isort --check-only project/*
	black --check project/*
	flake8 project/*

tests:
	PYTHONPATH=./project pytest -n 4