# Define variables
APP_NAME = halo
PYTHON = python
PIP = pip
FLASK = flask
GUNICORN = gunicorn
NPM = npm

# Development tasks
install-dependencies:
	$(PIP) install -r requirements.txt
	$(NPM) install --prefix reactFrontend

run-dev:
	$(PYTHON) manager.py

run-frontend-dev:
	$(NPM) start --prefix reactFrontend

# Docker-compose
run-docker:
	sudo docker-compose build && sudo docker-compose up

# Deployment tasks
deploy-heroku:
	heroku create
	git add .
	git commit -m "initial commit"
	git push heroku master

# Common tasks
clean:
	rm -rf _pycache_ *.pyc *.pyo
	$(NPM) run clean --prefix reactFrontend

# Default task
help:
	@echo "Available tasks:"
	@echo "  install-dependencies  : Install Python and frontend dependencies"
	@echo "  run-dev               : Run the Flask app locally for development"
	@echo "  run-frontend-dev      : Run the frontend locally for development"
	@echo "  run-docker            : Build and run the app using Docker Compose"
	@echo "  deploy-heroku         : Deploy the app to Heroku"
	@echo "  clean                 : Clean up temporary files"
	@echo "  help                  : Show this help message"

.PHONY: install-dependencies run-dev run-frontend-dev run-docker deploy-heroku clean help
