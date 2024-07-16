

import sys
import traceback
import datetime
import time
import ast # use to convert string to dictionary 
from   datetime import datetime
import random
import re

from view   import view_core_menu

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_stdlib import emailproc
from pytavia_core   import database
from pytavia_core   import config
from uuid     import uuid4
from flask import request 
from xml.sax            import saxutils as su

class profile_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def send_cv(self, params):    
        result_url = "/profile"
        
        unique_4_number             = random.randint(1000,9999)
        params["unique_4_number"]   = str(unique_4_number)

        # Get the current date
        apply_date           = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    

        # cv_user_html
        cv_user_html        = su.unescape(params["cv_user"])

        clean               = re.compile('<.*?>')
        params["cv_user"]   = re.sub( clean, '',cv_user_html)

        list_cv_user        = params["cv_user"].split(' ')
        list_cv_user        = list_cv_user[0:10]
        list_cv_user.append("...")
        cv_user_preview     = " ".join(list_cv_user)

        query   = {
            "phone"              : params["phone"],
            "cv_user"            : params["cv_user"],
            "cv_user_html"       : cv_user_html,
            "cv_user_preview"    : cv_user_preview,
            "cv_link"            : params["cv_link"],
            "summery_status_applying" : "WAITING"
        }

        update_doc = {
            "$set": query
        }

        summery_status_applying   = self.mgdDB.db_user.find_one(
            {"fk_user_id"         : params["fk_user_id"]},
            {"_id":0,"summery_status_applying":1}
        )
     
        if summery_status_applying["summery_status_applying"] != "WAITING":
            
            status_applying = {
                "status"            : "WAITING",
                "apply_date"        : apply_date                
            }     

            update_doc["$push"] = {"status_applying": status_applying}
      
        # Update the document in MongoDB
        user_rec                    = self.mgdDB.db_user.update_one(
            {"fk_user_id"         : params["fk_user_id"]},            
            update_doc            
        )
        
        return result_url

        
    def update_cv(self, params):    
        result_url = "/profile"
       

        query   = {
            "name"             : params["name"],
            "username"         : params["username"],     
            "email"            : params["email"]            
        }

        if params["email"] != params["old_email"]:
            query["ver_email"] = "FALSE"


        update_doc = {
            "$set": query
        }
      
        # Update the document in MongoDB
        user_rec                    = self.mgdDB.db_user.update_one(
            {"fk_user_id"         : params["fk_user_id"]},            
            update_doc            
        )
        
        return result_url

    def change_portal_tutor(self, params):    
        result_url = "/user/dashboard"

        query ={}

        register_teacher   = self.mgdDB.db_user.find_one(
            {"fk_user_id"         : params["fk_user_id"]},
            {"_id":0,"register_teacher":1}
        )        
     
        if register_teacher["register_teacher"] == "TRUE":        
            query["role"] = "TUTOR"

        update_doc = {
            "$set": query
        }
      
        # Update the document in MongoDB
        user_rec                    = self.mgdDB.db_user.update_one(
            {"fk_user_id"         : params["fk_user_id"]},            
            update_doc            
        )
        
        return result_url

        