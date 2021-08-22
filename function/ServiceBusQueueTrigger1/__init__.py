import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json
#from dotenv import load_dotenv


def main(msg: func.ServiceBusMessage):

    logging.info("here we are ....\n")
    notification_id = msg.get_body().decode('utf-8')

    logging.info('notification id %s', notification_id)
    logging.info(
        'Python ServiceBus queue trigger processing message: %s', notification_id)

    # TODO: Get connection to database .. i deleted the resource below immediately to avoid exposing my account
    # DEBUG = True
    POSTGRES_URL = "techconfdb.postgres.database.azure.com"
    POSTGRES_USER = "surambaya@techconfdb"
    POSTGRES_PW = "@cloudy2021"
    POSTGRES_DB = "techconfdb"
    SSL_MODE = True
    connection = None
    try:
        conn_str = "host={0} user={1} dbname={2} password={3}".format(
            POSTGRES_URL, POSTGRES_USER, POSTGRES_DB, POSTGRES_PW)
        connection = psycopg2.connect(conn_str)

        cursor = connection.cursor()

        logging.info(
            'Connected to the conf postgres database!!')
        # TODO: Get notification message and subject from database using the notification_id
        postgreSQL_select_Query = "select * from notification where id = %s"
        cursor.execute(postgreSQL_select_Query, (notification_id,))
        notification = cursor.fetchone()
        if notification is None:
            logging.info(
                'A notification with ID {} was not found on the database. No emails will be sent', notification_id)
        else:
            message = notification[2]
            subject = notification[5]
            # logging.info('subject: %s', subject)
            # logging.info('message: %s', message)

            # TODO: Get attendees email and name
            # TODO: Loop through each attendee and send an email with a personalized subject
            attendees_select = "select * from attendee"
            cursor.execute(attendees_select)
            attendees = cursor.fetchall()

            for row in attendees:
                # Query the database to retrieve a list of attendees (email and first name) ..current database columns
                # id, first_name, last_name,
                # conference_id, job_position,
                #  email, company, city, state,
                # interests, submitted_date, comments

                first_name = row[1]
                email = row[5]
                logging.info('email: %s', email)
                currsubject = 'Hi {} :  {}'.format(first_name, subject)
                logging.info('subject: %s', currsubject)
                logging.info('MESSAGE : %s ', message)
                sendemail(message=message, subject=currsubject, email=email)

            # TODO: Update the notification table by setting the completed date and updating the status with the
            # total number of attendees notified(assuming all have valid emails)
            notification_completed_date = datetime.utcnow()
            notification_status = 'Notified {} attendees'.format(
                len(attendees))
            logging.info(notification_status)
            notify_update = """Update notification set completed_date = %s, status = %s where id = %s"""
            cursor.execute(notify_update, (notification_completed_date,
                                           notification_status, notification_id))
            connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        # To help troubleshoot erors
        logging.exception(
            "Exception during trigger execution occured", exc_info=True)
    finally:
        # TODO: Close connection
        if connection:
            cursor.close()
            connection.close()
            logging.info("Connection Closed")


def sendemail(message, subject, email):
    if email is None:
        # no need to attemp sending to an empty email
        logging.info("\nunable to send message to blank email\n")
    else:
        message = Mail(
            # from_email=os.environ.get('ADMIN_EMAIL_ADDRESS'),
            from_email='info@aktech.co.ke',
            to_emails=email,
            subject=subject,
            plain_text_content=message)
        try:
            # on localhost i am using an .env file to store the key in the SENDGRID_API_KEY variable mentioned
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            sendstatus = 'email send status  {} \n'.format(
                response.status_code)
            logging.info(sendstatus)
        except (Exception, psycopg2.DatabaseError) as error:
            # This really helped to troubleshoot erors
            logging.exception(
                "Email send Exception Exception :", exc_info=True)
