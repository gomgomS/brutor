import config_core
import sys
import traceback

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config

class config_role_privilege(config_core.config_core):

    mgdDB = database.get_db_conn(config.mainDB)

    def __ini__(self):
        config_core.config_core.__init__(self)
    # end def

    def update(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "ADD_CONFIG_ROLE_PRIVILEGE_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            name      = params["name"     ]
            value     = params["value"    ]
            privilege = params["privilege"]
            status    = params["status"   ]
            role      = params["role"     ]

            config_role_privilege_rec = database.get_record("db_config_webapp_role_privilege")
            config_role_privilege_rec["name"           ] = name
            config_role_privilege_rec["value"          ] = value
            config_role_privilege_rec["status"         ] = status
            config_role_privilege_rec["fk_privilege_id"] = privilege
            config_role_privilege_rec["fk_role_id"     ] = role
            config_role_privilege_check = self.mgdDB.db_config_webapp_role_privilege.find_one({
                "value" : value
            })
            if config_role_privilege_check == None:
                self.mgdDB.db_config_webapp_role_privilege.insert( config_role_privilege_rec )
            else:
                self.mgdDB.db_config_webapp_role_privilege.update(
                    {"value" : value},
                    {"$set"  : {
                        "name"           : name      ,
                        "value"          : value     ,
                        "status"         : status    ,
                        "fk_privilege_id": privilege ,
                        "fk_role_id"     : role      , 
                    }}
                )
            # end if
            item_count = self.mgdDB.db_config_webapp_role_privilege.find({}).count()
            self.mgdDB.db_config_all.update(
                {"value" : "ROLE_PRIVILEGE_MAPPING"},
                {"$set"  : {"count" : item_count  }}
            )
        except :
            print (traceback.format_exc())
            response["message_action"] = "ADD_CONFIG_ROLE_PRIVILEGE_FAILED"
            response["message_action"] = "ADD_CONFIG_ROLE_PRIVILEGE_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def

    def remove(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "REMOVE_CONFIG_ROLE_PRIVILEGE_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            value = params["value"]
            self.mgdDB.db_config_webapp_role_privilege.remove({ "value" : value })
            item_count = self.mgdDB.db_config_webapp_role_privilege.find({}).count()
            self.mgdDB.db_config_all.update(
                {"value" : "ROLE_PRIVILEGE_MAPPING"},
                {"$set"  : {"count" : item_count }}
            )
        except:
            print (traceback.format_exc())
            response["message_action"] = "REMOVE_CONFIG_ROLE_PRIVILEGE_FAILED"
            response["message_action"] = "REMOVE_CONFIG_ROLE_PRIVILEGE_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
# end class
