import sys
import traceback
import requests
import ast
import json

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

from view import view_core_menu
from view import view_core_display
from view import view_core_header
from view import view_core_footer
from view import view_core_script
from view import view_core_css
from view import view_core_dialog_message

from collections import deque

class view_error_page:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app    
    # end def

    
    def html(self, params):
        response = {
            "message_action"    : "VIEW_ERROR_PAGE_SUCCESS",
            "message_desc"      : "",
        }

        

        menu_list              = view_core_menu.view_core_menu().html(params)
        core_display           = view_core_display.view_core_display().html(params)
        params["core_display"] = core_display         
        core_header            = view_core_header.view_core_header().html(params)
        core_footer            = view_core_footer.view_core_footer().html(params)
        core_script            = view_core_script.view_core_script().html(params)
        core_css               = view_core_css.view_core_css().html(params)
        core_dialog_message    = view_core_dialog_message.view_core_dialog_message().html(params)
        username               = params["username"          ]
        role_position          = params["role_position"     ]
        message_action         = params["message_action"    ]
        message_desc           = params["message_desc"      ]
        redirect               = params["redirect"          ]


        html = render_template(
            "error-page/error_page.html",
            menu_list_html      = menu_list,
            core_display        = core_display,
            core_header         = core_header, 
            core_footer         = core_footer, 
            core_script         = core_script,  
            core_css            = core_css,
            core_dialog_message = core_dialog_message,
            username            = username,
            role_position       = role_position,
            message_action      = message_action,
            message_desc        = message_desc,
            redirect            = redirect
        )            

        response["html"] = html
        return response
    # end def

# end class
