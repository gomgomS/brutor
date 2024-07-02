import sys
import traceback
import pymongo

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

class view_config:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self):
        pass
    # end def




    # FIND CONFIG LIST
    def _find_config(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_data"   : {}
        }


        config_all_list = []

        # IF USER IS ADMIN SHOW 
        if params["role"] == "ADMIN":
        
            # ADD MENU CONFIG
            config_all_list.append({
                "config_title"  : "Menu",
                "description"   : "Sidebar Menu",
                "url"           : "/configuration/menu",
                "count"         : str(self.mgdDB.db_menu.count())
            })

            # ADD MENU PERMISSION CONFIG
            config_all_list.append({
                "config_title"  : "Menu Permission",
                "description"   : "Role Position Menu Permission",
                "url"           : "/configuration/menu_permission",
                "count"         : str(self.mgdDB.db_menu_permission.count())
            })

            # ADD CONFIG STARTER
            config_all_list.append({
                "config_title"  : "Config Starter",
                "description"   : "Show config Starter button",
                "url"           : "/configuration/starter",
                "count"         : str(self.mgdDB.db_starter.count())
            })

            # ADD LEVEL CLASS
            config_all_list.append({
                "config_title"  : "Level Class",
                "description"   : "Level Class List",
                "url"           : "/configuration/level_class",
                "count"         : str(self.mgdDB.level_class.find({"is_deleted" : False }).count())
            })

            # # ADD TERMS AND CONDITIONS
            # config_all_list.append({
            #     "config_title"  : "Terms and Conditions",
            #     "description"   : "Terms and Conditions List",
            #     "url"           : "/configuration/terms_and_conditions",
            #     "count"         : str(self.mgdDB.db_terms_and_conditions.find({"is_deleted" : False }).count())
            # })

            # # ADD NOTIF EVENT
            # config_all_list.append({
            #     "config_title"  : "Notification Event",
            #     "description"   : "Notification Event List",
            #     "url"           : "/configuration/notif_event",
            #     "count"         : str(self.mgdDB.db_notif_event.find({"is_deleted" : False }).count())
            # })

            


            # FIND BASIC CONFIG
            config_list = []
            config_view = self.mgdDB.db_config.aggregate([
                { "$match" : { "is_deleted" : False }},
                { "$group" : { "_id": "$config_type", "count":{"$sum":1} }}
                ])

            for config_item in config_view:
                config_item["config_title"  ] = utils._get_title(config_item["_id"])
                config_item["url"           ] = "/configuration/general_config?config_type=" + config_item["_id"]
                config_list.append(config_item)
        
        # else:
        #     print("rerrr")

        #     # ADD TERMS AND CONDITIONS
        #     config_all_list.append({
        #         "config_title"  : "Terms and Conditions",
        #         "description"   : "Terms and Conditions List",
        #         "url"           : "/configuration/terms_and_conditions",
        #         "count"         : str(self.mgdDB.db_terms_and_conditions.find({"is_deleted" : False }).count())
        #     })

        #     # ADD NOTIF EVENT
        #     config_all_list.append({
        #         "config_title"  : "Notification Event",
        #         "description"   : "Notification Event List",
        #         "url"           : "/configuration/notif_event",
        #         "count"         : str(self.mgdDB.db_notif_event.find({"is_deleted" : False }).count())
        #     })

        #     # ADD MENU PERMISSION CONFIG
        #     config_all_list.append({
        #         "config_title"  : "Menu Permission",
        #         "description"   : "Role Position Menu Permission",
        #         "url"           : "/configuration/menu_permission",
        #         "count"         : str(self.mgdDB.db_menu_permission.find({"role_position_value" : {"$ne" : "ADMIN"} }).count())
        #     })

        #     # FIND REGULAR CONFIG
        #     regular_config_list = []
        #     regular_config_view = self.mgdDB.db_config.find({ "config_type" : "" })
        #     for regular_config_item in regular_config_view:
        #         regular_config_list.append(regular_config_item["misc"])

        #     print("\n=====================================================")
        #     print(str(regular_config_list))
        #     print("=====================================================\n")
        #     # FIND BASIC CONFIG
        #     config_list = [] # majukan kanan
        #     config_view = self.mgdDB.db_config.aggregate([
        #         { "$match" : {"is_deleted" : False, "config_type" : {"$in" : regular_config_list } }},
        #         { "$group" : { "_id": "$config_type", "count":{"$sum":1} }}
        #         ])

        #     for config_item in config_view:
        #         config_item["config_title"  ] = utils._get_title(config_item["_id"])
        #         config_item["url"           ] = "/configuration/general_config?config_type=" + config_item["_id"]
        #         config_list.append(config_item)


            config_all_list += config_list

        response["message_data"] = { "config_all_list" : config_all_list }
        return response
    # end def

    

    def html(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "FIND_CONFIG_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            menu_list              = view_core_menu.view_core_menu().html(params)
            core_display           = view_core_display.view_core_display().html(params)
            params["core_display"] = core_display         
            core_header            = view_core_header.view_core_header().html(params)
            core_footer            = view_core_footer.view_core_footer().html(params)
            core_script            = view_core_script.view_core_script().html(params)
            core_css               = view_core_css.view_core_css().html(params)
            core_dialog_message    = view_core_dialog_message.view_core_dialog_message().html(params)


            config_all_msg         = self._find_config(params)
            config_list            = config_all_msg["message_data"]["config_all_list"]


            return render_template(
                "config/config-list.html",
                menu_list_html      = menu_list,
                config_list         = config_list,
                core_display        = core_display,
                core_header         = core_header, 
                core_footer         = core_footer, 
                core_script         = core_script,  
                core_css            = core_css,
                core_dialog_message = core_dialog_message,
                username            = params["username"      ],
                role_position       = params["role" ]
            )        

        except:
            print (traceback.format_exc())
            response["message_action"] = "DISPLAY_ALL_CONFIG_FAILED"
            response["message_action"] = "DISPLAY_ALL_CONFIG_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
# end class
