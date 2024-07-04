import mysql.connector
from mysql.connector import errorcode
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Database connection details
db_config = { 
 'user': 'root', 
 'password': '12345', 
 'host': 'localhost', 
} 
# Connect to MySQL server and create database
def create_database(cursor): 
 try: 
 cursor.execute("CREATE DATABASE IF NOT EXISTS election_db") 
 cursor.execute("USE election_db") 
 print("Database 'election_db' created or already exists.") 
 except mysql.connector.Error as err: 
 print(f"Failed creating database: {err}") 
 exit(1) 
# Create tables
def create_tables(cursor): 
 tables = { 
 'candidates': ( 
 "CREATE TABLE IF NOT EXISTS candidates ("
 " candidate_id INT AUTO_INCREMENT PRIMARY KEY,"
 " name VARCHAR(255) NOT NULL,"
 " party VARCHAR(255) NOT NULL"
 ")"), 
 'voters': ( 
 "CREATE TABLE IF NOT EXISTS voters ("
 " voter_id INT AUTO_INCREMENT PRIMARY KEY,"
 " name VARCHAR(255) NOT NULL,"
 " age INT NOT NULL,"
 " voted BOOLEAN NOT NULL DEFAULT FALSE"
 ")"), 
 'votes': ( 
 "CREATE TABLE IF NOT EXISTS votes ("
 " vote_id INT AUTO_INCREMENT PRIMARY KEY,"
 " voter_id INT NOT NULL,"
 " candidate_id INT NOT NULL,"
 " FOREIGN KEY (voter_id) REFERENCES voters(voter_id),"
 " FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)"
 ")") 
 } 
 for table_name, table_description in tables.items(): 
 try: 
 cursor.execute(table_description) 
 print(f"Table '{table_name}' created or already exists.") 
 except mysql.connector.Error as err: 
 print(f"Failed creating table {table_name}: {err}") 
 exit(1) 
# Insert sample data
def insert_sample_data(cursor, cnx): 
 candidates = [('pavi', 'Party A'), ('bavithra', 'Party B'), ('mani', 'Party C')] 
 voters = [('uma', 40), ('pausi', 23), ('varnam', 50)] 
 add_candidate = "INSERT INTO candidates (name, party) VALUES (%s, %s)"
 add_voter = "INSERT INTO voters (name, age) VALUES (%s, %s)"
 try: 
 cursor.executemany(add_candidate, candidates) 
 cursor.executemany(add_voter, voters) 
 cnx.commit() 
 print("Inserted data into 'candidates' and 'voters' tables.") 
 except mysql.connector.Error as err: 
 print(f"Failed inserting data: {err}") 
# Query data
def query_data(cursor): 
 try: 
 cursor.execute("SELECT name, party FROM candidates") 
 for (name, party) in cursor: 
 print(f"Candidate: {name}, Party: {party}") 
 except mysql.connector.Error as err: 
 print(f"Failed querying data: {err}") 
# Send email with script
def send_email(script_content): 
 sender_email = "ssivaprakash58gmail.com"
 receiver_email = "aswin123@gmail.com"
 subject = "MySQL Election DB Script"
 msg = MIMEMultipart() 
 msg['From'] = sender_email
 msg['To'] = receiver_email
 msg['Subject'] = subject
 msg.attach(MIMEText(script_content, 'plain')) 
 try: 
 with smtplib.SMTP('smtp.gmail.com', 587) as server: 
 server.starttls() 
 server.login(sender_email, 'your_email_password') 
 server.sendmail(sender_email, receiver_email, msg.as_string()) 
 print("Email sent successfully.") 
 except Exception as e: 
 print(f"Error sending email: {e}") 
# Main script execution
def main(): 
 try: 
 cnx = mysql.connector.connect(**db_config) 
 cursor = cnx.cursor() 
 print("Connected to MySQL server.") 
 except mysql.connector.Error as err: 
 print(f"Connection error: {err}") 
 exit(1) 
 create_database(cursor) 
 create_tables(cursor) 
 insert_sample_data(cursor, cnx) 
 query_data(cursor) 
 cursor.close() 
 cnx.close() 
 script_content = """
import mysql.connector
from mysql.connector import errorcode
db_config = {
 'user': 'root',
 'password': '12345',
 'host': 'localhost',
}
try:
 cnx = mysql.connector.connect(**db_config)
 cursor = cnx.cursor()
 print("Connected to MySQL server.")
except mysql.connector.Error as err:
 if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
 print("Something is wrong with your user name or password")
 elif err.errno == errorcode.ER_BAD_DB_ERROR:
 print("Database does not exist")
 else:
 print(err)
 exit(1)
try:
 cursor.execute("CREATE DATABASE IF NOT EXISTS election_db")
 print("Database 'election_db' created or already exists.")
except mysql.connector.Error as err:
 print(f"Failed creating database: {err}")
 exit(1)
cursor.execute("USE election_db")
tables = {
 'candidates': (
 "CREATE TABLE IF NOT EXISTS candidates ("
 " candidate_id INT AUTO_INCREMENT PRIMARY KEY,"
 " name VARCHAR(255) NOT NULL,"
 " party VARCHAR(255) NOT NULL"
 ")"),
 'voters': (
 "CREATE TABLE IF NOT EXISTS voters ("
 " voter_id INT AUTO_INCREMENT PRIMARY KEY,"
 " name VARCHAR(255) NOT NULL,"
 " age INT NOT NULL,"
 " voted BOOLEAN NOT NULL DEFAULT FALSE"
 ")"),
 'votes': (
 "CREATE TABLE IF NOT EXISTS votes ("
 " vote_id INT AUTO_INCREMENT PRIMARY KEY,"
 " voter_id INT NOT NULL,"
 " candidate_id INT NOT NULL,"
 " FOREIGN KEY (voter_id) REFERENCES voters(voter_id),"
 " FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)"
 ")")
}
for table_name, table_description in tables.items():
 try:
 cursor.execute(table_description)
 print(f"Table '{table_name}' created or already exists.")
 except mysql.connector.Error as err:
 print(f"Failed creating table {table_name}: {err}")
 exit(1)
candidates = [('pavi', 'Party A'), ('bavithra', 'Party B'), ('mani', 'Party C')]
voters = [('uma', 40), ('pausi', 23), ('varnam', 50)]
add_candidate = "INSERT INTO candidates (name, party) VALUES (%s, %s)"
add_voter = "INSERT INTO voters (name, age) VALUES (%s, %s)"
try:
 cursor.executemany(add_candidate, candidates)
 cursor.executemany(add_voter, voters)
 cnx.commit()
 print("Inserted data into 'candidates' and 'voters' tables.")
except mysql.connector.Error as err:
 print(f"Failed inserting data: {err}")
query = "SELECT name, party FROM candidates"
try:
 cursor.execute(query)
 for (name, party) in cursor:
 print(f"Candidate: {name}, Party: {party}")
except mysql.connector.Error as err:
 print(f"Failed querying data: {err}")
cursor.close()
cnx.close()
"""
 send_email(script_content) 
if __name__ == "__main__": 
 main() 
