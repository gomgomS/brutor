import sys
import traceback
import time
import json
import datetime
import statistics
from bson import Int64

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )
sys.path.append("pytavia_modules/view" )

from flask          import render_template
from flask          import session
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

class view_profile:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    # FIND DATA USER ACTIVE ------------------THIS NEW DELETE THIS COMMENT AFTER YOU BACK
    def _data_user(self):      
        user_uuid   = session["user_uuid"]
        query = { "user_uuid": user_uuid}
        user = self.mgdDB.db_user.find_one(query)     
        # data_user = user['ver_email']          

        return user
       

    def html(self, params):
        menu_list               = view_core_menu.view_core_menu().html(params)
        core_display            = view_core_display.view_core_display().html(params)
        params["core_display"]  = core_display         
        core_header             = view_core_header.view_core_header().html(params)
        core_footer             = view_core_footer.view_core_footer().html(params)
        core_script             = view_core_script.view_core_script().html(params)
        core_css                = view_core_css.view_core_css().html(params)
        core_dialog_message     = view_core_dialog_message.view_core_dialog_message().html(params)

        data_user         = self._data_user()                          

        return render_template(
            "profile/profile.html",
            menu_list_html      = menu_list               ,
            core_display        = core_display            , 
            core_header         = core_header             , 
            core_footer         = core_footer             , 
            core_script         = core_script             , 
            core_css            = core_css                , 
            core_dialog_message = core_dialog_message     ,
            username            = params["username"      ],
            role_position       = params["role_position" ],

            data_user  = data_user

           # users_total         = users_total,
            
        )                
    # end def
# end class
