#!/usr/bin/python3

import sys
import json
import MySQLdb
import subprocess
from liquidplanner import  LiquidPlanner

DATABASE = ""
DB_USERNAME = ""
DB_PASSWORD = ""
LP_USERNAME = ""
LP_PASSWORD = ""
PROJECT_ID = ""
TEAM_ID = ""

LP = LiquidPlanner(LP_USERNAME, LP_PASSWORD)

conn = MySQLdb.connect("localhost",DB_USERNAME,DB_PASSWORD,DATABASE)
cur = conn.cursor()
cur.execute("SELECT account, notes, next_event FROM {0}.password_reset WHERE next_event > NOW() AND next_event < DATE_ADD(NOW(),INTERVAL 14 DAY);".format(DATABASE))
upcoming = cur.fetchall()

for event in upcoming:
    # Do things with the event

    data = {
        "parent_id":PROJECT_ID,
        "name":event[0],
        "team_id":TEAM_ID
    }

	process = subprocess.Popen(["./passgen.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (stdout, stderr) = process.communicate()
    
	if stderr is "":
        print("Failed to generate password.")
    else:
        password = stdout.decode('ascii')
        print(password)
		continue

    result = LP.create_task(data)

	try:
        print("Name: {}".format(result["name"]))
    except:
        print("Failed to create task for {}".format(data["name"]))
        continue

    try:
        cur.execut("UPDATE {0}.password_reset SET password = {1} WHERE account = {2};".format(DATABASE, password, event[0]))

	data = {
        "id":result["id"],
        "comment":event[1]
    }

    result = LP.add_comment(data)

    try:
        result["id"]
    except:
        print("Failed to comment on task.")

cur.execute("UPDATE {0}.password_reset SET next_event = DATE_ADD(next_event, INTERVAL (SELECT expiration) DAY) WHERE next_event > NOW() AND next_event < DATE_ADD(NOW(),INTERVAL 14 DAY);".format(DATABASE))
conn.commit()
cur.close()
conn.close()
