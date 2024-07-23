import config_core
import sys
import traceback
import json
import ast
import time
import random
import re

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib     import idgen
from pytavia_stdlib     import utils
from pytavia_core       import database
from pytavia_core       import config
from pytavia_core       import helper
from pytavia_stdlib     import cfs_lib
from xml.sax            import saxutils as su


class brutor_user_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def


    def _add(self, params):
        response = helper.response_msg(
            "ADD_USER_SUCCESS", "ADD USER SUCCESS", {} , "0000"
        )
        try:
            name                = params["name"                 ]
            username            = params["username"             ]
            password            = params["password"             ]
            role_position_value = params["role_position_value"  ]
            status_value        = params["status_value"         ]

            # CHECK IF USERNAME EXISTS
            username_rec = self.mgdDB.db_user.find_one(
                {
                    "username"  : username,
                    "status"    : "ACTIVE"
                }
            )

            if username_rec != None:
                response.put( "status"      , "ADD_USER_FAILED" )
                response.put( "desc"        , "Username sudah ada" )
                response.put( "status_code" , "1001" )
                response.put( "data"        , { "error_message" : "Username sudah ada" })
                return response

            hashed_password = utils._get_passwd_hash({
                "id"       : username,
                "password" : password
            })

            user_rec  = database.new(self.mgdDB, "db_user")
            user_rec.put("name",                name                )
            user_rec.put("username",            username            )
            user_rec.put("password",            hashed_password     )
            user_rec.put("role_position_value", role_position_value )
            user_rec.put("status",              status_value        )
            user_rec.insert()


        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "ADD_USER_FAILED" )
            response.put( "desc"        , "ADD USER FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def

    def _update_details(self, params):
        response = helper.response_msg(
            "UPDATE_USER_SUCCESS", "UPDATE USER SUCCESS", {} , "0000"
        )
        try:
            name                = params["name"                 ]
            username            = params["username"             ]
            role_position_value = params["role_position_value"  ]

            
            self.mgdDB.db_user.update_one(
                { "pkey" : params["fk_edit_user_id"] },
                { "$set" : {
                        "name"                  : name,
                        "username"              : username,
                        "role_position_value"   : role_position_value
                    }
                }
            )

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "UPDATE_USER_FAILED" )
            response.put( "desc"        , "UPDATE USER FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def

    def _toggle_status(self, params):
        response = helper.response_msg(
            "UPDATE_USER_STATUS_SUCCESS", "UPDATE USER STATUS SUCCESS", {} , "0000"
        )
        try:
            # if params["status"] == "ACTIVE":
            #     # CHECK IF EXISTING USERNAME
            #     username_rec = self.mgdDB.db_user.find_one(
            #         {
            #             "username"  : params["username"],
            #             "status"    : "ACTIVE"
            #         }
            #     )


                # if username_rec != None:
                #     response.put( "status"      , "ADD_USER_FAILED" )
                #     response.put( "desc"        , "Username sudah ada pada user aktif" )
                #     response.put( "status_code" , "1001" )
                #     response.put( "data"        , { "error_message" : "Username sudah ada pada user aktif" })
                #     return response

            # self.mgdDB.db_user.update_one(
            #     { "pkey" : params["fk_edit_user_id"] },
            #     { "$set" : {
            #             "status" : params["status"]
            #         }
            #     }
            # )

            self.mgdDB.db_user.delete_one(
                { "pkey" : params["fk_edit_user_id"] }
            )


            

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "UPDATE_USER_STATUS_FAILED" )
            response.put( "desc"        , "UPDATE USER STATUS FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def

    def _change_password(self, params):
        response = helper.response_msg(
            "UPDATE_USER_SUCCESS", "UPDATE USER SUCCESS", {} , "0000"
        )
        try:
            username = params["username"    ]
            password = params["password"    ]

            hashed_password = utils._get_passwd_hash({
                "id"       : username,
                "password" : password
            })

            
            self.mgdDB.db_user.update_one(
                { "pkey" : params["fk_edit_user_id"] },
                { "$set" : {
                        "password"  : hashed_password
                    }
                }
            )

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "UPDATE_USER_FAILED" )
            response.put( "desc"        , "UPDATE USER FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def

# end class
