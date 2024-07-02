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

class config_menu_webapp_item_all(config_core.config_core):

    mgdDB = database.get_db_conn(config.mainDB)

    def __ini__(self):
        config_core.config_core.__init__(self)
    # end def

    def update(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "ADD_MENU_CONFIG_ITEM_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            name   = params["name"  ]
            value  = params["value" ]
            order  = params["order" ]
            status = params["status"]
            href   = params["href"  ]
            icon   = params["icon"  ]
            desc   = params["desc"  ]

            order = int(order)
            config_web_menu_rec = database.get_record("db_config_menu_webapp_item_all")
            config_web_menu_rec["name"  ] = name
            config_web_menu_rec["value" ] = value
            config_web_menu_rec["order" ] = order
            config_web_menu_rec["status"] = status
            config_web_menu_rec["href"  ] = href
            config_web_menu_rec["icon"  ] = icon
            config_web_menu_rec["desc"  ] = desc
            config_web_menu_check = self.mgdDB.db_config_menu_webapp_item_all.find_one({
                "value" : value
            })
            if config_web_menu_check == None:
                self.mgdDB.db_config_menu_webapp_item_all.insert( config_web_menu_rec )
            else:
                self.mgdDB.db_config_menu_webapp_item_all.update(
                    {"value" : value},
                    {"$set"  : {
                        "name"  : name  ,
                        "value" : value ,
                        "order" : order ,
                        "status": status,
                        "href"  : href  ,
                        "icon"  : icon  ,
                        "desc"  : desc
                    }}
                )
            # end if
            item_count = self.mgdDB.db_config_menu_webapp_item_all.find({}).count()
            self.mgdDB.db_config_all.update(
                {"value" : "WEBAPP_MENU_ALL_ITEMS"},
                {"$set"  : {"count" : item_count }}
            )
        except :
            print (traceback.format_exc())
            response["message_action"] = "ADD_MENU_CONFIG_ITEM_FAILED"
            response["message_action"] = "ADD_MENU_CONFIG_ITEM_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def

    def remove(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "REMOVE_MENU_CONFIG_ITEM_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            value = params["value"]
            self.mgdDB.db_config_menu_webapp_item_all.remove({ "value" : value })
        except:
            print (traceback.format_exc())
            response["message_action"] = "REMOVE_MENU_CONFIG_ITEM_FAILED"
            response["message_action"] = "REMOVE_MENU_CONFIG_ITEM_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
# end class

