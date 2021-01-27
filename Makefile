typecheck: FORCE
		mypy -m twitch --ignore-missing-imports
		mypy -m tests.bot --ignore-missing-imports


setup:
	python3.7 -m pip install requests irc mysql-connector-python

test:
	python3.7 -m unittest tests.bot

initdb:
	# initialize the db with all tables needed. (for local dev)
	mysql --user="$MYSQL_USER" --password="$MYSQL_PASSWORD" --database="$MYSQL_DB" --execute="source seed.db"

twitch: FORCE
	python3.7 -m twitch

FORCE:
