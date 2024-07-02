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

class bucket_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def create(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "CREATE_BUCKET_SUCCESS",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            bucket_name = params["bucket_name"]
            access      = params["access"     ]
            encrypted   = params["encrypted"  ]
            compressed  = params["compressed" ]

            bucket_value     = bucket_name.replace(" ","_").upper()
            bucket_check_rec = self.mgdDB.db_bucket.find_one({
                "bucket_name" : bucket_name
            })
            if bucket_check_rec == None:
                str_created_time = time.strftime(
                        "%d-%m-%Y %H:%M:%S",
                        time.localtime(int(time.time()))
                )
                bucket_rec = database.get_record("db_bucket")
                bucket_rec["name"            ] = bucket_name
                bucket_rec["value"           ] = bucket_value
                bucket_rec["public"          ] = int( access     )
                bucket_rec["encrypted"       ] = int( encrypted  )
                bucket_rec["compressed"      ] = int( compressed )
                bucket_rec["str_created_time"] = str_created_time
                self.mgdDB.db_bucket.insert( bucket_rec )
            # end if
        except :
            self.webapp.logger.debug(traceback.format_exc())
            response["message_action"] = "CREATE_BUCKET_FAILED"
            response["message_action"] = "CREATE_BUCKET_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
# end class
