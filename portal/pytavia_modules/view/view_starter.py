
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
from pytavia_core   import helper

from view import view_core_menu
from view import view_core_display
from view import view_core_header
from view import view_core_footer
from view import view_core_script
from view import view_core_css
from view import view_core_dialog_message

class view_starter:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app    
    # end def


    def _find_starter_button(self, params):
        starter_button_list = []
        starter_button_view = self.mgdDB.db_starter.find({ "is_deleted" : False, "menu_value" : params["menu_value"] }).sort( "position", 1 )
        for starter_button_item in starter_button_view:
            starter_button_list.append(starter_button_item)

        response = {
            "starter_button_list"   : starter_button_list
        }

        return response
    # end def
    

    def _find_current_menu(self,params):                                    
        current_menu = self.mgdDB.db_menu.find_one({
            "value" : params['menu_value']
        })
        
        response =  current_menu
        return response

    def _find_permission_role(self,params):     
        permission_role_list = []

        permission_role = self.mgdDB.db_menu_permission.find({
            "menu_value" : params['menu_value']
        },{"_id":0,"menu_value":1,"role_position_value":1})      
        
        for permission_role_item in permission_role:
            permission_role_list.append(permission_role_item['role_position_value'])

        response = {
            "permission_role_list"   : permission_role_list
        }
                  
        return response


    def html(self, params):
        response = helper.response_msg(
            "FIND_STARTER_SUCCESS", "FIND STARTER SUCCESS", {} , "0000"
        )
        try:
            menu_list_html         = view_core_menu.view_core_menu().html(params)
            core_display           = view_core_display.view_core_display().html(params)
            params["core_display"] = core_display         
            core_header            = view_core_header.view_core_header().html(params)
            core_footer            = view_core_footer.view_core_footer().html(params)
            core_script            = view_core_script.view_core_script().html(params)
            core_css               = view_core_css.view_core_css().html(params)
            core_dialog_message    = view_core_dialog_message.view_core_dialog_message().html(params)


            # FIND STARTER BUTTONS
            starter_button_resp             = self._find_starter_button( params )
            starter_button_list             = starter_button_resp["starter_button_list"     ] 

            # FIND CURRENT MENU NOW
            current_menu                     = self._find_current_menu( params ) 

            # FIND PERMISSION ACCESS MENU 
            permission_role                  = self._find_permission_role( params ) 
            permission_role_list             = permission_role["permission_role_list"     ] 

            # FIND user
            user_rec                = self._data_user(params)       

            html = render_template(
                "starter/starter.html",
                menu_list_html      = menu_list_html,
                core_display        = core_display,
                core_header         = core_header, 
                core_footer         = core_footer, 
                core_script         = core_script,  
                core_css            = core_css,
                core_dialog_message = core_dialog_message,
                username            = params["username"      ],
                role_position       = params["role_position" ],
                starter_button_list= starter_button_list,              
                current_menu        = current_menu,
                user_rec            = user_rec
            )

            response.put( "data", {
                    "html" : html,
                    "permission_role_list": permission_role_list
                }
            )


        except:
            trace_back_msg = traceback.format_exc() 
            print(trace_back_msg)
            self.webapp.logger.debug(trace_back_msg)
            response.put( "status"      , "FIND_STARTER_FAILED" )
            response.put( "desc"        , "FIND STARTER FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try

        return response
    # end def

    def _data_user(self,params):              
        query = { "fk_user_id": params["fk_user_id"]}
        user = self.mgdDB.db_user.find_one(query)             

        return user
    
# end class

