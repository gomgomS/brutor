import sys
import traceback
import base64

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config

class cfs_convert_file:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self,app):
        self.webapp = app
    # end def

    def get_file(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "GET_CFS_FILE_SUCCES",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            key             = params["key"      ]
            bucket          = params["bucket"   ]
            #label           = params["label"]            
            
            cfs_rec =  self.mgdDB.db_blipcom_cfs.find_one({
                    "$and" : [
                            {"key"      : key       },
                            {"bucket"   : bucket    }
                    ]
            })
                      
            
            if cfs_rec != None:
                data = {
                    "key"       : cfs_rec["key"             ],
                    "conType"   : cfs_rec["content_type"    ],
                    "encode"    : cfs_rec["encode"          ]
                }
                response["message_data"] = data
            #end if 
        except:
            print (traceback.format_exc())
            response["message_action"] = "ADD_CFS_FILE_FAILED"
            response["message_action"] = "ADD_CFS_FILE__FAILED: " + str(sys.exc_info())              
        return response

    def get_json_file(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "GET_CFS_FILE_SUCCES",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            key             = params["key"      ]
            bucket          = params["bucket"   ]
            #label           = params["label"]            
            
            cfs_rec =  self.mgdDB.db_blipcom_cfs.find_one({
                    "$and" : [
                            {"key"      : key       },
                            {"bucket"   : bucket    }
                    ]
            })
                      
            key       = cfs_rec["key"         ] 
            extension = cfs_rec["extension"   ]
            conType   = cfs_rec["content_type"]
            filename  = key+"."+extension
            conDis   = "attachment; filename=" + filename
            if cfs_rec != None:
                data = {
                    "key"             : key     ,
                    "conType"         : conType ,
                    "conDis"          : conDis  ,
                    "file_dencode"    : cfs_rec["encode"].decode()
                }
                response["message_data"] = data
            #end if 
        except:
            print (traceback.format_exc())
            response["message_action"] = "ADD_CFS_FILE_FAILED"
            response["message_action"] = "ADD_CFS_FILE__FAILED: " + str(sys.exc_info())              
        return response
