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

class view_core_menu:
   
    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self):
        self.g_menu_list = list(
            self.mgdDB.db_config_menu_webapp_item_all.find({"status":"ENABLE"}).sort(
                "order",pymongo.ASCENDING
            )
        )
    # end def

    def menu_display(self, params): 
        fk_user_id      = session.get("fk_user_id")
        role   = session.get("role")
        menu_list       = []

        # FIND MENU DEPENDING ON THE ROLE PERMISSION

        permitted_menu_list = []
        permission_view = self.mgdDB.db_menu_permission.find({ "role_position_value" : role })
        for permission_item in permission_view:
            permitted_menu_list.append(permission_item["menu_value"])
        

        # FIND THE MENU THAT IS ALLOWED FOR THE ROLE POSITION
        menu_list = []
        menu_view = self.mgdDB.db_menu.find({"value" : { "$in" : permitted_menu_list }}).sort("position", 1)
        for menu_item in menu_view:
            menu_list.append(menu_item)
        
        # ADD LOGOUT
        # menu_list.append(
        #     {
        #         "menu_name"     : "LOGOUT",
        #         "icon_class"    : "log-out",
        #         "url"           : "/auth/logout"
        #     }
        # )
 
        return menu_list
    # end def
    

    
    # get from route_privilege
    def menu_display_2(self, params):
        # fk_user_id  = params["fk_user_id"]
        fk_user_id    = session.get("fk_user_id")
        menu_list   = []
        user_role_rec = self.mgdDB.db_user.find_one({
            "pkey" : fk_user_id
        })
        """
            If the user role is not found then check the super user
            if it is not then we just exit this 
        """
        
        # if user_role_rec == None:
        superuser_role_rec = self.mgdDB.db_user.find_one({ "pkey" : fk_user_id })
        if superuser_role_rec != None:
            menu_list = self.mgdDB.db_config_webapp_route_privileges.find({ "status" : "ENABLE" , "route_type" : "MENU" }).sort(
                    "order",pymongo.ASCENDING
            )
        # end if
        response = { "menu_list" : menu_list }

        return response

        # end if
        """
            process this if the user role is found in db_user_role table and 
            the user has a specific role
        """
        # fk_role_id          = user_role_rec["role"]
        # role_privilege_view = self.mgdDB.db_config_webapp_role_privilege.find({
        #     "fk_role_id" : fk_role_id
        # })
        # check_duplicate = {}
        # for role_privilege_rec in role_privilege_view:
        #     fk_privilege_id    = role_privilege_rec["fk_privilege_id"]
        #     menu_privilege_rec = self.mgdDB.db_config_webapp_route_privileges.find_one({
        #         "value"           : fk_privilege_id,
        #         "status"          : "ENABLE",
        #         "route_type"      : "MENU"
        #     })
        #     if menu_privilege_rec != None:
        #         fk_menu_id    = menu_privilege_rec["value"]

        #         if fk_menu_id not in check_duplicate :
        #             check_duplicate[ fk_menu_id ] = fk_menu_id                
        #             menu_list.append( menu_item_rec )
                # end 
                    
            # end if
        # end for
        
        new_list = sorted(menu_list, key=lambda k: k['order']) 

        #print( "core menu 2: new list sorted ---------------------------------------------" )
        #print( new_list )
        #print( "---------------------------------------------" )

        response = { "menu_list_2" : new_list }
        #response = { "menu_list" : menu_list }
        return response
    # end def


    """
        Later as part of these params object
        we need to see who the user is and render based on that.
        This is the new application
    """


    def html(self, params):
        g_menu_list = self.menu_display( params )
        return g_menu_list
    # end def

# end class
