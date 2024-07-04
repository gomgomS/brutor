import time
import copy
import pymongo
import os
import sys

from bson.objectid import ObjectId

class mongo_model:

    def __init__(self, record, lookup, db_handle):
        self._mongo_record  = copy.deepcopy(record)
        self._lookup_record = copy.deepcopy(lookup)
        self._db_handle     = db_handle
    # end def

    def put(self, key, value):
        if not (key in self._lookup_record):
            raise ValueError('SETTING_NON_EXISTING_FIELD', key, value)
        # end if
        self._mongo_record[key] = value
    # end def

    def get(self):
        return self._mongo_record
    # end def   

    def delete(self , query):
        collection_name = self._lookup_record["__db__name__"]
        self._db_handle[collection_name].remove( query )
    # end def

    def insert(self, lock=None):
        collection_name = self._lookup_record["__db__name__"]
        del self._mongo_record["__db__name__"]
        # if 
        #if not(collection_name in self._db_handle.list_collection_names()):
        #    self._db_handle.create_collection( collection_name )
        # end if
        if lock == None:
            self._db_handle[collection_name].insert_one(  
                self._mongo_record
            )
        else:
            self._db_handle[collection_name].insert_one(  
                self._mongo_record,
                session=lock
            )
        # end if
    # end def

    def update(self, query):
        collection_name = self._lookup_record["__db__name__"]
        self._db_handle[collection_name].update(
            query, 
            { "$set" : self._mongo_record }
        )
    # end def
# end class
#
#
# Define the models/collections here for the mongo db
#
db = {
    
    "db_config_all" : {
        "name"                  : "",
        "add_url"               : "",
        "edit_url"              : "",
        "value"                 : "",
        "count"                 : 0 ,
        "desc"                  : "",
        "type"                  : "", # MENU PERMISSION | ETC
        # additional
        "misc"                  : "",
        "bo_access"             : "FALSE", # TRUE | FALSE  | give access to back office
        "bo_access_2"           : "FALSE"  # TRUE | FALSE  | give access to back office
    },

    "db_config_general" : {
        "name"                  : "",
        "value"                 : "",
        "order"                 : 0 ,
        "status"                : "ENABLE",
        "desc"                  : "",
        "misc"                  : "",
    },

    "db_config_menu_webapp_handler" : {
        "name"                  : "",
        "value"                 : "",
        "href"                  : "",
        "status"                : "ENABLE",
        "fk_menu_id"            : "CONFIGURATION"
    },

    "db_config_menu_webapp_item_all" : {
        "name"                  : "",
        "value"                 : "",
        "order"                 : 0 ,
        "href"                  : "",
        "status"                : "ENABLE",
        "icon"                  : "",
        "description"           : ""
    },

    "db_config_privilege" : {
        "name"                  : "",
        "value"                 : "",
        "order"                 : 0 ,
        "status"                : "ENABLE",
        "misc"                  : "",
        "desc"                  : ""
    },

    "db_config_role" : {
        "name"                  : "",
        "value"                 : "",
        "order"                 : 0 ,
        "status"                : "ENABLE",
        "user_type"             : "BO", # additional for user type
        "misc"                  : "",
        "desc"                  : ""
    },

    "db_config_webapp_menu_privilege" : {
        "name"                  : "",
        "value"                 : "",
        "order"                 : 0 ,
        "status"                : "ENABLE",
        "fk_privilege_id"       : "SELECT PRIVILEGE",
        "fk_menu_id"            : "SELECT MENU",
        "desc"                  : ""
    },

    "db_config_webapp_role_privilege" : {
        "name"                  : "",
        "value"                 : "",
        "order"                 : 0 ,
        "status"                : "ENABLE",
        "fk_privilege_id"       : "SELECT PRIVILEGE",
        "fk_role_id"            : "SELECT ROLE"
    },

    "db_config_webapp_route_privileges" : {
        "name"                  : "", # this for route action name (for logging), display as privilege text
        "value"                 : "", # this value as ROUTE_NAME, should be Unique
        "href"                  : "", # route url
        "order"                 : 0 , # use order to sort side menu list
        "route_type"            : "", # MENU | PAGE | PROCESS ( PROCESS UPDATE, PROCESS EDIT, PROCESS DELETE, etc  )
        "status"                : "ENABLE",
        "misc"                  : "",
        "desc"                  : "" ,
        # for route_type MENU only
        "display_text"          : "", # display as MENU text
        "icon"                  : "", # icon for MENU
        "bo_access"             : "TRUE", # give privilege to Back Office, default TRUE, update in CMS
    },

    "db_cookies" : {
        "fk_user_id"            : "",
        "cookie_id"             : "",
        "user_agent"            : {},
        "referrer"              : "",
        "x_forward_for"         : "",
        "username"              : "",
        "expire_time"           : "",
        "active"                : "", # TRUE | FALSE  
    },

    "db_log_login_auth" : {
        "fk_user_id"            : "" ,
        "usernmae"              : "",
        "desc"                  : "",
        "state"                 : "LOGIN_FAILED", # LOGIN_FAILED | LOGIN_SUCCESS,
    },

    "db_role_parent_to_child_mapping" : {
        "name"                  : "",
        "value"                 : "",
        "status"                : "ENABLE",
        "parent_role_val"       : "",
        "child_role_val"        : "",
        "desc"                  : "",
    },

    "db_security_api_core" : {
        "api_key"               : "",
        "api_secret"            : "",
        "active"                : "TRUE",
        "description"           : ""
    },
    
    "db_security_cfs" : {
        "token_value"           : "",
        "username"              : "",
        "password"              : "",
        "expire_time"           : "",
        "active"                : "TRUE"
    }, 
    
    "db_security_user" : {
        "token_value"           : "",
        "username"              : "",
        "password"              : "",
        "expire_time"           : "",
        "active"                : "TRUE"
    },

    "db_session" : {
        "fk_user_id"            : "",
        "login_time"            : 0 
    },

    "db_setting_app" : {
        "idle_account"          : "",
        "force_change_password" : "",
        "password_history"      : "",
        "password_length"       : "",
        "variable_password"     : { 
            "numeric"               : "FALSE",  # <TRUE> | <FALSE>
            "lower_case"            : "FALSE",  # <TRUE> | <FALSE>
            "upper_case"            : "FALSE",  # <TRUE> | <FALSE>
            "symbol"                : "FALSE",  # <TRUE> | <FALSE>
            "symbol_str"            : ""
        },
        "wrong_counter"         : "",
        "limit_history_password": 0,
        "screen_timeout"        : 0,
        "tran_timeout"          : 0,
    },

    "db_system_activity_logging" : {
        "client_type"           : "",
        "action"                : "",
        "description"           : "",
        "action_time"           : "",
        "call_id"               : "",
        "request"               : "",
        "response"              : "",
        "fk_user_id"            : "",
        "portal_type"           : "",
        "merchant_id"           : "",
        "user_role"             : "",
        "username"              : "",
        "activity_data"         : "",
    },

    "db_unique_counter" : {
        "counter"               : 0,
    },

    "db_random_config" : {
        "config_name"           : "check_gapeka_api_status",
        "check_gpk_api_status"  : "off",
    },

    "db_config"                    : {
        "_id"                   : ObjectId(),
        "name"                  : "",
        "value"                 : "",
        "desc"                  : "",
        "config_type"           : "",
        "misc"                  : "",
        "data"                  : {}
    },

    "db_menu"                   : {
        "_id"                   : ObjectId(),
        "menu_name"             : "",
        "value"                 : "",
        "icon_class"            : "",
        "url"                   : "",
        "position"              : "",
        "desc"                  : "",
        "rec_timestamp"         : ""
    },

    "db_starter"                   : {
        "_id"                   : ObjectId(),
        "menu_value"            : "",
        "name"                  : "",
        "value"                 : "",
        "icon_class"            : "",
        "url"                   : "",
        "position"              : "",
        "desc"                  : "",
        "rec_timestamp"         : ""
    },

    "db_menu_permission"        : {
        "_id"                   : ObjectId(),
        "role_position_value"   : "",
        "menu_value"            : "",
        "desc"                  : "",
        "rec_timestamp"         : ""
    },

    "db_super_user" : {
        "username"              : "",
        "password"              : "",
        "role"                  : "ADMIN",
    },

    # USERS

    "db_user"                         : {
        "fk_user_id"                : "",
        "user_uuid"                 : "",
        "username"                  : "",
        "password"                  : "",
        "role"                      : "STUDENT", # TUTOR | STUDENT | ADMIN
        "name"                      : "",
        "phone"                     : "",
        "email"                     : "",
        "ver_email"                 : "FALSE",
        'ver_rec'                   : [],
        "saldo"                     : "",
        "rec_transaction"           : [],
        "last_login"                : "",
        "str_last_login"            : "",       
        "login_status"              : "",      # TRUE | FALSE
        "inactive_status"           : "FALSE", # TRUE | FALSE
        "lock_status"               : "FALSE", # TRUE | FALSE
        "lock_note"                 : "",
        "image"                     : "",
        "register_student"          : "TRUE",   # TRUE | FALSE
        "register_teacher"          : "FALSE",  # TRUE | FALSE
    },

    # CLASS REGISTER
    "db_class"                      : {                
        "class_id"                  : "",
        "creator_id"                : "",
        "level_id"                  : "",
        "name_class"                : "",
        "desc_class"                : "",
        "desc_class_html"           : "",
        "desc_class_preview"        : "",
        "status_class"              : "",       # OPEN_SHARING(another can open this class),PRIVATE(creator only), COMMINGSOON(still development), MAINTENENCE (improvement)
        "prerequisite_class_id"     : [],       # fill with pkey for certain class should pass
        "pass_requirement"          : "",       # desc for pass the class
        "pass_requirement_html"     : "",       #
        "pass_requirement_preview"  : "",       #
        "price_class"               : ""
    },

    # CLASS ACTIVATION
    "db_activation_class"         : {         
        "activation_class_id"       : "",
        "active_class_name"         : "",       #
        "class_id"                  : "",
        "activate_timestamp"        : "",
        "str_activate_timestamp"    : "",
        "student_limit"             : "",       # LIMIT MAX STUDENT CAN JOIN
        "can_just_test_to_pass"     : "FALSE",  # TRUE | FALSE
        "price_class"               : "",
        "status_activation"         : "",       # OPEN_REGISTRATION, RUNNING, FINISHED
        "prerequisite_class_id"     : [],       # fill with pkey for certain class should pass
        "auto_close_reg_kuota"      : "FALSE",       # TRUE(if kuota full registration close automatic) | FALSE
        "auto_close_reg_status"     : "FALSE",       # TRUE(if status running close automatic) | FALSE
        "total_meeting"             : 0,
        "total_test"                : 0
    },

    # TEST
    "db_test"                       : {      
        "test_id"                   : "",              
        "activation_class_id"       : "",    
        "name_test"                 : "",       
        "desc_test"                 : "",    
        "desc_test_html"            : "",       # 
        "desc_test_preview"         : "",       #         
        "score_to_pass"             : "",   
        "start_timestamp"           : 0,
        "end_timestamp"             : 0,
        "str_start_datetime"        : "", 
        "str_end_datetime"          : "",
        "type_test"                 : "",       # PDF, GOOGLE TEST, LIVE CODE 
        "source"                    : "",       # can be link, or source file             
    },   

     # MEETING
    "db_meeting"                    : {      
        "meeting_id"                : "",              
        "activation_class_id"       : "",    
        "name_meeting"              : "",       
        "desc_meeting"              : "",    
        "desc_meeting_html"         : "",       # 
        "desc_meeting_preview"      : "",       #                 
        "start_timestamp"           : 0,
        "end_timestamp"             : 0,
        "str_start_datetime"        : "", 
        "str_end_datetime"          : "",    
        "source"                    : "",       # can be link, or source file             
    },   

    # CLASS LEVEL
    "db_level_class"                : {        
        "level_name"                : "",       
        "desc"                      : "",
        "desc_html"                 : "",
    },

    # PENGELOLAAN KONTEN
    "db_konten"                     : {
        "konten_id"                 : "",
        "fk_user_id"                : "",
        "fk_perusahaan_id"          : "", # Perusahaan
        "perusahaan_name"           : "",
        "posisi_name"               : "",
        "jenis_tampilan_name"       : "", 
        "fk_posisi_value"           : "", # CONFIG - POSISI DI APLIKASI
        "fk_jenis_tampilan_value"   : "", # CONFIG - JENIS TAMPILAN
        "urutan"                    : 0,
        "judul_konten"              : "",
        "deskripsi"                 : "",
        "deskripsi_html"            : "",
        "deskripsi_preview"         : "",
        "url"                       : "", 
        "start_timestamp"           : 0,
        "end_timestamp"             : 0,
        "str_start_datetime"        : "", 
        "str_end_datetime"          : "", 
        "image"                     : "",
        "status_value"              : "" # PROSES - TAYANG - SELASAI
    },

    "db_konten_img"                 : {
        "fk_konten_id"              : "",
        "image"                     : ""
    },

    "db_konten_status_history"      : {
        "fk_user_id"                : "",
        "fk_konten_id"              : "",
        "status_value"              : "",
        "update_from"               : ""
    },

    "db_update_konten_history"      : {
        "fk_user_id"                : "",
        "fk_konten_id"              : "",
        "update_notes"              : "",
        "rec_before"                : {
            "fk_perusahaan_id"      : "", # Perusahaan
            "fk_posisi_value"       : "", # CONFIG - POSISI DI APLIKASI
            "fk_jenis_tampilan_value": "",# CONFIG - JENIS TAMPILAN
            "perusahaan_name"       : "",
            "posisi_name"           : "",
            "jenis_tampilan_name"   : "",
            "urutan"                : 0,
            "judul_konten"          : "",
            "deskripsi"             : "",
            "deskripsi_html"        : "",
            "url"                   : "", 
            "start_timestamp"       : 0,
            "end_timestamp"         : 0,
            "str_start_datetime"    : "", 
            "str_end_datetime"      : "",
            "image"                 : ""
        },
        "rec_after"                 : {
            "fk_perusahaan_id"      : "", # Perusahaan
            "fk_posisi_value"          : "", # CONFIG - POSISI DI APLIKASI
            "fk_jenis_tampilan_value"  : "", # CONFIG - JENIS TAMPILAN
            "perusahaan_name"       : "",
            "posisi_name"           : "",
            "jenis_tampilan_name"   : "",
            "urutan"                : 0,
            "judul_konten"          : "",
            "deskripsi"             : "",
            "deskripsi_html"        : "",
            "url"                   : "", 
            "start_timestamp"       : 0,
            "end_timestamp"         : 0,
            "str_start_datetime"    : "", 
            "str_end_datetime"      : "",
            "image"                 : ""
        } 
    },



}
