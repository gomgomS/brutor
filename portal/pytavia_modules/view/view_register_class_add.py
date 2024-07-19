import sys
import traceback

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
from pytavia_core   import helper

from view import view_core_menu
from view import view_core_display
from view import view_core_header
from view import view_core_footer
from view import view_core_script
from view import view_core_css
from view import view_core_dialog_message

class view_register_class_add:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def


    def _find_level_class(self, params):
        level_class_list = []
        level_class_view = self.mgdDB.db_level_class.find()
        for level_class_item in level_class_view:
            level_class_list.append(level_class_item)

        response = {
            "level_class_list"   : level_class_list
        }
        return response
    # end def

    def _find_class(self, params):
        class_list = []
       
        class_view = self.mgdDB.db_class.find({
            "$or": [{
                "creator_id"    :params["fk_user_id"],
                "buyer_user_id" :params["fk_user_id"]
            }]
        })
        

        for class_item in class_view:
            class_list.append(class_item)

        response = {
            "class_list"   : class_list
        }
        return response
    # end def

    def _find_creator_name(self, params):
        user_rec = self.mgdDB.db_user.find_one({ 
            "fk_user_id" : params["fk_user_id"] 
        })   
        
        response = {
            "creator_name"   : user_rec["name"]
        }                

        return response
    # end def


    
    def html(self, params):
        response = helper.response_msg(
            "FIND_KONTEN_TAMBAH_FORM_SUCCESS", "FIND KONTEN TAMBAH FORM SUCCESS", {} , "0000"
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

            # FIND level_class
            level_class_resp             = self._find_level_class( params )
            level_class_list             = level_class_resp["level_class_list"         ] 

            # FIND creator class
            creator_name_resp             = self._find_creator_name( params )            
            creator_name                  = creator_name_resp["creator_name"         ] 

            # FIND class
            class_resp             = self._find_class( params )
            class_list             = class_resp["class_list"         ] 
            print(class_list)
            print("hokage")
            
            html = render_template(
                "register_class/register_class_add.html",
                menu_list_html          = menu_list_html,
                core_display            = core_display,
                core_header             = core_header, 
                core_footer             = core_footer, 
                core_script             = core_script,  
                core_css                = core_css,
                core_dialog_message     = core_dialog_message,
                username                = params["username"      ],
                role_position           = params["role_position" ],
                redirect                = params["redirect"      ],       
                level_class_list        = level_class_list,
                creator_name            = creator_name,       
                class_list              = class_list,
              )

            response.put( "data", {
                    "html" : html
                }
            )


        except:
            trace_back_msg = traceback.format_exc() 
            print(trace_back_msg)
            self.webapp.logger.debug(trace_back_msg)
            response.put( "status"      , "FIND_KONTEN_TAMBAH_FORM_FAILED" )
            response.put( "desc"        , "FIND KONTEN TAMBAH FORM FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try

        return response
    # end def
    
# end class

