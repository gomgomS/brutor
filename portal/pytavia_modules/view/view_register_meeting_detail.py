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


class view_register_meeting_detail:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def

    

    def _find_register_meeting_detail(self, params):    

        # find activation class id base meeting id
        meeting_rec = self.mgdDB.db_meeting.find_one({ 
            "meeting_id" : params['meeting_id']
        })   

        activation_class_id = meeting_rec['activation_class_id']
        
        # find list enrollment student register in this class base
        student_enrollments = self.mgdDB.db_enrollment.find({
            "activation_class_id" : activation_class_id,
        })
      
        
        student_enrollment_list = []
        for user_item in student_enrollments:            
            # find data user         
            user_resp                       = self._data_user_enrollment( user_item["fk_user_id"] )            
            user_item["detail_student"]     = user_resp

            # find attendance user and user id student
            attendance_user_resp                       = self._data_attendance_user( params['meeting_id'], user_item["detail_student"]["fk_user_id"] )            
            user_item["detail_attendance_student"]     = attendance_user_resp
            student_enrollment_list.append(user_item)
       

        response = {
            "student_enrollment_list"   : student_enrollment_list,           
        }

        return response
    # end def
    

    def html(self, params):
        response = helper.response_msg(
            "FIND_meeting_SUCCESS", "FIND meeting SUCCESS", {} , "0000"
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


            entry_resp              = utils._find_table_entries()
            entry_list              = entry_resp["entry_list"]

            # FIND user
            user_rec                = self._data_user(params)       

            # FIND meeting INFOMRATION
            meeting_rec                = self._find_meeting_information(params)

            # FIND meeting
            meeting_resp                   = self._find_register_meeting_detail( params )            
            student_enrollment_list     = meeting_resp["student_enrollment_list"]

            html = render_template(
                "register_meeting/register_meeting_detail_list.html",
                menu_list_html          = menu_list_html,
                core_display            = core_display,
                core_header             = core_header, 
                core_footer             = core_footer, 
                core_script             = core_script,  
                core_css                = core_css,
                core_dialog_message     = core_dialog_message,
                username                = params["username"      ],
                role_position           = params["role_position" ],                                           
                user_rec                = user_rec,
                student_enrollment_list = student_enrollment_list,
                meeting_id                 = params['meeting_id'],
                meeting_rec                = meeting_rec          
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
    
    def _find_meeting_information(self, params):      
        class_rec = self.mgdDB.db_meeting.find_one({ 
            "meeting_id" : params['meeting_id']
        })         

        response = class_rec
        return response

    def _data_user_enrollment(self,fk_user_id):         
            
        user = self.mgdDB.db_user.find_one(
            { "fk_user_id": fk_user_id},
            {'_id':0,'name':1,'fk_user_id':1,'username':1}
        )

        return user

    def _data_user(self,params):              
        query = { "fk_user_id": params["fk_user_id"]}
        user = self.mgdDB.db_user.find_one(query)             

        return user

    def _data_attendance_user(self, meeting_id, fk_user_id):        
        query = { 
            "fk_meeting_id": meeting_id,
            "fk_user_id": fk_user_id
            }
        
        user = self.mgdDB.db_attendance.find_one(query)             

        return user
# end class

