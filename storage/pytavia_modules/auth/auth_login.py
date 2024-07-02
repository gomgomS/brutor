import sys
import traceback
import datetime
import time

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config

class auth_login:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def login(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "LOGIN_SUCCESS",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            username        = params["username" ]
            password        = params["password" ]
            hashed_password = utils._get_passwd_hash({
                "id"        : username,
                "password"  : password
            })
            admin_user_rec  = self.mgdDB.db_admin_user.find_one({
                "username"  : username
            })
            if admin_user_rec == None:
                response["message_action"] = "LOGIN_FAILED"
                response["message_code"  ] = "1"
                return response
            # end if
        except :
            print (traceback.format_exc())
            response["message_action"] = "LOGIN_FAILED"
            response["message_action"] = "LOGIN_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
# end class
