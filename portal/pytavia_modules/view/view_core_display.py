import sys
import traceback
import pymongo

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config

from flask import session

class view_core_display:
   
    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self):
        pass
    # end def

    def core_display(self, params):
        core_css_rec = self.mgdDB.db_config_general.find_one({
            "value" : "DISPLAY_CORE_CSS_FILE"
        })
        component_css_rec = self.mgdDB.db_config_general.find_one({
            "value" : "DISPLAY_COMPONENT_CSS_FILE"
        })
        logo_rec = self.mgdDB.db_config_general.find_one({
            "value" : "DISPLAY_MAIN_LOGO"
        })
        copyright_text_rec = self.mgdDB.db_config_general.find_one({
            "value" : "DISPLAY_COPYRIGHT_TEXT"
        })
        response = {
            "core_css"      : core_css_rec      ["misc"],
            "components_css": component_css_rec ["misc"],
            "logo_image"    : logo_rec          ["misc"],
            "copyright_text": copyright_text_rec["misc"]
        }
        return response
    # end def

    """
        Later as part of these params object
        we need to see who the user is and render based on that.
        This is the new application
    """
    def html(self, params):
        core_display_map = self.core_display( params )
        return core_display_map
    # end def

# end class
