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

class view_config_menu_permission:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def

    def _find_role_position(self, params):
        query = { 
            "config_type"   : "ROLE_POSITION",
            "is_deleted"    : False
        }

        #tidak memasukan sysadmin
        if params["role_position"] != "SYSADMIN":
            query["value"] = {"$ne" : "SYSADMIN" }

        role_position_view = self.mgdDB.db_config.find(query)

        response = {
            "role_position_list"   : list(role_position_view)
        }
        return response
    # end def

    def _find_menu(self, params):
        query = { 
            "is_deleted" : False 
        }

        menu_view = self.mgdDB.db_menu.find(query)

        response = {
            "menu_list"   : list(menu_view)
        }
        return response
    # end def

    def _find_menu_permission(self, params):
        query = { 
            "is_deleted" : False 
        }

        if params["role_position"] != "SYSADMIN":
            query["role_position_value"] = {"$ne" : "SYSADMIN" }

        menu_permission_view = self.mgdDB.db_menu_permission.find(query)

        response = {
            "menu_permission_list"   : list(menu_permission_view)
        }
        return response
    # end def

    
    def html(self, params):
        response = helper.response_msg(
                "FIND_MENU_PERMISSION_SUCCESS", "FIND MENU PERMISSION SUCCESS", {} , "0000"
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


            # FIND MENU PERMISSION
            menu_permission_resp    = self._find_menu_permission( params )
            menu_permission_list    = menu_permission_resp["menu_permission_list"   ]

            # FIND ROLE POSITION
            role_position_resp      = self._find_role_position( params )
            role_position_list      = role_position_resp["role_position_list"       ]

            # FIND MENU
            menu_resp               = self._find_menu( params )
            menu_list               = menu_resp["menu_list"   ]


            html = render_template(
                "configuration/config_menu_permission.html",
                menu_list_html          = menu_list_html,
                core_display            = core_display,
                core_header             = core_header, 
                core_footer             = core_footer, 
                core_script             = core_script,  
                core_css                = core_css,
                core_dialog_message     = core_dialog_message,
                username                = params["username"      ],
                role_position           = params["role_position" ],
                menu_permission_list    = menu_permission_list,
                role_position_list      = role_position_list,
                menu_list               = menu_list
            )

            response.put( "data", {
                    "html" : html
                }
            )

        except:
            trace_back_msg = traceback.format_exc() 
            print(trace_back_msg)
            self.webapp.logger.debug(trace_back_msg)
            response.put( "status"      , "FIND_MENU_PERMISSION_FAILED" )
            response.put( "desc"        , "FIND MENU PERMISSION FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try

        return response
    # end def
    
# end class

