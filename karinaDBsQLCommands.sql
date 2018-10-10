/* 
MySQL 5.7.22, RDS db.m3.medium
*/

/* 

Authentication Stuff

RDSHOST="host=srbhiblimbwh5j.cuceupwwww7d.us-east-1.rds.amazonaws.com"
TOKEN="$(aws rds generate-db-auth-token --hostname $RDSHOST --port 3306 --region us-east-1c --username karinadb )"

mysql --host=$RDSHOST --port=3306 --ssl-ca=/Users/harsh/Desktop/rds-ca-2015-root.pem --enable-cleartext-plugin --user=karinadb --password=$TOKEN 

*/

drop table if exists patient;
drop table if exists appointment;
drop table if exists stage;

/* Create new instance of a patient table */

create table patient(
	first_name VARCHAR(64) NOT NULL,
	last_name VARCHAR(64) NOT NULL,
	email VARCHAR(64) UNIQUE NOT NULL,
	dob DATE NOT NULL,
	since DATE NOT NULL,
	patientID VARCHAR(16) NOT NULL PRIMARY KEY
);

/* Create new instance of an appointment table */

create table appointment(
	drName VARCHAR(64) REFERENCES doctor(name),
	lastAppointmentDate DATETIME,
	nextAppointmentDate DATETIME,
	currentStage ENUM('A','B','C','D','E','F','G','H','I','J','0'), /* 0 type for people with no current stage */
	nextStage ENUM('A','B','C','D','E','F','G','H','I','J','0'), /* 0 type for people with no next stage */
	appointmentID varchar(64) NOT NULL PRIMARY KEY,
	drAdvice varchar(512),
	patientID varchar(64) references patient(patientID)
);

/* We will keep infromation about different stages in this table */

create table stage(
	stage ENUM('A','B','C','D','E','F','0') NOT NULL PRIMARY KEY,
	description varchar(500)
);

/* Populate stage table with mock data = update this later on with real stage*/

insert into stage values ('A', 'At this stage, we will be giving you advice on ...');
insert into stage values ('B', 'At this stage, we will be giving you advice on ...');
insert into stage values ('C', 'At this stage, we will be giving you advice on ...');
insert into stage values ('D', 'At this stage, we will be giving you advice on ...');
insert into stage values ('E', 'At this stage, we will be giving you advice on ...');
insert into stage values ('F', 'At this stage, we will be giving you advice on ...');

/* Populate patient table with mock data */

insert into patient values ('Diana','Wong', 'diana.wong@gmail.com','1990-03-13','2017-12-12','p001');
insert into patient values ('Katy','Perry', 'katyperry@gmail.com','1991-03-13','2017-12-12','p002');
insert into patient values ('Krista','Steward', 'krista@gmail.com','1980-03-13','2017-12-12','p003');

/* Populate appointment table with mock data */

insert into appointment values ('Dr David Lee', '2018-03-03', '2018-10-10', 'A', 'B', 'a001','drink more water', 'p001');
insert into appointment values ('Dr Happy Lee', '2018-04-03', '2018-09-10', 'B', 'D', 'a002','drink more juice', 'p002');
insert into appointment values ('Dr Happy Lee', '2018-05-03', '2018-11-10', 'A', 'D', 'a003','drink more milk', 'p003');

insert into appointment values ('Dr David Lee', '2018-03-03', '2018-10-11', 'B', 'E', 'a004','pee more', 'p001');

/* Patient views their current stage */

select currentStage from appointment where patientID = 'p123'

/* View all appointment information from a patient using their ID*/

select * from patient where patientID = 'p123';

/* Patient views next appointment using this command */

select nextAppointmentDate from appointment where patientID = 'p123';

/* Patient updates their next appointment date */

update appointment set nextAppointmentDate = '2020-12-12' where patientID = 'p123';

/* Set next appointment as current appointment, and update next appointment 
with new appointment date */

update appointment 
set currentStage = 
(
select nextStage 
from (select * from appointment) as tempAppointment 
where patientID = 'p123'
), 
nextStage = 'C' where patientID = 'p123';

insert into appointment values ('Dr Happy Lee', '2018-05-03 12:12:12', '2018-11-10', 'A', 'D', 'a005','NULL', 'p003');

select * from appointment where appointmentid = 'a005'

select appointmentID from appointment where patientID = 'a005' order by appointmentID desc;




