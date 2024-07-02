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

class config_menu_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def


    def _add(self, params):
        response = helper.response_msg(
            "ADD_MENU_SUCCESS", "ADD MENU SUCCESS", {} , "0000"
        )
        try:
            print("ENTER ADD FUNCTION")
            
            menu_rec  = database.new(self.mgdDB, "db_menu")
            menu_rec.put("menu_name",   params["menu_name"      ])
            menu_rec.put("value",       params["value"          ])
            menu_rec.put("icon_class",  params["icon_class"     ])
            menu_rec.put("url",			params["url"            ])
            menu_rec.put("position",    int(params["position"   ]))
            menu_rec.put("desc",        params["desc"           ])
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
            
            self.mgdDB.db_menu.update(
                {"pkey" : params["fk_menu_id"]},
                {"$set" : {
                    "menu_name"     : params["menu_name"    ],
                    "value"         : params["value"        ],
                    "icon_class"    : params["icon_class"   ],
                    "url"           : params["url"          ],
                    "position"      : int(params["position" ]),
                    "desc"          : params["desc"         ]
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
            
            self.mgdDB.db_menu.delete_one(
                { "pkey" : params["fk_menu_id"] },
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
