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

class view_config_setting_menu:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self):
        pass
    # end def

    def show_menu_list(self, params):
        page_id = params["id"] if "id" in params else None
        value   = params["value"] if "value" in params else None
        isChkBox_state_setting_menu  = {
            "num_isChecked"     : "", 
            "lowCs_isChecked"   : "",
            "upCs_isChecked"    : "",
            "sym_isChecked"     : "",            
            "sym_str"     : ""
        }
        
        edit_item_rec = self.mgdDB.db_setting_app.find_one({})        
        if edit_item_rec == None:
            edit_item_rec = database.get_record("db_setting_app")
        # end if
        
        config_all_rec         = self.mgdDB.db_config_all.find_one({"value" : page_id})
        config_setting_menu    = self.mgdDB.db_setting_app.find_one({}) 
        
        if config_setting_menu :
            num_isChecked       = "checked" if config_setting_menu["variable_password"]["numeric"] != "FALSE" else ""
            lowCs_isChecked     = "checked" if config_setting_menu["variable_password"]["lower_case"] != "FALSE" else ""
            upCs_isChecked      = "checked" if config_setting_menu["variable_password"]["upper_case"] != "FALSE" else ""
            sym_isChecked       = "checked" if config_setting_menu["variable_password"]["symbol"] != "FALSE" else ""
            sym_str             = config_setting_menu["variable_password"]["symbol_str"] and config_setting_menu["variable_password"]["symbol_str"] or "" 
            isChkBox_state_setting_menu  = {
                "num_isChecked"     : num_isChecked , 
                "lowCs_isChecked"   : lowCs_isChecked,
                "upCs_isChecked"    : upCs_isChecked,
                "sym_isChecked"     : sym_isChecked,            
                "sym_str"           : sym_str                    
            }
        else:
            config_setting_menu = database.get_record("db_setting_app")
        
        response = {
            "config_setting_menu"           : config_setting_menu,
            "isChkBox_state_setting_menu"   : isChkBox_state_setting_menu ,
            "edit_item_rec"                 : edit_item_rec       ,
            "config_all_rec"                : config_all_rec
        }
        return response
    # end def

    def html(self, params):
        menu_list                   = view_core_menu.view_core_menu().html(params)
        core_display                = view_core_display.view_core_display().html(params)
        params["core_display"]      = core_display         
        core_header                 = view_core_header.view_core_header().html(params)
        core_footer                 = view_core_footer.view_core_footer().html(params)
        core_script                 = view_core_script.view_core_script().html(params)
        core_css                    = view_core_css.view_core_css().html(params)
        core_dialog_message         = view_core_dialog_message.view_core_dialog_message().html(params)
        show_menu_data              = self.show_menu_list( params )
        config_setting_menu         = show_menu_data["config_setting_menu"         ] 
        isChkBox_state_setting_menu = show_menu_data["isChkBox_state_setting_menu" ] 
        edit_item_rec               = show_menu_data["edit_item_rec"               ] 
        config_all_rec              = show_menu_data["config_all_rec"              ] 
        return render_template(
            "system-setting/setting-list.html",
            isChkBox_state_setting_menu = isChkBox_state_setting_menu,
            menu_list_html      = menu_list,
            config_setting_menu = config_setting_menu ,
            edit_item_rec       = edit_item_rec,
            config_all_rec      = config_all_rec,
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
