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

class view_config_notif_event:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def

    def _find_channel(self, params):
        channel_view = self.mgdDB.db_config.find(
            { 
                "config_type"   : "CHANNEL", 
                "is_deleted"    : False,
                "value"         : {
                    "$nin" : [ "PERSONAL", "EVENT_REMINDER" ]
                }
            },
            { 
                "_id"   : 0, 
                "name"  : 1, 
                "value" : 1,
                "desc"  : 1
            }
        )

        response = {
            "channel_list"   : list(channel_view)
        }
        return response
    # end def

    def _find_event(self, params):
        event_view = self.mgdDB.db_notif_event.find({ "is_deleted" : False })

        response = {
            "event_list"   : list(event_view)
        }
        return response
    # end def


    def html(self, params):
        response = helper.response_msg(
            "FIND_CONFIG_STARTER_SUCCESS", "FIND CONFIG STARTER SUCCESS", {} , "0000"
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


            # FIND CHANNEL
            channel_resp            = self._find_channel( params )
            channel_list            = channel_resp["channel_list"     ] 

            # FIND EVENT
            event_resp             = self._find_event( params )
            event_list             = event_resp["event_list"     ] 


            html = render_template(
                "configuration/config_notif_event.html",
                menu_list_html      = menu_list_html,
                core_display        = core_display,
                core_header         = core_header, 
                core_footer         = core_footer, 
                core_script         = core_script,  
                core_css            = core_css,
                core_dialog_message = core_dialog_message,
                username            = params["username"      ],
                role_position       = params["role_position" ],
                channel_list           = channel_list,
                event_list= event_list
            )

            response.put( "data", {
                    "html" : html
                }
            )

        except:
            trace_back_msg = traceback.format_exc() 
            print(trace_back_msg)
            self.webapp.logger.debug(trace_back_msg)
            response.put( "status"      , "FIND_CONFIG_STARTER_FAILED" )
            response.put( "desc"        , "FIND CONFIG STARTER FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try

        return response
    # end def
    
# end class

