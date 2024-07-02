import sys
import traceback
import time
import json
import datetime

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

class view_core_dialog_message:

    def __init__(self):
        pass
    # end def
    
    def html(self, params):
        core_display = params["core_display"]
        message      = None
        message_data = None
        
        if "message" in params:
            message_data = params["message_data"]            
        #end if 
        
        return render_template(
            "core/dialog_message.html",
            core_display = core_display,
            message      = message,
            message_data = message_data
        )
    # end def
# end class
