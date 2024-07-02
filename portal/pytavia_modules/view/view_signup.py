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

from view import view_core_display
from view import view_core_script
from view import view_core_css
from view import view_core_dialog_message

class view_signup:

    def __init__(self):
        pass
    # end def

    def html(self, params):
        core_display = view_core_display.view_core_display().html( params )
        params["core_display"]  = core_display         
        core_script             = view_core_script.view_core_script().html(params)
        core_css                = view_core_css.view_core_css().html(params)
        core_dialog_message     = view_core_dialog_message.view_core_dialog_message().html(params)
        return render_template(
            "auth/signup.html", 
            core_script         = core_script         , 
            core_css            = core_css            , 
            core_dialog_message = core_dialog_message , 
            core_display        = core_display
        )                
    # end def

# end class
