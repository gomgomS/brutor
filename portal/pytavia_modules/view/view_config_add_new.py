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

from view import view_core_menu
from view import view_core_display
from view import view_core_header
from view import view_core_footer
from view import view_core_script
from view import view_core_css
from view import view_core_dialog_message

class view_config_add_new:

    def __init__(self):
        pass
    # end def

    def html(self, params):
        menu_list              = view_core_menu.view_core_menu().html(params)
        core_display           = view_core_display.view_core_display().html(params)
        params["core_display"] = core_display         
        core_header            = view_core_header.view_core_header().html(params)
        core_footer            = view_core_footer.view_core_footer().html(params)
        core_script            = view_core_script.view_core_script().html(params)
        core_css               = view_core_css.view_core_css().html(params)
        core_dialog_message    = view_core_dialog_message.view_core_dialog_message().html(params)
        return render_template(
            "config/config-add.html",
            menu_list_html      = menu_list,
            core_display        = core_display,
            core_header         = core_header, 
            core_footer         = core_footer, 
            core_script         = core_script,  
            core_css            = core_css,
            core_dialog_message = core_dialog_message,
            username            = params["username"      ],
            role_position       = params["role_position" ]
        )                
    # end def

# end class
