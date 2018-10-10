import sys
import logging
import rds_config
import pymysql
import traceback

#rds settings
rds_host  = "srbhiblimbwh5j.cuceupwwww7d.us-east-1.rds.amazonaws.com"
bind_address = "0.0.0.0"
port = 3306
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
	conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5, port=port, bind_address=bind_address)
except:
	traceback.print_exc()
	logger.error("ERROR: Unexpected error: Could not connect to MySql instance. Hello testing.")
	sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

def handler(event, context):

	item_count = 0

	with conn.cursor() as cur:
		# cur.execute("drop table if exists Employee3")
		# cur.execute("create table Employee3 ( EmpID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (EmpID))")
		# cur.execute('insert into Employee3 (EmpID, Name) values(1, "Joe")')
		# cur.execute('insert into Employee3 (EmpID, Name) values(2, "Bob")')
		# cur.execute('insert into Employee3 (EmpID, Name) values(3, "Mary")')

		cur.execute("drop table if exists patient")
		cur.execute("drop table if exists appointment")
		cur.execute("drop table if exists stage")
		cur.execute("create table patient(\
			first_name VARCHAR(64) NOT NULL,\
			last_name VARCHAR(64) NOT NULL,\
			email VARCHAR(64) UNIQUE NOT NULL,\
			dob DATE NOT NULL,\
			since DATE NOT NULL,\
			patientID VARCHAR(16) NOT NULL PRIMARY KEY\
		)")
		cur.execute("create table appointment(\
	drName VARCHAR(64) REFERENCES doctor(name),\
	lastAppointmentDate DATETIME,\
	nextAppointmentDate DATETIME,\
	currentStage ENUM('A','B','C','D','E','F','G','H','I','J','0'), /* 0 type for people with no current stage */\
	nextStage ENUM('A','B','C','D','E','F','G','H','I','J','0'), /* 0 type for people with no next stage */\
	appointmentID varchar(64) NOT NULL PRIMARY KEY,\
	drAdvice varchar(512),\
	patientID varchar(64) references patient(patientID)\
)")
		cur.execute("create table stage(\
	stage ENUM('A','B','C','D','E','F','0') NOT NULL PRIMARY KEY,\
	description varchar(500)\
)")
		cur.execute("insert into stage values ('A', 'At this stage, we will be giving you advice on ...')")
		cur.execute("insert into stage values ('B', 'At this stage, we will be giving you advice on ...')")
		cur.execute("insert into stage values ('C', 'At this stage, we will be giving you advice on ...')")
		cur.execute("insert into stage values ('D', 'At this stage, we will be giving you advice on ...')")
		cur.execute("insert into stage values ('E', 'At this stage, we will be giving you advice on ...')")
		cur.execute("insert into stage values ('F', 'At this stage, we will be giving you advice on ...')")

		cur.execute("insert into patient values ('Diana','Wong', 'diana.wong@gmail.com','1990-03-13','2017-12-12','p001')")
		cur.execute("insert into patient values ('Katy','Wang', 'kw@gmail.com','1991-03-13','2017-12-12','p002')")
		cur.execute("insert into patient values ('Terri','Mack', 'tm@gmail.com','1992-03-13','2017-12-12','p003')")

		cur.execute("insert into appointment values ('Dr David Lee', '2018-03-03', '2018-10-10', 'A', 'B', 'a001','NULL', 'p001')")
		cur.execute("insert into appointment values ('Dr John Lee', '2018-03-03', '2018-10-10', 'B', 'B', 'a002','NULL', 'p002')")
		cur.execute("insert into appointment values ('Dr Krista Kapoor', '2018-03-03', '2018-10-10', 'C', 'F', 'a003','NULL', 'p003')")

		conn.commit()
	
	return "successful setting up of db"