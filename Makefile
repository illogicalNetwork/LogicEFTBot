typecheck: FORCE
		mypy -m twitch --ignore-missing-imports

setup:
	python3.7 -m pip install requests irc mysql-connector-python

initdb:
	# initialize the db with all tables needed. (for local dev)
	mysql --user="$MYSQL_USER" --password="$MYSQL_PASSWORD" --database="$MYSQL_DB" --execute="source seed.db"

twitch: FORCE
	python3.7 -m twitch

FORCE:
