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

class view_register_class_edit:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def

    def _find_one_register_class(self, params):
        register_class_rec = self.mgdDB.db_class.find_one({"pkey" : params['class_id'], "is_deleted" : False })

        response = {
            "register_class_rec"    : register_class_rec,            
        }
        return response
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
             "$or": [                
                { 
                    "$and": [
                        { "creator_id": params['fk_user_id'] },  # Include documents with status "PAID"
                        { "buyer_user_id": "" }, # Only if buyer_user_id matches fk_user_id
                        {"class_id": {"$ne": params["class_id"]}}               
                    ]
                },  # Include documents with status "OPEN"
                { 
                    "$and": [
                        { "status_class": "PAID" },  # Include documents with status "PAID"
                        { "buyer_user_id": params['fk_user_id'] },  # Only if buyer_user_id matches fk_user_id
                        {"class_id": {"$ne": params["class_id"]}}               
                    ]
                }, 
                                
            ]
        })

       
        

        for class_item in class_view:
            class_list.append(class_item)

        response = {
            "class_list"   : class_list
        }
        return response
    # end def

    def _find_creator_name(self, register_class_rec):
        user_rec = self.mgdDB.db_user.find_one({ 
            "fk_user_id" : register_class_rec["creator_id"] 
        })   
        
        response = {
            "creator_name"   : user_rec["name"]
        }                

        return response
    # end def


    def _data_user(self):      
        user_uuid   = session["user_uuid"]
        query = { "user_uuid": user_uuid}
        user = self.mgdDB.db_user.find_one(query)     
        # ver_status = user['ver_email']          

        return user

    
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

            # FIND ONE class
            register_class_resp             = self._find_one_register_class( params )
            register_class_rec              = register_class_resp["register_class_rec"  ] 
            

            # FIND level_class
            level_class_resp             = self._find_level_class( params )
            level_class_list             = level_class_resp["level_class_list"         ] 

            # FIND creator class
            creator_name_resp             = self._find_creator_name( register_class_rec )            
            creator_name                  = creator_name_resp["creator_name"         ] 

            # FIND class
            class_resp             = self._find_class( params )
            class_list             = class_resp["class_list"         ] 

            user_rec         = self._data_user()     
            
            html = render_template(
                "register_class/register_class_edit.html",
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
                register_class_rec      = register_class_rec,
                user_rec                = user_rec
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

