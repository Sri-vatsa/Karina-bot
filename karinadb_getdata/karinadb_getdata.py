import sys
import logging
import rds_config
import pymysql
import traceback
import datetime

#rds settings
rds_host  = "srbhiblimbwh5j.cuceupwwww7d.us-east-1.rds.amazonaws.com"
bind_address = "0.0.0.0"
port = 3306
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def connect_to_db():
	try:
		conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5, port=port, bind_address=bind_address)
	except:
		traceback.print_exc()
		logger.error("ERROR: Unexpected error: Could not connect to MySql instance. Hello testing.")
		sys.exit()

	logger.info("SUCCESS: Connection to RDS mysql instance succeeded")
	return conn

def handler(event, context):

	conn = connect_to_db()

	with conn.cursor() as cur:
		patient_id = event['patientid']
		sql_select = "select * from appointment where patientID = '%s'" % patient_id
		cur.execute(sql_select)
		patient_data = cur.fetchall()
		
		# process data
		patient_data_serial = []
		for patient in patient_data:
			patient_datum = {}

			patient_datum["doctor"] = patient[0]
			patient_datum["prev_appt"] = patient[1].__str__()
			patient_datum["next_appt"] = patient[2].__str__()
			patient_datum["prev_stage"] = patient[3]
			patient_datum["next_stage"] = patient[4]
			patient_datum["appt_id"] = patient[5]
			patient_datum["patient_id"] = patient[7]
			patient_datum["advice"] = patient[6]

			patient_data_serial.append(patient_datum)
		conn.commit()
	cur.close()	
	conn.close()

	return patient_data_serial