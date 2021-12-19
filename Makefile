setup:
	python3.7 -m pip install requests maya irc mysql-connector-python black rich

setup-discord:
	python3.7 -m pip install discord requests mysql-connector-python black

check: FORCE
	black *.py bot/*.py tests/*.py
	mypy -m twitch-master --ignore-missing-imports
	mypy -m discordbot --ignore-missing-imports
	mypy -m tests.bot --ignore-missing-imports

test: check FORCE
	python3.7 -m unittest tests.bot

initdb:
	# initialize the db with all tables needed. (for local dev)
	mysql --user="$MYSQL_USER" --password="$MYSQL_PASSWORD" --database="$MYSQL_DB" --execute="source seed.db"

twitch: FORCE
	python3.7 -m twitch-master

discord: FORCE
	python3.7 -m discordbot

FORCE:
