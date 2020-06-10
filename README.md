# Ecosystem
Challenge for ecosystem team, built in python 3.7

# Setup your local environment for development
- copy the `example.env` file to `.env` file in the project root folder.
- run `make init-venv` to create a virtual environment and config git-hooks.

# Running the project locally
- run `docker-compose up` to start the FastApi webserver in [localhost](http://localhost:8000)
- go to [swagger page](http://localhost:8000/docs) in the project to see all the active endpoints.

# Running testings and coverage tools
- run `source .venv/bin/activate´ to activate virtualenv.
- run `make tests` to test the project and get the current code coverage.

**Status**: Not finished
