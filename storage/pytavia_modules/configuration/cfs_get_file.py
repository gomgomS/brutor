import sys
import traceback
import re
import time
import gridfs

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )
sys.path.append("pytavia_modules/configuration") 

from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config

class cfs_get_file:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self,app):
       self.webapp = app
    # end def

    def get(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "GET_CFS_FILE_SUCCES",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:

            self.webapp.logger.debug("-----------------------------------------")
            self.webapp.logger.debug( params )
            self.webapp.logger.debug("-----------------------------------------")

            key     = params["key"   ]
            bucket  = params["bucket"]
            if bucket != None:
                bucket  = params["bucket"]
            # end if
            cfs_rec = None
            if bucket != None:
                cfs_rec = self.mgdDB.db_blipcom_cfs.find_one({
                    "$and" : [
                        {"key"    : key    },
                        {"bucket" : bucket }
                    ]
                })
            else:
                cfs_rec = self.mgdDB.db_blipcom_cfs.find_one({
                    "key" : key
                })
            # end if
            if cfs_rec != None:
                content_type    = cfs_rec["content_type"]
                handle_mgd_grid = gridfs.GridFS(self.mgdDB)
                file_mgd_grid   = handle_mgd_grid.get( cfs_rec["fk_file_id"] )
                response["message_data"] = {
                    "raw_data"     : file_mgd_grid.read(),
                    "content_type" : content_type
                }
            else:
                response["message_data"] = {
                    "raw_data"     : "",
                    "content_type" : "text/html"
                }
            # end if
        except :
            print (traceback.format_exc())
            response["message_action"  ] = "GET_CFS_FILE_FAILED"
            response["message_desc"    ] = "GET_CFS_FILE_FAILED: " + str(sys.exc_info())
            response["message_data"    ] = {
                "raw_data"     : "",
                "content_type" : "text/html"
            }
        # end try
        return response
    # end def

    def get_all(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "GET_CFS_FILE_SUCCES",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            key     = params["key"   ]
            types   = params["type"  ]
            bucket  = params["bucket"]
            label   = params["label" ]
            cfs_rec = self.mgdDB.db_blipcom_cfs.find({
                "$and" : [
                    {"key"    : key    },
                    {"bucket" : bucket },
                    {"types"  : types  },
                 ]
            })
            cfs_list = []
            if cfs_rec != None:
                for cfs in cfs_rec :
                    cfs_convert   = cfs_convert.cfs_convert().convert(cfs)
                    cfs["decode"] = cfs_convert["decode"]
                    cfs_list.append(cfs)
                #end for
                response["message_data"  ] = cfs_list            
            else:
                response["message_action"] = "CFS_FILE_NOT_EXIST"
            #end if
        except :
            print (traceback.format_exc())
            response["message_action"] = "GET_CFS_FILE_FAILED"
            response["message_action"] = "GET_CFS_FILE__FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
    
    def get_one(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "GET_CFS_FILE_SUCCES",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            key    = params["key"   ]
            types  = params["type"  ]
            bucket = params["bucket"]
            label  = params["label" ]

            cfs_list = self.mgdDB.db_blipcom_cfs.find_one({
                "$and" : [
                    {"key"    : key     },
                    {"bucket" : bucket  },
                    {"types"  : types   },
                ]
            })
            if cfs_list != None:
                cfs_convert = cfs_convert.cfs_convert().convert(cfs_list)
                cfs_list["decode"] = cfs_convert["decode"]
                cfs_list.append(cfs)
                response["message_data"] = cfs_list            
            else:
                response["message_action"] = "CFS_FILE_NOT_EXIST"
            #end if
        except :
            print (traceback.format_exc())
            response["message_action"] = "GET_CFS_FILE_FAILED"
            response["message_action"] = "GET_CFS_FILE__FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
