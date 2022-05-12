# Project Setup

[![Production Workflow](https://github.com/ThomasAnnamNJIT/final_flask_start/actions/workflows/prod.yml/badge.svg)](https://github.com/ThomasAnnamNJIT/is601-project-three/actions/workflows/production.yml)

* [Production Deployment](https://thomasannam-is601-prod.herokuapp.com)


[![Development Workflow](https://github.com/ThomasAnnamNJIT/final_flask_start/actions/workflows/dev.yml/badge.svg)](https://github.com/ThomasAnnamNJIT/is601-project-three/actions/workflows/dev.yml)

* [Developmental Deployment](https://thomasannam-is601-dev.herokuapp.com/)

## Running Locally

1. To Build with docker compose:
   docker compose up --build
2. To run tests, Lint, and Coverage report use this command: pytest --pylint --cov

.pylintrc is the config for pylint, .coveragerc is the config for coverage and setup.py is a config file for pytest


### Future Notes and Resources
* https://flask-user.readthedocs.io/en/latest/basic_app.html
* https://hackersandslackers.com/flask-application-factory/
* https://suryasankar.medium.com/a-basic-app-factory-pattern-for-production-ready-websites-using-flask-and-sqlalchemy-dbb891cdf69f
* https://develie.hashnode.dev/exploring-flask-sqlalchemy-queries
* https://wtforms.readthedocs.io/en/3.0.x/
* https://bootstrap-flask.readthedocs.io/en/stable/
* https://flask-sqlalchemy.palletsprojects.com/en/2.x/