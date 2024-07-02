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

class config_setting_menu(config_core.config_core):

    mgdDB = database.get_db_conn(config.mainDB)

    def __ini__(self):
        config_core.config_core.__init__(self)
    # end def

    def update(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "ADD_CONFIG_MENU_SETTING_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "set_security",
            "message_data"   : {}
        }
        try:
            idle_account                = params["idle_account"      ]
            force_change_password       = params["force_change_password"     ]
            password_history            = params["password_history"     ]
            password_length             = params["password_length"    ]
            numeric                     =  "TRUE" if  "numeric" in params     else "FALSE"
            lower_case                  =  "TRUE" if  "lower_case" in params  else "FALSE"
            upper_case                  =  "TRUE" if  "upper_case" in params  else "FALSE"
            symbol_str                  =   params["symbol_str"      ] 
            symbol                      =   "TRUE" if "symbol" in params     else "FALSE"
            wrong_counter               = params["wrong_counter"      ]
            screen_timeout              = params["screen_timeout"]
            tran_timeout                = params["tran_timeout"  ]
            count_db_setting_security_app = self.mgdDB.db_setting_app.find_one({})
            variable_password = {
                        "numeric"    : numeric,
                        "lower_case"  : lower_case,
                        "upper_case" : upper_case,
                        "symbol_str" : symbol_str,
                        "symbol"     : symbol  }
                        
            if count_db_setting_security_app == None:
                setting_security_app_rec = database.get_record("db_setting_app")                
                setting_security_app_rec["idle_account"               ] = idle_account
                setting_security_app_rec["force_change_password"      ] = force_change_password
                setting_security_app_rec["password_history"           ] = password_history
                setting_security_app_rec["password_length"            ] = password_length
                setting_security_app_rec["wrong_counter"              ] = wrong_counter
                setting_security_app_rec["variable_password"          ] = variable_password
                setting_security_app_rec["screen_timeout"             ] = screen_timeout
                setting_security_app_rec["tran_timeout"               ] = tran_timeout
                self.mgdDB.db_setting_app.insert( setting_security_app_rec )
            else:
                self.mgdDB.db_setting_app.update(
                    { "_id" : count_db_setting_security_app["_id"] },
                    { "$set"  : {
                        "idle_account"               : idle_account       ,
                        "force_change_password"      : force_change_password      ,
                        "password_history"           : password_history      ,
                        "password_length"            : password_length     ,
                        "wrong_counter"              : wrong_counter   ,
                        "variable_password"          : variable_password ,
                        "screen_timeout"             : screen_timeout ,
                        "tran_timeout"               : tran_timeout ,
                    }}
                )
            # end if
            item_count = self.mgdDB.db_setting_app.find({}).count()
            self.mgdDB.db_config_all.update(
                {"value" : "CONF_MENU_SETTING"},
                {"$set"  : {"count" : item_count }}
            )
        except :
            print (traceback.format_exc())
            response["message_action"] = "ADD_CONFIG_MENU_SETTING_FAILED"
            response["message_action"] = "ADD_CONFIG_MENU_SETTING_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
    
