import sys
import traceback
import datetime
import time
import ast # use to convert string to dictionary 
from   datetime import datetime

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )


from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config


class auth_util:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def
    
    def check_username_availability(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "USERNAME_AVAILABILITY_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            username      = params["username"]
            user_auth_rec = self.mgdDB.db_user_auth.find_one({
                "username"   : username 
            })
            self.webapp.logger.debug("-------------------------------------")
            self.webapp.logger.debug( params        )
            self.webapp.logger.debug( user_auth_rec )
            self.webapp.logger.debug("-------------------------------------")
            if user_auth_rec != None:
                messages_rec  = self.mgdDB.db_config_messages.find_one({
                    "value" : "USERNAME_AVAILABILITY_FAILED_1"
                })
                response["message_action"] = "USERNAME_AVAILABILITY_FAILED"
                response["message_code"  ] = messages_rec["code"   ]
                response["message_desc"  ] = messages_rec["message"]
                return response
            # end if
        except:
            self.mgdDB.webapp.logger.debug (traceback.format_exc())
            response["message_action"] = "USERNAME_AVAILABILITY_FAILED"
            response["message_action"] = "USERNAME_AVAILABILITY_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
# end class
