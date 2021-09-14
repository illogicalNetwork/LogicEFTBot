setup:
	python3.7 -m pip install requests maya irc mysql-connector-python black rich

setup-discord:
	python3.7 -m pip install discord requests mysql-connector-python black

check: FORCE
	black *.py bot/*.py tests/*.py
	mypy bot --ignore-missing-imports
	mypy tests --ignore-missing-imports
	mypy *.py --ignore-missing-imports

test: check FORCE
	python3.7 -m unittest tests.bot

integration: FORCE
	python3.7 -m unittest tests.integration.twitch

initdb:
	# initialize the db with all tables needed. (for local dev)
	mysql --user="$MYSQL_USER" --password="$MYSQL_PASSWORD" --database="$MYSQL_DB" --execute="source seed.db"

twitch: FORCE
	python3.7 -m twitch_master

discord: FORCE
	python3.7 -m discordbot

FORCE:
