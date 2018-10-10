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
		cur.execute("create table patient(\
			first_name VARCHAR(64) NOT NULL,\
			last_name VARCHAR(64) NOT NULL,\
			email VARCHAR(64) UNIQUE NOT NULL,\
			dob DATE NOT NULL,\
			since DATE NOT NULL,\
			patientID VARCHAR(16) NOT NULL PRIMARY KEY\
			)")
		cur.execute("create table appointment(\
			drName VARCHAR(64) NOT NULL,\
			lastAppointmentDate DATE NOT NULL,\
			nextAppointmentDate DATE NOT NULL,\
			stage varchar(64) NOT NULL,\
			appointmentID varchar(64) NOT NULL PRIMARY KEY,\
			userid varchar(64) references patient(patientID)\
		)")
		conn.commit()
		cur.execute("select * from Employee3")
		for row in cur:
			item_count += 1
			logger.info(row)
			#print(row)
		conn.commit()
	str = "Added {} items from RDS MySQL table".format(item_count)

	return str