import sys
import traceback
import time
import json
from datetime import datetime
import statistics
from bson import Int64

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

from view import view_core_menu
from view import view_core_display
from view import view_core_header
from view import view_core_footer
from view import view_core_script
from view import view_core_css
from view import view_core_dialog_message

class view_dashboard:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    # FIND DATA USER ACTIVE ------------------THIS NEW DELETE THIS COMMENT AFTER YOU BACK
    def _data_user(self):      
        user_uuid   = session["user_uuid"]
        query = { "user_uuid": user_uuid}
        user = self.mgdDB.db_user.find_one(query)     
        # ver_status = user['ver_email']          

        return user
    
    def _find_class(self, activation_class_id):
        activation_class_rec = self.mgdDB.db_activation_class.find_one({
            "activation_class_id": activation_class_id                
        })

        class_rec = self.mgdDB.db_class.find_one({
            "class_id": activation_class_rec['class_id']                
        })

        return class_rec

    def _find_schedule(self, params):
        schedule_list = []
        current_time = datetime.now()

        # Step 1: Fetch enrollment records for the user
        enrollment_rec = self.mgdDB.db_enrollment.find({
            "fk_user_id": params["fk_user_id"],
            "enrollment_status": 'REGISTERED'
        })
            
        for enrollment in enrollment_rec:
            activation_class_id = enrollment["activation_class_id"]

            class_rec = self._find_class(enrollment["activation_class_id"])

            # Step 2: Fetch class details using activation_class_id
            class_details = self.mgdDB.db_activation_class.find_one({"activation_class_id": activation_class_id})                        
            
            # Step 3: Fetch meetings related to this activation_class_id
            meeting_rec = self.mgdDB.db_meeting.find({"activation_class_id": activation_class_id})
            for meeting in meeting_rec:
                # Convert date format directly in the function
                start_iso = datetime.strptime(meeting["str_start_datetime"], "%d/%m/%Y %H:%M").isoformat()
                end_iso = datetime.strptime(meeting["str_end_datetime"], "%d/%m/%Y %H:%M").isoformat()

                # Determine color based on whether the event has passed
                event_color = "grey" if datetime.strptime(meeting["str_end_datetime"], "%d/%m/%Y %H:%M") < current_time else "blue"

                # Create event dictionary
                event = {
                    "title": meeting["name_meeting"],
                    "start": start_iso,  # ISO formatted date
                    "end": end_iso,      # ISO formatted date
                    "url": meeting.get("source", ""),  # Optional field
                    "color": event_color,  # Set color based on date
                    "detail_activation_class": "/myClass/detail/"+enrollment["enrollment_id"],
                    "extendedProps": {
                        "class_name": class_rec['name_class'],                        
                    }
                }
                schedule_list.append(event)
            
            # Step 4: Fetch tests related to this activation_class_id
            test_rec = self.mgdDB.db_test.find({"activation_class_id": activation_class_id})
            for test in test_rec:
                # Convert date format directly in the function
                start_iso = datetime.strptime(test["str_start_datetime"], "%d/%m/%Y %H:%M").isoformat()
                end_iso = datetime.strptime(test["str_end_datetime"], "%d/%m/%Y %H:%M").isoformat()

                # Determine color based on whether the event has passed
                event_color = "grey" if datetime.strptime(test["str_end_datetime"], "%d/%m/%Y %H:%M") < current_time else "orange"

                # Create event dictionary
                event = {
                    "title": test["name_test"],
                    "start": start_iso,  # ISO formatted date
                    "end": end_iso,      # ISO formatted date
                    "url": test.get("source", ""),  # Optional field
                    "color": event_color,  # Set color based on date
                    "detail_activation_class": "/myClass/detail/"+enrollment["enrollment_id"],
                    "extendedProps": {
                        "class_name": class_rec['name_class'],                        
                    }
                }
                schedule_list.append(event)

        return {"schedule_list": schedule_list}

    def _find_schedule_as_tutor(self, params):
        schedule_list = []
        fk_user_id = params['fk_user_id']
        current_time = datetime.now()
        
        # Step 3: Fetch meetings related to this fk_user_id
        meeting_rec = self.mgdDB.db_meeting.find({"fk_user_id": fk_user_id},
        {"_id":0,"activation_class_id":1,"name_meeting":1,"str_start_datetime":1,"str_end_datetime":1})

        schedule_list_meeting = []
        for meeting in meeting_rec:
            # Convert date format directly in the function
            start_iso = datetime.strptime(meeting["str_start_datetime"], "%d/%m/%Y %H:%M").isoformat()
            end_iso = datetime.strptime(meeting["str_end_datetime"], "%d/%m/%Y %H:%M").isoformat()

            # Determine color based on whether the event has passed
            event_color = "grey" if datetime.strptime(meeting["str_end_datetime"], "%d/%m/%Y %H:%M") < current_time else "blue"

            # Create event dictionary
            event = {
                "title": meeting["name_meeting"],
                "start": start_iso,  # ISO formatted date
                "end": end_iso,      # ISO formatted date
                "url": "/activation_class/detail/" + meeting["activation_class_id"],  # Link to class details
                "color": event_color,  # Set color based on date                
            }
            schedule_list_meeting.append(event)
        
        #  Step 4: Fetch tests related to this fk_user_id
        test_rec = self.mgdDB.db_test.find({"fk_user_id": fk_user_id},
        {"_id":0,"activation_class_id":1,"name_test":1,"str_start_datetime":1,"str_end_datetime":1})
        for test in test_rec:
            # Convert date format directly in the function
            start_iso = datetime.strptime(test["str_start_datetime"], "%d/%m/%Y %H:%M").isoformat()
            end_iso = datetime.strptime(test["str_end_datetime"], "%d/%m/%Y %H:%M").isoformat()

            # Determine color based on whether the event has passed
            event_color = "grey" if datetime.strptime(test["str_end_datetime"], "%d/%m/%Y %H:%M") < current_time else "orange"

            # Create event dictionary
            event = {
                "title": test["name_test"],
                "start": start_iso,  # ISO formatted date
                "end": end_iso,      # ISO formatted date
                "url": "/activation_class/detail/" + test["activation_class_id"],  # Link to class details
                "color": event_color,  # Set color based on date                
            }
            schedule_list.append(event)

        return {"schedule_list": schedule_list}


    def html(self, params):
        menu_list               = view_core_menu.view_core_menu().html(params)
        core_display            = view_core_display.view_core_display().html(params)
        params["core_display"]  = core_display         
        core_header             = view_core_header.view_core_header().html(params)
        core_footer             = view_core_footer.view_core_footer().html(params)
        core_script             = view_core_script.view_core_script().html(params)
        core_css                = view_core_css.view_core_css().html(params)
        core_dialog_message     = view_core_dialog_message.view_core_dialog_message().html(params)

        user_rec         = self._data_user()                          

        # FIND SCHEDULE, SEPERATE SCHEDULE BETWEEN TUTOR AND STUDENT
        if params['role'] == 'STUDENT':
            schedule_recs                        = self._find_schedule( params ) 
        else:
            schedule_recs                        = self._find_schedule_as_tutor( params ) 

        schedule_list                        = schedule_recs["schedule_list"     ] 


        return render_template(
            "dashboard/index.html",
            menu_list_html      = menu_list               ,
            core_display        = core_display            , 
            core_header         = core_header             , 
            core_footer         = core_footer             , 
            core_script         = core_script             , 
            core_css            = core_css                , 
            core_dialog_message = core_dialog_message     ,
            username            = params["username"      ],
            role_position       = params["role_position" ],            
            user_rec            = user_rec,
            schedule_list       = schedule_list

           # users_total         = users_total,
            
        )                
    # end def
# end class
