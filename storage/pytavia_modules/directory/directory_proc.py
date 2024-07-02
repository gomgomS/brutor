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

class directory_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def create(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "CREATE_DIRECTORY_SUCCESS",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            directory_name   = params["directory_name"]
            parent_node_id   = params["parent_node_id"]
            fk_bucket_id     = None
            directory_string = ""
            bucket_rec       = self.mgdDB.db_bucket.find_one({
                "pkey" : parent_node_id
            })
            if bucket_rec   != None:
                fk_bucket_id = bucket_rec["value"]
                directory_string = "/" + directory_name
            else:
                folder_rec       = self.mgdDB.db_filesystem.find_one({
                    "current_node_id" : parent_node_id
                })
                fk_bucket_id     = folder_rec["fk_bucket_id"]
                directory_string = folder_rec["file_path"   ] + "/" + directory_name 
            # end if
            filesystem_rec = self.mgdDB.db_filesystem.find_one({
                "parent_node_id" : parent_node_id,
                "file_path"      : directory_string
            })
            if filesystem_rec == None:
                str_created_time = time.strftime(
                        "%d-%m-%Y %H:%M:%S", time.localtime(int(time.time()))
                )
                db_filespec_rec  = database.get_record("db_filesystem")
                db_filespec_rec["file_path"       ] = directory_string
                db_filespec_rec["filename"        ] = directory_name
                db_filespec_rec["parent_node"     ] = "BUCKET"
                db_filespec_rec["parent_node_id"  ] = parent_node_id
                db_filespec_rec["child_node"      ] = ""
                db_filespec_rec["child_node_id"   ] = ""
                db_filespec_rec["current_node"    ] = directory_name
                db_filespec_rec["current_node_id" ] = db_filespec_rec["pkey"]
                db_filespec_rec["fk_bucket_id"    ] = fk_bucket_id
                db_filespec_rec["str_created_time"] = str_created_time
                self.mgdDB.db_filesystem.insert( db_filespec_rec )
            # end if
            response["message_data"  ] = {
                "parent_node_id" : parent_node_id
            }
        except :
            self.webapp.logger.debug(traceback.format_exc())
            response["message_action"] = "CREATE_DIRECTORY_FAILED"
            response["message_action"] = "CREATE_DIRECTORY_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
# end class
