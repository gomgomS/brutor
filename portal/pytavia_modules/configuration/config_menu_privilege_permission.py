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

class config_menu_privilege_permission(config_core.config_core):

    mgdDB = database.get_db_conn(config.mainDB)

    def __ini__(self):
        config_core.config_core.__init__(self)
    # end def

    def update(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "ADD_CONFIG_MENU_PRIVILEGE_PERMISSION_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            name      = params["name"     ]
            value     = params["value"    ]
            status    = params["status"   ]
            privilege = params["privilege"]
            menu      = params["menu"     ]

            config_menu_privilege_rec = database.get_record("db_config_webapp_menu_privilege")
            config_menu_privilege_rec["name"           ] = name
            config_menu_privilege_rec["value"          ] = value
            config_menu_privilege_rec["status"         ] = status
            config_menu_privilege_rec["fk_privilege_id"] = privilege
            config_menu_privilege_rec["fk_menu_id"     ] = menu
            config_menu_privilege_check = self.mgdDB.db_config_webapp_menu_privilege.find_one({
                "value" : value
            })
            if config_menu_privilege_check == None:
                self.mgdDB.db_config_webapp_menu_privilege.insert( config_menu_privilege_rec )
            else:
                self.mgdDB.db_config_webapp_menu_privilege.update(
                    {"value" : value},
                    {"$set"  : {
                        "name"            : name      ,
                        "value"           : value     ,
                        "status"          : status    ,
                        "fk_privilege_id" : privilege ,
                        "fk_menu_id"      : menu      , 
                    }}
                )
            # end if
            item_count = self.mgdDB.db_config_webapp_menu_privilege.find({}).count()
            self.mgdDB.db_config_all.update(
                {"value" : "SYSTEM_MENU_PERMISSION"},
                {"$set"  : {"count" : item_count  }}
            )
        except :
            print (traceback.format_exc())
            response["message_action"] = "ADD_CONFIG_MENU_PRIVILEGE_PERMISSION_FAILED"
            response["message_action"] = "ADD_CONFIG_MENU_PRIVILEGE_PERMISSION_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def

    def remove(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "REMOVE_CONFIG_MENU_PRIVILEGE_PERMISSION_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            value = params["value"]
            self.mgdDB.db_config_webapp_menu_privilege.remove({ "value" : value })
            item_count = self.mgdDB.db_config_webapp_menu_privilege.find({}).count()
            self.mgdDB.db_config_all.update(
                {"value" : "SYSTEM_MENU_PERMISSION"},
                {"$set"  : {"count" : item_count  }}
            )
        except:
            print (traceback.format_exc())
            response["message_action"] = "REMOVE_CONFIG_MENU_PRIVILEGE_PERMISSION_FAILED"
            response["message_action"] = "REMOVE_CONFIG_MENU_PRIVILEGE_PERMISSION_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
# end class

