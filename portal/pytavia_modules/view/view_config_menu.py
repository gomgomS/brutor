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

class view_config_menu:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def

    def _find_menu(self, params):

        menu_list = []
        menu_view = self.mgdDB.db_menu.find({ "is_deleted" : False })
        for menu_item in menu_view:
            menu_list.append(menu_item)


        response = {
            "menu_list"   : menu_list
        }

        return response
    # end def

    
    def html(self, params):
        response = helper.response_msg(
            "FIND_CONFIG_MENU_SUCCESS", "FIND CONFIG MENU SUCCESS", {} , "0000"
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


            # FIND MENU
            menu_resp             = self._find_menu( params )
            menu_list             = menu_resp["menu_list"     ] 


            html = render_template(
                "configuration/config_menu.html",
                menu_list_html      = menu_list_html,
                core_display        = core_display,
                core_header         = core_header, 
                core_footer         = core_footer, 
                core_script         = core_script,  
                core_css            = core_css,
                core_dialog_message = core_dialog_message,
                username            = params["username"      ],
                role_position       = params["role_position" ],
                menu_list           = menu_list
            )

            response.put( "data", {
                    "html" : html
                }
            )
        except:
            trace_back_msg = traceback.format_exc() 
            print(trace_back_msg)
            self.webapp.logger.debug(trace_back_msg)
            response.put( "status"      , "FIND_CONFIG_MENU_FAILED" )
            response.put( "desc"        , "FIND CONFIG MENU FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try

        return response
    # end def
    
# end class

