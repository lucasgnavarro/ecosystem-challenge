# Powershell script for running git_etl with docker-compose(using docker container)
docker-compose run app python cli.py git_etl https://github.com/mitre/cti/ enterprise-attack/attack-pattern "['type','spec_version','objects[0].x_mitre_data_sources[0]']"
