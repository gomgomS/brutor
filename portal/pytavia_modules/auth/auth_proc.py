import sys
import traceback
import datetime
import time
import ast # use to convert string to dictionary 
from   datetime import datetime
import random
import string

from view   import view_core_menu

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_stdlib import emailproc
from pytavia_core   import database
from pytavia_core   import config
from uuid     import uuid4
from flask import request 

class auth_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def
    
    def log_login(self,params):
        fk_user_id = params["fk_user_id" ] if "fk_user_id" in params else None
        state      = params["state"      ] if "state"      in params else None
        desc       = params["desc"       ] if "desc"       in params else None     
        username   = params["username"   ] if "username"   in params else None     
        log_login_rec  = database.get_record("db_log_login_auth")
        log_login_rec["fk_user_id" ] = fk_user_id
        log_login_rec["username"   ] = username
        log_login_rec["desc"       ] = desc
        log_login_rec["state"      ] = state
        self.mgdDB.db_log_login_auth.insert( log_login_rec )
        
        return True
    #end def
    
    def validate_wrong_counter(self,params):
        params_log ={
            "fk_user_id" : "",
            "state"      : "",
            "des"        : ""
        }
        username        = params["username"   ]
        state_login     = params["state_login"]        
        current_date    = int(time.time())
        day_reset_wrong_counter = 0 
        limit_wrong_counter     = 0        
        
        limit_wrong_counter_rec = self.mgdDB.db_setting_app.find_one(
                {},{"wrong_counter" : 1 , "_id" : 0}
        )
        
        if "wrong_counter" in limit_wrong_counter_rec:
            limit_wrong_counter = limit_wrong_counter_rec["wrong_counter"]
        # end if
        user_auth_rec = self.mgdDB.db_user_auth.find_one({ 
            "username" : username 
        })              
        
        if user_auth_rec  == None:
            params_log["state_login" ] = state_login
            params_log["fk_user_id"  ] = None
            params_log["desc"        ] = "Failed in validate username"
            self.log_login(params_log)
            return False
        #end if
        
        user_role_rec = self.mgdDB.db_user_role.find_one({
            "fk_user_id" : user_auth_rec["fk_user_id"]
        }) 
        
        config_role_rec = self.mgdDB.db_config_role.find_one({
            "value" : user_role_rec["role"]
        })         
               
        if state_login == "LOGIN_SUCCESS":            
            role_misc               = ast.literal_eval(config_role_rec["misc"])  
            wrong_counter           = user_auth_rec["wrong_counter"     ]
            date_last_failed_login  = user_auth_rec["date_failed_login" ]
            
            if "reload_wrong_counter" in role_misc:
                day_reset_wrong_counter = role_misc["reload_wrong_counter"] 
            # end if        
            if date_last_failed_login == None or date_last_failed_login == 0:
                date_last_failed_login = current_date
            # end if
            
            date_last_failed_login = datetime.fromtimestamp(date_last_failed_login)
            current_date           = datetime.fromtimestamp(current_date)
            totaldays              = (current_date - date_last_failed_login).days
            if int(totaldays) >= int(day_reset_wrong_counter):
                wrong_counter = 0
            #end if

            self.mgdDB.db_user_auth.update(
                {"username" : username},
                { "$set"    : {
                        "wrong_counter"     : wrong_counter,
                        "date_failed_login" : 0 ,
                        "login_status"      : "TRUE",
                        "forced_logout"     : "FALSE"
                    }
                }
            )   
            
            params_log["state_login" ] = state_login
            params_log["fk_user_id"  ] = user_auth_rec["fk_user_id"]
            params_log["desc"        ] = "login success"
            self.log_login(params_log)            
            return True
         
        """ 
         - Status login failed and user_auth is exist
        """
        if user_auth_rec["lock"] != "TRUE":
            self.mgdDB.db_user_auth.update(
                {"username" : username},
                { "$set" : {
                        "wrong_counter"     : int(user_auth_rec["wrong_counter"]) + 1,
                        "date_failed_login" : current_date
                    }
                }
            )
        #end if
            
        if int(user_auth_rec["wrong_counter"]) >= int(limit_wrong_counter) : 
            self.mgdDB.db_user_auth.update(
                {"username" : username},
                {"$set"     : {"lock" : "TRUE"}}                    
            )
        #end if
        
        params_log["state_login" ] = state_login
        params_log["fk_user_id"  ] = user_auth_rec["fk_user_id"]
        params_log["desc"        ] = "Failed in validate password"
        self.log_login(params_log)
        
        return False 
    #end def
    
    def logout(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "LOGOUT_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }

        self.webapp.logger.debug( "auth logout params ---------------------------------------------" )
        self.webapp.logger.debug( params )
        self.webapp.logger.debug( "---------------------------------------------" )    

        try:
            fk_user_id = params["fk_user_id"]            
            self.mgdDB.db_user.update(
                {"pkey" : fk_user_id},
                { "$set"    : {
                        "login_status"      : "FALSE"
                    }
                }
            )
            
            self.mgdDB.db_cookies.update(
                {
                    "fk_user_id" : fk_user_id,
                    "active"     : "TRUE"
                },
                { "$set"    : {
                        "active" : "FALSE"
                    }
                }
            )
            
        except:
            print (traceback.format_exc())
            response["message_action"] = "LOGOUT_FAILED"
            response["message_action"] = "LOGOUT_FAILED: " + str(sys.exc_info())
        # end try
        return response

    def login(self, params) :
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "LOGIN_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }

        try:
            username        = params["txt_l_username"]
            password        = params["txt_l_password"]

            browser         = request.user_agent.browser
            xff             = request.remote_addr

            hashed_password = utils._get_passwd_hash({
                "id"       : username,
                "password" : password
            })

            user_rec = self.mgdDB.db_user.find_one({
                "username" : username,
                "password" : hashed_password
            })         
            
       

            if user_rec == None :    
                # NO RECORD FOUND
                error_msg_rec = self.mgdDB.db_config_general.find_one({                            
                            "value" : "ERROR_LOGIN_TYPE_001"                            
                        })

            else :
                if user_rec["inactive_status"] == "TRUE" :
                    error_msg_rec = self.mgdDB.db_config_general.find_one({                            
                            "value" : "ERROR_LOGIN_TYPE_002"                            
                        })
                    
                else :
                    
                    self.mgdDB.db_user.update(
                        {"pkey"     : user_rec["pkey"]},
                        {"$set"     : {
                            "login_status"    : "TRUE",
                        }}
                    )

                    response["message_action"] = "LOGIN_SUCCESS"
                    response["message_code"  ] = ""
                    response["message_title" ] = ""
                    response["message_desc"  ] = ""
                    response["message_data"  ] = {
                        "fk_user_id"      : user_rec["pkey"                 ],
                        "username"        : user_rec["username"             ],
                        "role"            : user_rec["role"                 ],
                        "user_uuid"       : user_rec["user_uuid"            ],
                        "email"           : user_rec["email"                ],
                    }
                    return response

                #end if                 

            #endif

            if error_msg_rec != None :
                response["message_action"] = "LOGIN_FAILED"
                response["message_code"  ] = error_msg_rec["misc"]
                response["message_title" ] = error_msg_rec["name"]
                response["message_desc"  ] = error_msg_rec["desc"]

                       
        # end try
        except :
            self.webapp.logger.debug (traceback.format_exc())
            response["message_action"] = "LOGOUT_FAILED"
            response["message_desc"  ] = "LOGOUT_FAILED: " + str(sys.exc_info())

        #end except     
        return response
    #end def

    def register_superuser(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "REGISTER_SUPERUSER_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            username        = params["username"]
            password        = params["password"]
            role            = params["role"    ]
            hashed_password = utils._get_passwd_hash({
                "id"        : username,
                "password"  : password
            })
            super_user_rec  = self.mgdDB.db_super_user.find_one({
                "username"  : username
            })
            if super_user_rec != None:
                response["message_action"] = "REGISTER_SUPERUSER_FAILED"
                response["message_code"  ] = "1"
                response["message_desc"  ] = "username already taken"
                return response
            # end if
            super_user_rec = database.get_record("db_super_user")
            super_user_rec["username"] = username
            super_user_rec["password"] = hashed_password
            super_user_rec["role"    ] = role
            self.mgdDB.db_super_user.insert( super_user_rec )
        except:
            print (traceback.format_exc())
            response["message_action"] = "REGISTER_SUPERUSER_FAILED"
            response["message_action"] = "REGISTER_SUPERUSER_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def

    def get_landing_url(self, params):
        result_url = "/user/dashboard"
        try :
            menu_list = view_core_menu.view_core_menu().menu_display(params)
            if menu_list != [] :
                result_url = menu_list[0]["url"]
                
            #endif
        except : 
            print (traceback.format_exc())

        return result_url
    #end def

    import string

    def register(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "REGISTER_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            username = params["username"]
            password = params["password"]
            email = params["email"]

            # Validate password length
            if len(password) < 8:
                response["message_action"] = "REGISTER_USER_FAILED"
                response["message_code"] = "1"
                response["message_desc"] = "Password must be at least 8 characters long"
                return response

            # Validate password length
            if len(username) < 5:
                response["message_action"] = "REGISTER_USER_FAILED"
                response["message_code"] = "1"
                response["message_desc"] = "Username must be at least 5 characters long"
                return response

            # Validate username contains no punctuation
            if any(char in string.punctuation for char in username):
                response["message_action"] = "REGISTER_USER_FAILED"
                response["message_code"] = "1"
                response["message_desc"] = "Username should not contain any punctuation"
                return response

            hashed_password = utils._get_passwd_hash({
                "id": username,
                "password": password
            })

            user_rec = self.mgdDB.db_user.find_one({
                "$or": [
                    {"email": email},
                    {"username": username}
                ]
            })

            if user_rec is not None:
                response["message_action"] = "REGISTER_USER_FAILED"
                response["message_code"] = "1"
                response["message_desc"] = "Username or email already taken"
                return response
            # end if                     

            mdl_register_user = database.new(self.mgdDB, "db_user")            
            fk_user_id = mdl_register_user.get()["pkey"]

            mdl_register_user.put("fk_user_id", fk_user_id)
            mdl_register_user.put("user_uuid", str(uuid4()))
            mdl_register_user.put("username", username)
            mdl_register_user.put("email", email)
            mdl_register_user.put("name", "")
            mdl_register_user.put("role", "STUDENT")
            mdl_register_user.put("password", hashed_password)
            mdl_register_user.insert()         
        except:
            print(traceback.format_exc())
            response["message_action"] = "REGISTER_USER_FAILED"
            response["message_desc"] = "REGISTER_USER_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def

    def send_verification_email(self, params):
        result_url = "/user/dashboard"
        
        unique_4_number             = random.randint(1000,9999)
        params["unique_4_number"]   = str(unique_4_number)

        # Get the current date
        verification_date           = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create the new verification record
        ver_rec_entry = {
            "unique_4_number"       : unique_4_number,
            "verification_date"     : verification_date
        }

        # Update the document in MongoDB
        user_rec                    = self.mgdDB.db_user.update_one(
            {"fk_user_id"           : params["fk_user_id"]},
            {"$push"                : {"ver_rec": ver_rec_entry}}
        )

        #for send email
        html                        = emailproc.send_verification_email(params)

        return result_url

    
    def check_verification_email(self, params):
        result_url = "/user/dashboard"

        # Update the document in MongoDB
        user_rec                    = self.mgdDB.db_user.find_one(
            {"fk_user_id"           : params["fk_user_id"]},            
        )

        # check if input number its in a list of verification number
        list_number_verification = []
        for unique_4_number in user_rec['ver_rec']:              
            list_number_verification.append(unique_4_number['unique_4_number'])

        if int(params['unique_4_number']) in list_number_verification : 
            user_rec         = self.mgdDB.db_user.update_one(
                {"fk_user_id"         : params["fk_user_id"]}, 
                {"$set"               : {"ver_email":"TRUE"}}
            )        

        return result_url

    #end def

# end class

