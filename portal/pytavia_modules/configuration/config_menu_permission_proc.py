import config_core
import sys
import traceback
import requests
import json
import ast

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib   import idgen
from pytavia_stdlib   import utils
from pytavia_core     import database
from pytavia_core     import config
from pytavia_core     import helper

class config_menu_permission_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def


    def _add(self, params):
        response = helper.response_msg(
            "ADD_MENU_SUCCESS", "ADD MENU SUCCESS", {} , "0000"
        )

        try:

            
            menu_rec  = database.new(self.mgdDB, "db_menu_permission")
            menu_rec.put("role_position_value", params["role_position_value"    ])
            menu_rec.put("menu_value",          params["menu_value"             ])
            menu_rec.put("desc",                params["desc"                   ])
            menu_rec.insert()



        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "ADD_MENU_FAILED" )
            response.put( "desc"        , "ADD MENU FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def
    
    def _update(self, params):
        response = helper.response_msg(
            "UPDATE_MENU_SUCCESS", "UPDATE MENU SUCCESS", {} , "0000"
        )

        try:
            
            self.mgdDB.db_menu_permission.update(
                {"pkey" : params["fk_menu_permission_id"]},
                {"$set" : {
                    "role_position_value"   : params["role_position_value"  ],
                    "menu_value"            : params["menu_value"           ],
                    "desc"                  : params["desc"                 ]
                }
            })



        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "UPDATE_MENU_FAILED" )
            response.put( "desc"        , "UPDATE MENU FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def

    def _delete(self, params):
        response = helper.response_msg(
            "DELETE_MENU_SUCCESS", "DELETE MENU SUCCESS", {} , "0000"
        )

        try:
            
            self.mgdDB.db_menu_permission.delete_one(
                { "pkey" : params["fk_menu_permission_id"] },
            )

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "DELETE_MENU_FAILED" )
            response.put( "desc"        , "DELETE MENU FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def



    

# end class
