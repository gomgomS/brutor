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

class config_owner:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def upsert(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "ADD_OWNER_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:

            pkey        = params["pkey"]
            name        = params["name"]
            desc        = params["desc"]
            misc        = params["misc"]
            context     = params["context"]
            
            doc = self.mgdDB.db_config_vessel_owner.find_one({ "pkey" : pkey})
            if doc:
                self.mgdDB.db_config_vessel_owner.update(
                    { 
                        "pkey"      : doc['pkey'],
                    },
                    {
                        "$set":
                        { 
                            "name" : name, 
                            "desc" : desc,
                            "misc" : misc,
                            "context" : context, 
                        }
                    }
                )
                response["message_action"] = "UPDATE_OWNER_SUCCESS"
            else:

                doc = database.get_record("db_config_vessel_owner")
                doc["fk_user_id"] = params['fk_user_id']   
                doc["name"] = name
                doc["desc"] = desc      
                doc["misc"] = misc
                doc["context"] = context
                self.mgdDB.db_config_vessel_owner.insert( doc )

                response["message_action"] = "ADD_OWNER_SUCCESS"
            #endif

            #update item
            item_count = self.mgdDB.db_config_vessel_owner.find({}).count()
            self.mgdDB.db_config_all.update(
                {"value" : "CONFIG_OWNER"},
                {"$set"  : {"count" : item_count }}
            )
        except :
            self.webapp.logger.debug(traceback.format_exc())
            response["message_action"   ] = "ADD_OWNER_FAILED"
            response["message_action"   ] = "ADD_OWNER_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def

    def remove(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "REMOVE_OWNER_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            pkey = params["pkey"]
            self.mgdDB.db_config_vessel_owner.remove({ "pkey": pkey })
        except:
            self.webapp.logger.debug(traceback.format_exc())
            response["message_action"] = "REMOVE_OWNER_FAILED"
            response["message_action"] = "REMOVE_OWNER_FAILED: " + str(sys.exc_info())
        # end try

        return response
    # end def
# end class
