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

from collections import deque

class view_config_owner:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self):
        pass
    #enddef

    def show_menu_list(self, params):
        #prepare params
        page_id         = params["id"] if "id" in params else 'CONFIG_OWNER'
        pkey            = params["pkey"] if "pkey" in params else None
        
        #get config all
        config_all_rec   = self.mgdDB.db_config_all.find_one({"value" : page_id})
        
        #get edit rec
        edit_item_rec   = None
        if pkey != None:
            edit_item_rec = self.mgdDB.db_config_vessel_owner.find_one({
                "pkey" : pkey
            })
        #endif
        
        #get data list
        config_data_list = self.mgdDB.db_config_vessel_owner.find({})
        
        #response
        response = {
            "config_all_rec"   : config_all_rec,
            "config_data_list" : config_data_list,
            "edit_item_rec"    : edit_item_rec,
        }
        return response
    #enddef

    def html(self, params):
        menu_list               = view_core_menu.view_core_menu().html(params)
        core_display            = view_core_display.view_core_display().html(params)
        params["core_display"]  = core_display         
        core_header             = view_core_header.view_core_header().html(params)
        core_footer             = view_core_footer.view_core_footer().html(params)
        core_script             = view_core_script.view_core_script().html(params)
        core_css                = view_core_css.view_core_css().html(params)
        core_dialog_message     = view_core_dialog_message.view_core_dialog_message().html(params)
        show_menu_data          = self.show_menu_list( params )
        config_all_rec          = show_menu_data["config_all_rec"]
        config_data_list        = show_menu_data["config_data_list"] 
        edit_item_rec           = show_menu_data["edit_item_rec"]
        return render_template(
            "configuration/owner.html",
            menu_list_html      = menu_list,
            config_all_rec      = config_all_rec,
            config_data_list    = config_data_list,
            edit_item_rec       = edit_item_rec,
            core_display        = core_display,
            core_header         = core_header, 
            core_footer         = core_footer, 
            core_script         = core_script,  
            core_css            = core_css,
            core_dialog_message = core_dialog_message,
            username            = params["username"],
            role_position       = params["role_position"]
        )                
    #enddef
#endclass