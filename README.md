# Fellow_kids
[![Codacy Badge][codacy-badge]][codacy-url]
[![Discord chat][discord-badge]][discord-url]

The fellow_kids bot in the french fortress discord server

## Running
the recommended way to run the bot is through docker-compose

1. Rename `docker-compose.example.yml` to `docker-compose.yml`
2. Edit the yaml file with your Discord key and optionally a Merriam Webster thesaurus key
3. Run `docker-compose up -d` to build and run the bot along with the postgresql database and detach from the container
4. Stop the container using `docker-compose stop`

if you cannot or do not wish to run using docker follow these steps

1. [Install Pipenv](https://github.com/pypa/pipenv#installation)
2. Run `pipenv install` to install dependencies
3. Run these commands inside the psql client
```sql
CREATE USER fellow_kids WITH LOGIN PASSWORD 'fellow_kids';
CREATE DATABASE fellow_kids OWNER fellow_kids;
```
4. Rename `config.example.json` to `config.json` and edit the values with your Discord api key and optionally a Merriam Webster api key
5. Run the bot using `pipenv run python fellow_kids.py`

[codacy-badge]: https://api.codacy.com/project/badge/Grade/a0957cdb0de64e70b60b3333a4a20eaa
[codacy-url]: https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=peppizza/discordBot&amp;utm_campaign=Badge_Grade
[discord-badge]: https://img.shields.io/discord/684472795639447621.svg?logo=discord&style=flat-square
[discord-url]: https://discord.gg/nP9JY4C
