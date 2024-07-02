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

class config_starter_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def


    def _add(self, params):
        response = helper.response_msg(
            "ADD_STARTER_BUTTON_SUCCESS", "ADD STARTER BUTTON SUCCESS", {} , "0000"
        )
        try:

            
            menu_rec  = database.new(self.mgdDB, "db_starter")
            menu_rec.put("menu_value",          params["menu_value"             ])
            menu_rec.put("name" ,               params["name"                   ])
            menu_rec.put("value",               params["value"                  ])
            menu_rec.put("icon_class",          params["icon_class"             ])
            menu_rec.put("url",			        params["url"                    ])
            menu_rec.put("position",            int(params["position"           ]))
            menu_rec.put("desc",                params["desc"                   ])
            menu_rec.insert()


        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "ADD_STARTER_BUTTON_FAILED" )
            response.put( "desc"        , "ADD STARTER BUTTON FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def
    
    def _update(self, params):
        response = helper.response_msg(
            "UPDATE_STARTER_BUTTON_SUCCESS", "UPDATE STARTER BUTTON SUCCESS", {} , "0000"
        )
        try:
            
            self.mgdDB.db_starter.update(
                {"pkey" : params["fk_starter_id"]},
                {"$set" : {
                    "menu_value"            : params["menu_value"           ],
                    "name"                  : params["name"                 ],
                    "value"                 : params["value"                ],
                    "icon_class"            : params["icon_class"           ],
                    "url"                   : params["url"                  ],
                    "position"              : int(params["position"         ]),
                    "desc"                  : params["desc"                 ]
                }
            })



        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "UPDATE_STARTER_BUTTON_FAILED" )
            response.put( "desc"        , "UPDATE STARTER BUTTON FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def

    def _delete(self, params):
        response = helper.response_msg(
            "DELETE_STARTER_BUTTON_SUCCESS", "DELETE STARTER BUTTON SUCCESS", {} , "0000"
        )
        try:
            
            self.mgdDB.db_starter.delete_one(
                { "pkey" : params["fk_starter_id"] },
            )

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "DELETE_STARTER_BUTTON_FAILED" )
            response.put( "desc"        , "DELETE STARTER BUTTON FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def


# end class
