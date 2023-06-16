# import psycopg2
# from psycopg2 import Error
from datetime import datetime
from main import models
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

# validate email using regular expretions
def validate_email(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

# for postgres db
# try:
#     connection = psycopg2.connect(
#         user="username",
#         password="password",
#         host="host",
#         port="port",
#         database="db",
#     )
#     cursor = connection.cursor()
# except (Exception, Error) as error:
#     print("Error while connecting to PostgreSQL:", error)

# def check_email_in_db(email, is_verified):
#     if not validate_email(email):
#         return False
#     query = 'SELECT * FROM "user" WHERE username = %s;'
#     try:
#         cursor.execute(query, (email,))
#         result = cursor.fetchone()
#         if result and not is_verified:
#             datetime_obj = datetime.strptime(str(result[3]), "%Y-%m-%d %H:%M:%S.%f")
#             date_only = datetime_obj.date()
#             return f"Email found in the database. Email was exposed at {date_only}"
#         elif is_verified:
#             return f"""<br>Email: {result[1]}<br>
#             Password: {result[2][0:2]}************<br>
#             Date: {result[3]}"""
#         else:
#             return False
#     except (Exception, Error) as error:
#         print(error)
#         return False

def check_email_in_db(email, is_verified): # 'is verified' is used to understand where user is checking email, in telegram bot or after him verified yourself.
    if not validate_email(email): # check is email valid
        return False
    try:
        data = models.ExposedUser.objects.filter(username=email) # try to get something from db using email
        result = data[0] # filter() returns Queriset (list of objects), so I use data[0] to get only first object
        if data.exists() and not is_verified:
            return f"Email found in the database. Email was exposed at {result.date_created}"
        elif is_verified:
            return f"""<br>Email: {result.username}<br>
            Password: {result.password[0:2]}************<br>
            Date: {result.date_created}"""
        else:
            return False
    except Exception as error:
        print(error)
        return False