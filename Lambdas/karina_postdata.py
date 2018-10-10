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
	resp = "Success"
	with conn.cursor() as cur:
		patient_id = event['patientid']
		next_stage = event['nextstage']
		advice = event['advice']

		sql_update = "update appointment set currentStage = (select nextStage from (select * from appointment) as tempAppointment where patientID = '%s'), nextStage = '%s', drAdvice = '%s' where patientID = '%s';" % (patient_id, next_stage, advice, patient_id)
		try:
			cur.execute(sql_update)
		except pymysql.MySQLError as e:
			resp = "Unable to add details. Please ensure patient exists in records."
			print('Got error {!r}, errno is {}'.format(e, e.args[0]))
		conn.commit()
	cur.close()
	conn.close()
	return resp