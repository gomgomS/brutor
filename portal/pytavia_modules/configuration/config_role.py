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

class config_role(config_core.config_core):

    mgdDB = database.get_db_conn(config.mainDB)

    def __ini__(self):
        config_core.config_core.__init__(self)
    # end def

    def update(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "ADD_CONFIG_ROLE_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            name   = params["name"      ]
            value  = params["value"     ]
            order  = params["order"     ]
            status = params["status"    ]
            utype  = params["user_type" ]
            misc   = params["misc"      ]
            desc   = params["desc"      ]

            order = int(order)
            config_role_rec = database.get_record("db_config_role")
            config_role_rec["name"      ] = name
            config_role_rec["value"     ] = value
            config_role_rec["order"     ] = order
            config_role_rec["status"    ] = status
            config_role_rec["user_type" ] = utype            
            config_role_rec["misc"      ] = misc
            config_role_rec["desc"      ] = desc
            config_role_check = self.mgdDB.db_config_role.find_one({
                "value" : value
            })
            if config_role_check == None:
                self.mgdDB.db_config_role.insert( config_role_rec )
            else:
                self.mgdDB.db_config_role.update(
                    {"value" : value},
                    {"$set"  : {
                        "name"      : name   ,
                        "value"     : value  ,
                        "order"     : order  ,
                        "status"    : status ,
                        "user_type" : utype  ,
                        "misc"      : misc   ,
                        "desc"      : desc   ,
                    }}
                )
            # end if
            item_count = self.mgdDB.db_config_role.find({}).count()
            self.mgdDB.db_config_all.update(
                {"value" : "USER_ROLE"},
                {"$set"  : {"count" : item_count }}
            )
        except :
            print (traceback.format_exc())
            response["message_action"] = "ADD_CONFIG_ROLE_FAILED"
            response["message_action"] = "ADD_CONFIG_ROLE_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def

    def remove(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "REMOVE_CONFIG_ROLE_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            value = params["value"]
            self.mgdDB.db_config_role.remove({ "value" : value })
            item_count = self.mgdDB.db_config_role.find({}).count()
            self.mgdDB.db_config_all.update(
                {"value" : "USER_ROLE"},
                {"$set"  : {"count" : item_count }}
            )
        except:
            print (traceback.format_exc())
            response["message_action"] = "REMOVE_CONFIG_ROLE_FAILED"
            response["message_action"] = "REMOVE_CONFIG_ROLE_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
# end class
