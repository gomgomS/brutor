import config_core
import sys
import traceback

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib   import idgen
from pytavia_stdlib   import utils
from pytavia_core     import database
from pytavia_core     import config

class config_document_type:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def upsert(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "ADD_DOC_TYPE_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:

            name        = params["name"         ]
            value       = params["value"        ]
            desc        = params["desc"         ]
            misc        = params["misc"         ]
            context     = params["context"      ]

            doc = self.mgdDB.db_config_document_type.find_one({ "value" : value})
            if doc:
                self.mgdDB.db_config_document_type.update(
                    { 
                        "pkey"      : doc['pkey'],
                    },
                    { "$set"        : { 
                        "name"      : name, 
                        "value"     : value,
                        "desc"      : desc,
                        "context"   : context, 
                        "misc"      : misc,
                        }
                    }
                )

                response["message_action"] = "UPDATE_DOC_TYPE_SUCCESS"
            else:

                doc = database.get_record("db_config_document_type")
                doc["fk_user_id"      ] = params['fk_user_id']   
                doc["name"            ] = name
                doc["value"           ] = value  
                doc["desc"            ] = desc      
                doc["misc"            ] = misc
                doc["context"         ] = context

                self.mgdDB.db_config_document_type.insert( doc )

                response["message_action"] = "ADD_DOC_TYPE_SUCCESS"
            
        except :
            self.webapp.logger.debug(traceback.format_exc())
            response["message_action"   ] = "ADD_DOC_TYPE_FAILED"
            response["message_action"   ] = "ADD_DOC_TYPE_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def

    def remove(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "REMOVE_DOC_TYPE_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            value = params["value"]
            self.mgdDB.db_config_document_type.remove({ "value": value })
        except:
            self.webapp.logger.debug(traceback.format_exc())
            response["message_action"] = "REMOVE_DOC_TYPE_FAILED"
            response["message_action"] = "REMOVE_DOC_TYPE_FAILED: " + str(sys.exc_info())
        # end try

        return response
    # end def
# end class
