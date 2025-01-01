import sys
import traceback
import datetime
import os
from pymongo import MongoClient

sys.path.append("../")
sys.path.append("../pytavia_core")
sys.path.append("../pytavia_modules")
sys.path.append("../pytavia_settings")
sys.path.append("../pytavia_stdlib")
sys.path.append("../pytavia_storage")

from pytavia_core import database
from pytavia_core import config


class process_user_cleanup:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self):
        pass

    def process(self, params):
        print("-CLEANUP DB_USER-")
        print("=======================================")

        try:
            # Query to find users with ver_email = 'FALSE'
            query = {"ver_email": "FALSE"}
            users_to_delete = list(
                self.mgdDB.db_user.find(query, {"email": 1, "name": 1, "phone": 1, "_id": 0})
            )

            if not users_to_delete:
                print("No users found with ver_email set to 'FALSE'.")
                return

            # Log user details to a text file
            log_dir = "../static/user_cleanup_logs/"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
                print("Log directory created")

            log_file_path = os.path.join(log_dir, f"user_cleanup_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(log_file_path, "w") as log_file:
                log_file.write("Deleted Users Log\n")
                log_file.write("=================\n")
                for user in users_to_delete:
                    log_file.write(f"Email: {user.get('email', '')}, Name: {user.get('name', '')}, Phone: {user.get('phone', '')}\n")

            print(f"User details logged to {log_file_path}")

            # Delete users from the database
            delete_result = self.mgdDB.db_user.delete_many(query)
            print(f"Deleted {delete_result.deleted_count} users with ver_email set to 'FALSE'.")

        except Exception as e:
            print("An error occurred during cleanup:")
            print(traceback.format_exc())


if __name__ == "__main__":
    try:
        ps = process_user_cleanup()
        ps.process({})
    except:
        print(traceback.format_exc())
