import sys
import traceback

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

sys.path.append("pytavia_modules/view" )

from flask          import render_template
from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config
from pytavia_core   import helper

from view import view_core_menu
from view import view_core_display
from view import view_core_header
from view import view_core_footer
from view import view_core_script
from view import view_core_css
from view import view_core_dialog_message

class view_users_edit_form:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def

    def _find_one_user(self, params):
        user_rec = self.mgdDB.db_user.find_one(
            {
                "pkey"  : params["fk_edit_user_id"]
            }
        )

        response = {
            "user_rec"   : user_rec
        }

        return response
    # end def

    def _find_role_position(self, params):
        query = {
            "config_type"   : "ROLE_POSITION",
            "is_deleted"    : False
        }

        if params["role_position"] != "SYSADMIN":
            query["value"] = {"$ne" : "SYSADMIN" }

        role_position_view = self.mgdDB.db_config.find(query)

        response = {
            "role_position_list"   : list(role_position_view)
        }

        return response
    # end def


    def html(self, params):
        response = helper.response_msg(
            "FIND_USER_EDIT_FORM_SUCCESS", "FIND USER EDIT FORM SUCCESS", {} , "0000"
        )
        try:
            menu_list_html         = view_core_menu.view_core_menu().html(params)
            core_display           = view_core_display.view_core_display().html(params)
            params["core_display"] = core_display         
            core_header            = view_core_header.view_core_header().html(params)
            core_footer            = view_core_footer.view_core_footer().html(params)
            core_script            = view_core_script.view_core_script().html(params)
            core_css               = view_core_css.view_core_css().html(params)
            core_dialog_message    = view_core_dialog_message.view_core_dialog_message().html(params)


            # FIND ONE USER
            user_resp              = self._find_one_user( params )
            user_rec               = user_resp["user_rec"       ]

            # FIND ROLE POSITION
            role_position_resp  = self._find_role_position( params )
            role_position_list  = role_position_resp["role_position_list"   ] 

           
            html = render_template(
                "users/users_edit_form.html",
                menu_list_html          = menu_list_html,
                core_display            = core_display,
                core_header             = core_header, 
                core_footer             = core_footer, 
                core_script             = core_script,  
                core_css                = core_css,
                core_dialog_message     = core_dialog_message,
                username                = params["username"      ],
                role_position           = params["role_position" ],
                redirect                = params["redirect"      ],
                user_rec                = user_rec,
                role_position_list      = role_position_list
            )

            response.put( "data", {
                    "html" : html
                }
            )


        except:
            trace_back_msg = traceback.format_exc() 
            print(trace_back_msg)
            self.webapp.logger.debug(trace_back_msg)
            response.put( "status"      , "FIND_USER_EDIT_FORM_FAILED" )
            response.put( "desc"        , "FIND USER EDIT FORM FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try

        return response
    # end def
    
# end class

