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

class view_general_config:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def

    def _find_config(self, params):
        config_type = params["config_type"]
        
        query = { 
            "config_type"   : config_type, 
            "is_deleted"    : False 
        }

        if config_type == "ROLE_POSITION" and params["role_position"] != "SYSADMIN":
            query["value"] = { "$ne" : "SYSADMIN" }

        config_view = self.mgdDB.db_config.find(query)
        config_title = utils._get_title(config_type)

        response = {
            "config_list"   : list(config_view),
            "config_title"  : config_title
        }

        return response
    # end def

    
    def html(self, params):
        response = helper.response_msg(
            "FIND_CONFIG_SUCCESS", "FIND CONFIG SUCCESS", {} , "0000"
        )
        try:
            menu_list              = view_core_menu.view_core_menu().html(params)
            core_display           = view_core_display.view_core_display().html(params)
            params["core_display"] = core_display         
            core_header            = view_core_header.view_core_header().html(params)
            core_footer            = view_core_footer.view_core_footer().html(params)
            core_script            = view_core_script.view_core_script().html(params)
            core_css               = view_core_css.view_core_css().html(params)
            core_dialog_message    = view_core_dialog_message.view_core_dialog_message().html(params)


            config_resp             = self._find_config( params )
            config_list             = config_resp["config_list"     ] 
            config_title            = config_resp["config_title"    ] 


            html = render_template(
                "configuration/general_config.html",
                menu_list_html      = menu_list,
                core_display        = core_display,
                core_header         = core_header, 
                core_footer         = core_footer, 
                core_script         = core_script,  
                core_css            = core_css,
                core_dialog_message = core_dialog_message,
                username            = params["username"      ],
                role_position       = params["role_position" ],
                config_list         = config_list,
                config_title        = config_title,
                config_type         = params["config_type"]
            )

            response.put( "data", {
                    "html" : html
                }
            )

        except:
            trace_back_msg = traceback.format_exc() 
            print(trace_back_msg)
            self.webapp.logger.debug(trace_back_msg)
            response.put( "status"      , "FIND_CONFIG_FAILED" )
            response.put( "desc"        , "FIND CONFIG FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try

        return response
    # end def
    
# end class

