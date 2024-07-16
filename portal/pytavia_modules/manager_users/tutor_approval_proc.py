import config_core
import sys
import traceback
import json
import ast
import time
import random
import re
from   datetime import datetime

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib     import idgen
from pytavia_stdlib     import utils
from pytavia_core       import database
from pytavia_core       import config
from pytavia_core       import helper
from pytavia_stdlib     import cfs_lib
from xml.sax            import saxutils as su


class tutor_approval_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def



    def set_meeting(self, params):    
        result_url = "/tutor_approval"

        # Get the current date
        apply_date           = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       
        # CONVERT STR DATETIME TO TIMESTAMP
        start_datetime_obj = utils._get_datetime_from_str_date(params["start_datetime"] ,date_format = '%d/%m/%Y %H:%M' )
        start_timestamp    = utils._convert_datetime_to_timestamp(start_datetime_obj)

        date_interview_str = start_datetime_obj.strftime('%d %B %Y %H:%M')
        
        status_applying = {
                "status"            : "SET MEETING",
                "link_meeting"      : params["link_meeting"],                
                "date_interview_timestamp" : start_timestamp,
                "date_interview_str"    : date_interview_str,
                "apply_date"            :apply_date
        }     
      
        # Update the document in MongoDB
        user_rec                    = self.mgdDB.db_user.update_one(
            {"user_uuid"         : params["user_uuid"]},            
            {
                '$set'            : {"summery_status_applying": "SET MEETING"},
                '$push'           : {"status_applying": status_applying}
            }      
        )
        
        return result_url

    def approval_tutor(self, params):    
        result_url = "/tutor_approval"

        # Get the current date
        apply_date           = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
        
        status_applying = {
                "status"            : "APPROVE",
                "apply_date"        : apply_date
        }     
      
        # Update the document in MongoDB
        user_rec                    = self.mgdDB.db_user.update_one(
            {"user_uuid"         : params["user_uuid"]},            
            {
                '$set'            : {"summery_status_applying": "APPROVE", "register_teacher": "TRUE"},
                '$push'           : {"status_applying": status_applying}
            }      
        )
        
        return result_url

        

# end class
