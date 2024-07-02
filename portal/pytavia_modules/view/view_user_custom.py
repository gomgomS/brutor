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

class view_user_custom:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app    
    # end def

    def display_child_group(self, params) :

        fk_user_id          = params["fk_user_id"]
        child_role_final    = []

        # check if the user is super_user
        user_rec = self.mgdDB.db_super_user.find_one({ "pkey" : fk_user_id })

        if user_rec != None :
            child_role_list  = self.mgdDB.db_config_role.find({ "user_type" : "BO" })
            child_role_final = list ( child_role_list )        

        else :            
            user_rec  = self.mgdDB.db_user.find_one({ "pkey" : fk_user_id })
            
            if user_rec != None : 
                user_role       = user_rec["role"]
                child_role_list = self.mgdDB.db_role_parent_to_child_mapping.find({ "parent_role_val" : user_role })
              

                for each_role in child_role_list :
                    child_role_list_rec = self.mgdDB.db_config_role.find_one({ 
                            "value"     : each_role["child_role_val"],
                            "user_type" : "BO"
                        })
                    if child_role_list_rec != None :
                        child_role_final.append( child_role_list_rec )
                # end for
            # end if
        # end else

        self.webapp.logger.debug( "display group 2 child_role_final ---------------------------------------------" )
        self.webapp.logger.debug( child_role_final )
        self.webapp.logger.debug( "---------------------------------------------" )

        response = { "config_role_list" : child_role_final }

        return response


    #end def

    def display_list(self, params) :
        user_final_list = []
        fk_user_id      = params["fk_user_id"]

        user_data = {                    
                    "pkey"              : "",
                    "name"              : "",
                    "phone"             : "",
                    "email"             : "",
                    "username"          : "",
                    "role_name"         : "",
                    "login_status"      : "",
                    "inactive_status"   : "",
                    "inactive_note"     : "",
                }

        # cek if user is super_user :
        fk_user_rec = self.mgdDB.db_super_user.find_one({ "pkey" : fk_user_id })

        if fk_user_rec != None :
            user_list_rec = self.mgdDB.db_user.find({ "type" : "BO" })
            
            if user_list_rec != None :

                for each_user in user_list_rec :
                    user_data = {}                 
                    user_data["pkey"    ] = each_user["pkey"          ]
                    user_data["name"    ] = each_user["name"          ]
                    user_data["phone"   ] = each_user["phone"         ]
                    user_data["email"   ] = each_user["email"         ]
                    user_data["username"] = each_user["username"      ]

                    user_role_rec = self.mgdDB.db_config_role.find_one({ "value" : each_user["role"] })
                    if user_role_rec != None :
                        user_data["role_name"] = user_role_rec["name" ]
                    # end if

                    user_auth_rec = self.mgdDB.db_user_auth.find_one({ "fk_user_id" : each_user["pkey"] })
                    if user_auth_rec != None :
                        user_data["login_status"    ] = user_auth_rec["login_status"  ]                        
                        user_data["inactive_note"   ] = user_auth_rec["inactive_note" ]
                        user_data["inactive_status" ] = config.G_STATUS_INACTIVE[ user_auth_rec["inactive_status"] ]
                    # end if

                    user_final_list.append( user_data )
                    
                #end for
            # end if
        # end if
        else :
            fk_user_rec = self.mgdDB.db_user.find_one({ "pkey" : fk_user_id })

            if fk_user_rec != None :
                
                all_child_role = self.display_child_group( params )
                
                if len(all_child_role["config_role_list"]) > 0 :
                    for each_child_role in all_child_role["config_role_list"] :
                        print("===========================================")
                        print("each child role in all child_role_list")
                        print(each_child_role)

                        user_list_rec = self.mgdDB.db_user.find({ 
                            "type" : "BO", 
                            "role" : each_child_role["value"],
                            "pkey" : { "$nin" : [fk_user_id] }
                        })

                        if user_list_rec != None :
                            for each_user in user_list_rec :
                                user_data = {}                 
                                user_data["pkey"    ] = each_user["pkey"          ]
                                user_data["name"    ] = each_user["name"          ]
                                user_data["phone"   ] = each_user["phone"         ]
                                user_data["email"   ] = each_user["email"         ]
                                user_data["username"] = each_user["username"      ]

                                user_role_rec = self.mgdDB.db_config_role.find_one({ "value" : each_user["role"] })
                                if user_role_rec != None :
                                    user_data["role_name"] = user_role_rec["name" ]
                                # end if

                                user_auth_rec = self.mgdDB.db_user_auth.find_one({ "fk_user_id" : each_user["pkey"] })
                                if user_auth_rec != None :
                                    user_data["login_status"    ] = user_auth_rec["login_status"  ]                        
                                    user_data["inactive_note"   ] = user_auth_rec["inactive_note" ]
                                    user_data["inactive_status" ] = config.G_STATUS_INACTIVE[ user_auth_rec["inactive_status"] ]
                                # end if

                                user_final_list.append( user_data )

                        # end for user_list_rec
                    # end for all_child_role
                # end if
            #end if

        # end else

        response = { "user_list" : user_final_list }
        return response

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

        user_list_resp         = self.display_list( params ) 
        user_list              = user_list_resp["user_list"]
        display_group_resp     = self.display_child_group( params ) 
        config_role_list       = display_group_resp["config_role_list"]
        
        return render_template(
            "list-user/user-list.html",
            menu_list_html      = menu_list,
            config_role_list    = config_role_list,
            user_list           = user_list,
            core_display        = core_display,
            core_header         = core_header, 
            core_footer         = core_footer, 
            core_script         = core_script,  
            core_css            = core_css,
            core_dialog_message = core_dialog_message 
        )                
    # end def
# end class
