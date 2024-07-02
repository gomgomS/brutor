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

class view_core_header:

    def __init__(self):
        pass
    # end def
    
    def html(self, params):
        core_display = params["core_display"]        
        return render_template(
            "core/header.html",
            core_display = core_display
        )
    # end def
# end class
