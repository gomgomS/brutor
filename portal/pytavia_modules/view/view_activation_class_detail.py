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


class view_activation_class_detail:

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

    def _meeting_report(self, params):
        # Fetch meetings
        meeting_recs = self.mgdDB.db_meeting.find({
            "activation_class_id": params.get("activation_class_id")
        })
        meeting_list = list(meeting_recs)

        # Fetch attendance records
        attendance_recs = self.mgdDB.db_attendance.find({
            "fk_meeting_id": {"$in": [meeting['meeting_id'] for meeting in meeting_list]}
        })
        attendance_list = list(attendance_recs)

        # Fetch user records
        user_recs = self.mgdDB.db_user.find({
            "register_student": "TRUE"  # Example condition; adjust as needed
        })
        user_list = list(user_recs)
        
        # Fetch enrollment records
        enrollment_recs = self.mgdDB.db_enrollment.find({
            "activation_class_id": params.get("activation_class_id"),
            "is_deleted": False
        })
        enrollment_list = list(enrollment_recs)
        
        # Create mapping of user_id to user name
        user_map = {user['fk_user_id']: user['name'] for user in user_list}
        
        # Create mapping of user_id to enrollment status
        enrollment_map = {enrollment['fk_user_id']: enrollment['enrollment_status'] for enrollment in enrollment_list}

        # Initialize header
        th_meeting_report = ['Name', 'Status']  # Added 'Status' column
        for meeting_item in meeting_list:
            th_meeting_report.append(meeting_item['name_meeting'])
        th_meeting_report.append('Attendance %')  # Add attendance percentage column

        # Prepare data for the report
        report_data = []
        for user in user_list:
            user_id = user['fk_user_id']
            # Check if the user is registered
            if user_id not in enrollment_map:
                continue
            
            user_name = user['name']
            enrollment_status = enrollment_map.get(user_id, 'UNKNOWN')
            user_row = [user_name, enrollment_status]

            present_count = 0  # Counter for present meetings

            for meeting_item in meeting_list:
                meeting_id = meeting_item['meeting_id']
                # Find attendance record for the current user and meeting
                attendance_record = next((att for att in attendance_list if att['fk_user_id'] == user_id and att['fk_meeting_id'] == meeting_id), None)
                if attendance_record:
                    if attendance_record['status'] == 'PRESENT':
                        present_count += 1
                    user_row.append(attendance_record['status'])
                else:
                    user_row.append(' - ')  # Placeholder for no attendance record

            # Calculate attendance percentage
            total_meetings = len(meeting_list)
            attendance_percentage = (present_count / total_meetings) * 100 if total_meetings > 0 else 0
            user_row.append(f"{attendance_percentage:.2f}%")  # Format as percentage with two decimal places

            report_data.append(user_row)

        # Format response
        response = {            
            "header": th_meeting_report,
            "data": report_data
        }       
        

        return response


    def _test_report(self, params):
        # Fetch test records
        test_recs = self.mgdDB.db_test.find({
            "activation_class_id": params.get("activation_class_id")
        })
        test_list = list(test_recs)

        # Fetch test result records
        test_result_recs = self.mgdDB.db_test_result.find({
            "fk_test_id": {"$in": [test['test_id'] for test in test_list]}
        })
        test_result_list = list(test_result_recs)

        # Fetch user records
        user_recs = self.mgdDB.db_user.find({})
        user_list = list(user_recs)

        # Fetch enrollment records
        enrollment_recs = self.mgdDB.db_enrollment.find({
            "activation_class_id": params.get("activation_class_id"),
            "is_deleted": False
        })
        enrollment_list = list(enrollment_recs)

        # Create mappings
        user_map = {user['fk_user_id']: user['name'] for user in user_list}
        enrollment_map = {enrollment['fk_user_id']: enrollment['enrollment_status'] for enrollment in enrollment_list}

        # Initialize header
        th_test_report = ['Name', 'Enrollment Status'] + [test['name_test'] for test in test_list] + ['Passed Percentage']

        # Prepare data for the report
        report_data = []
        for user in user_list:
            user_id = user['fk_user_id']
            # Check if the user is registered
            if user_id not in enrollment_map:
                continue

            user_name = user_map.get(user_id, 'Unknown')
            enrollment_status = enrollment_map.get(user_id, 'UNKNOWN')
            user_row = [user_name, enrollment_status]

            pass_count = 0
            for test_item in test_list:
                test_id = test_item['test_id']
                # Find test result record for the current user and test
                test_result_record = next((result for result in test_result_list if result['fk_user_id'] == user_id and result['fk_test_id'] == test_id), None)
                if test_result_record:
                    status = test_result_record['status']
                    score = test_result_record['score']
                    if status == 'PASS':
                        pass_count += 1
                    user_row.append(f"{score} ({status})")
                else:
                    user_row.append('-')  # Placeholder for no test result record

            # Calculate passed percentage
            passed_percentage = (pass_count / len(test_list)) * 100 if test_list else 0
            user_row.append(f"{passed_percentage:.2f}%")

            report_data.append(user_row)

        # Format response
        response = {
            "header": th_test_report,
            "data": report_data
        }

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
    

            # FIND class
            # class_resp             = [self._find_enroll_class( params )]

            # FIND ACTIVE CLASS
            activation_class_rec                = self._find_activation_class( params )             

            # FIND CLASS
            class_rec                           = self._find_class( activation_class_rec["class_id"] ) 

            # FIND TEST
            test_recs                           = self._find_test( params ) 
            test_list                           = test_recs["test_list"     ] 

            # FIND MEEETING
            meeting_recs                        = self._find_meeting( params ) 
            meeting_list                        = meeting_recs["meeting_list"     ] 

            # FIND user
            user_rec                            = self._data_user(params) 

            # Meeting Report
            meeting_report_rec                  = self._meeting_report(params)      

            # Test Report
            test_report_rec                     = self._test_report(params)     

            
            html = render_template(
                "activation_class/activation_class_detail.html",
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
                meeting_report_rec      = meeting_report_rec,
                test_report_rec         = test_report_rec
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

    def _data_user(self,params):              
        query = { "fk_user_id": params["fk_user_id"]}
        user = self.mgdDB.db_user.find_one(query)             

        return user
    # end def
   
    
# end class

