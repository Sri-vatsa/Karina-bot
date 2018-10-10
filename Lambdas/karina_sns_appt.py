import sys
import logging
import rds_config
import pymysql
import traceback
from datetime import datetime, timedelta 
import boto3

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

def _check_if_in_24hrs(appointment):
	current = datetime.today()
	if appointment < (current + timedelta(hours=48)):
		return True
	else:
		return False

def _generate_people_to_message(appointments):
	people_to_message = []
	for appointment in appointments:
		print("appointment")
		print(appointment)
		if _check_if_in_24hrs(appointment[2]): #2 is next appointment date
			people_to_message.append([appointment[7], appointment[2]]) #7 is patient id and 2 is next appointment date
	return people_to_message

def _find_contact_num_for_all(people_to_message):

	conn = connect_to_db()
	with conn.cursor() as cur:
		
		#TODO FILL WITH RIGHT INDEX OF PHONE NUMBER
		for i in range(len(people_to_message)):
			print(people_to_message[i][0])
			sql_select = "select contact from patient where patientID = '%s'" % people_to_message[i][0]
			cur.execute(sql_select)
			person_data = cur.fetchone()
			print("person data")
			print(person_data)
			contact = person_data[0]
			people_to_message[i].append(contact)

		conn.commit()
	cur.close()
	conn.close()

	return people_to_message

def _initialise_sns():
	# Initialize SNS client
	session = boto3.Session(region_name= "us-east-1")
	sns_client = session.client('sns')
	return sns_client

def _send_messages(sns_client, data):
	
	for person in data:
		# Send message
		date = person[1]
		#print(date)
		message = "Hi there! Don\'t forget your appointment on {0!s}".format(date)
		response = sns_client.publish(
			PhoneNumber= "+65" + person[2], 
			Message=message,
			MessageAttributes={
				'AWS.SNS.SMS.SenderID': {
					'DataType': 'String',
					'StringValue': 'Karina'
				},
				'AWS.SNS.SMS.SMSType': {
					'DataType': 'String',
					'StringValue': 'Promotional'
				}
			}
		)

		logger.info(response)


def handler(event, context):
	
	conn = connect_to_db()
	resp = "Success"
	with conn.cursor() as cur:

		sql_select = "select * from appointment"

		people_to_message = None
		all_appointments = None
		try:
			cur.execute(sql_select)
			all_appointments = cur.fetchall()
		except pymysql.MySQLError as e:
			print('Got error {!r}, errno is {}'.format(e, e.args[0]))

		if all_appointments is not None:
			print("all appointments")
			print(all_appointments)
			people_to_message = _generate_people_to_message(all_appointments)

		conn.commit()
	cur.close()
	conn.close()

	sns_ready_data = _find_contact_num_for_all(people_to_message)

	print("SNS ready data")
	print(sns_ready_data)

	# Send messages to people
	sns_client = _initialise_sns()
	_send_messages(sns_client, sns_ready_data)
	
	return resp