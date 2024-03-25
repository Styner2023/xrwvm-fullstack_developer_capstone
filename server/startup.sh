#!/bin/bash

# Name of your database file
DB_NAME="db.sqlite3"

# Name of the SQL dump file
DUMP_NAME="db_dump.sql"

# Import the SQL dump file into a new SQLite database
sqlite3 $DB_NAME < $DUMP_NAME

# Set the Django secret key and any other configuration
export SECRET_KEY='your-secret-key'
# Add any other configuration data here

# Start the Django server
python manage.py runserver

