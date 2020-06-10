# Ecosystem
Challenge for ecosystem team, built in python 3.7

### Pre-requisites
To run this project you need to have [docker-compose](https://docs.docker.com/compose/install/) or Python3.7 to setup your local virtual environment.

### Important notes:
This project was built to run the requested jobs in two ways:
- Running the scripts in [scripts](https://github.com/lucasgnavarro/ecosystem-challenge/tree/master/scripts) folder 
- Making the requests to the FastApi service that this project provides you.

### Running the scripts
- run `make build` to build the docker image.
- run the script required from the [scripts](https://github.com/lucasgnavarro/ecosystem-challenge/tree/master/scripts) folder 

### Running the FastApi service
- run `make run` to start the FastApi server in [localhost](http://localhost:8000)
- go to [swagger page](http://localhost:8000/docs) in the project to see all the active endpoints, you can finde payloads examples there.

----
### Setup your local environment for development:
**Pre-requisites:**
- Python 3.7

**Setup your virtualenvironemt**
- run `make init-venv` to create a virtual environment and config git-hooks.
- in the project root run `source .venv/bin/activate`

### Running testings and coverage tools
- run `make tests` to test the project and get the current code coverage.

### Checking cli.py usage
with your virtualenv activated, in the project root folder you can run:
- `python cli.py -h` 
```
NAME
    cli.py

SYNOPSIS
    cli.py COMMAND

COMMANDS
    COMMAND is one of the following:

     git_etl
       Extract valuable information from github repository

     url_haus_extraction
       Extract unique active malware urls from urlhaus
(END)

```
**To check each command usage**
-`python cli.py git_etl -h` 
```
NAME
    cli.py git_etl - Extract valuable information from github repository

SYNOPSIS
    cli.py git_etl REPO_URL SUBFOLDER SEARCH_KEYWORDS <flags>

DESCRIPTION
    Extract valuable information from github repository

POSITIONAL ARGUMENTS
    REPO_URL
        Repository base url. Example: https://github.com/mitre/cti/
    SUBFOLDER
        The path within the repo of the datasources tha we want to use. Example: enterprise-attack/attack-pattern
    SEARCH_KEYWORDS
        list of keys to extract from the datasources. Example ["type","spec_version",]

FLAGS
    --dump_file=DUMP_FILE
        if True dump transformation content into a file in temp dir with current timestamp

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
(END)

```

-`python cli.py url_haus_extraction -h`
```
NAME
    cli.py url_haus_extraction - Extract unique active malware urls from urlhaus

SYNOPSIS
    cli.py url_haus_extraction <flags>

DESCRIPTION
    Extract unique active malware urls from urlhaus

FLAGS
    --search_keywords=SEARCH_KEYWORDS
(END)

```

### Notes:
```
Point 1,2,3,4: core.github_etl 
                        -> app.utils.GitHelper
                        -> app.utils.TransformationHelper 
Point 5: core.url_haus_extraction
                        -> app.utils.download_and_save
                        -> app.utils.extract_file
                        -> app.utils.transform_csv
```

