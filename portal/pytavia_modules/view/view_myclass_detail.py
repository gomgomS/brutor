import sys
import traceback
import pymongo
import urllib.parse

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

sys.path.append("pytavia_modules/view" )

from flask          import render_template
from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_stdlib import pagination
from pytavia_core   import helper
from pytavia_core   import database
from pytavia_core   import config

from view import view_core_menu
from view import view_core_display
from view import view_core_header
from view import view_core_footer
from view import view_core_script
from view import view_core_css
from view import view_core_dialog_message


class view_myclass_detail:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def

    def _find_activation_class(self, params):      
        activation_class_rec = self.mgdDB.db_activation_class.find_one({ 
            "activation_class_id" : params["activation_class_id"]
        })           
        response = activation_class_rec 
        return response

    def _find_class(self, class_id):      
        class_rec = self.mgdDB.db_class.find_one({ 
            "class_id" : class_id
        })   
        response = class_rec 
        return response       

    def _find_test(self, params): 
        test_list = []     
        test_recs = self.mgdDB.db_test.find({ 
            "activation_class_id" : params["activation_class_id"]
        })   

        for test_item in test_recs:
            test_list.append(test_item)

        response = {
            "test_list"   : test_list
        }

        return response 
    
    def _find_meeting(self, params):     
        meeting_list = [] 
        meeting_recs = self.mgdDB.db_meeting.find({ 
            "activation_class_id" : params["activation_class_id"]
        })          

        for meeting_item in meeting_recs:
            meeting_list.append(meeting_item)

        response = {
            "meeting_list"   : meeting_list
        }
        
        return response 

    def _find_enrollment(self, params):      
        enrollment_rec = self.mgdDB.db_enrollment.find_one({ 
            "enrollment_id" : params["enrollment_id"]
        })   

        response = enrollment_rec 
        return response     
    
    def _find_tutor(self, params):             
        user_rec = self.mgdDB.db_user.find_one({ 
            "fk_user_id" : params["fk_user_id"]
        })   

        response = user_rec 
        return response 
    

    def html(self, params):
        response = helper.response_msg(
            "FIND_CLASS_PROSES_SUCCESS", "FIND KONTEN PROSES SUCCESS", {} , "0000"
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
    

            # FIND ENROLLMENT
            enrollment_rec                      = self._find_enrollment( params )             
            

            # FIND ACTIVE CLASS
            activation_class_rec                = self._find_activation_class( enrollment_rec )             
            # FIND TUTOR
            tutor_rec                           = self._find_tutor( activation_class_rec )             

            # FIND CLASS
            class_rec                           = self._find_class( activation_class_rec["class_id"] ) 

            # FIND TEST
            test_recs                           = self._find_test( enrollment_rec ) 
            test_list                           = test_recs["test_list"     ] 

            # FIND MEEETING
            meeting_recs                        = self._find_meeting( enrollment_rec ) 
            meeting_list                        = meeting_recs["meeting_list"     ] 

            # FIND user
            user_rec                            = self._data_user(params)       
            
            html = render_template(
                "myclass/myclass_detail.html",
                menu_list_html          = menu_list_html,
                core_display            = core_display,
                core_header             = core_header, 
                core_footer             = core_footer, 
                core_script             = core_script,  
                core_css                = core_css,
                core_dialog_message     = core_dialog_message,
                username                = params["username"      ],
                role_position           = params["role_position" ],       
                activation_class_rec    = activation_class_rec,
                class_rec               = class_rec,
                test_list               = test_list,
                meeting_list            = meeting_list,
                user_rec                = user_rec,
                tutor_rec               = tutor_rec,
            )


            response.put( "data", {
                    "html" : html
                }
            )


        except:
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "FIND_KONTEN_PROSES_FAILED" )
            response.put( "desc"        , "FIND_KONTEN_PROSES_FAILED" )
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

