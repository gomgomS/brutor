import sys
import time
import traceback
import datetime
import hashlib

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config

import security_proc

class security_gateway:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    """
        For login fk_user_id is sent as the username
            but for all the other calls its all using 
                fk_user_id
    """
    def login(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "VERIFY_SUCCESS",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            pass
        except:
            pass
        # end try
        return response
    # end def

    def _put_file(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "VERIFY_SUCCESS",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        headers    = params ["headers"      ]
        token      = headers["auth-token"   ]
        label      = headers["auth-label"   ]   
        fk_user_id = params ["fk_user_id"   ]
        key        = params ["key"          ]
        bucket     = params ["bucket"       ]
        extension  = params ["extension"    ]     
        conType    = params ["conType"      ]   
        p_label    = params ["label"        ]   
        try:
            calc_token    = security_proc.security_proc(self.webapp).request_security_token({
                "fk_user_id"    : fk_user_id,
                "sequence"      : key + bucket + p_label + extension + conType + fk_user_id ,
                "label"         : label
            })
            self.webapp.logger.debug("calc_token : "+calc_token)
            self.webapp.logger.debug("token      : "+token)
            if calc_token != token:
                response["message_action"] = "VERIFY_FAILED"
            # end if
        except:
            self.webapp.logger.debug (traceback.format_exc())
            response["message_action"] = "VERIFY_FAILED"
            response["message_action"] = "VERIFY_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
    
    def _get_file(self,params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "VERIFY_SUCCESS",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        headers    = params ["headers"      ]
        token      = headers["auth-token"   ]
        label      = headers["auth-label"   ]   
        fk_user_id = params ["fk_user_id"   ]
        key        = params ["key"          ]
        bucket     = params ["bucket"       ]
        try:
            calc_token    = security_proc.security_proc(self.webapp).request_security_token({
                "fk_user_id"    : fk_user_id,
                "sequence"      : str(bucket) + fk_user_id + str(key)  ,
                "label"         : label
            })
            self.webapp.logger.debug("calc_token : "+calc_token)
            self.webapp.logger.debug("token      : "+token)
            if calc_token != token:
                response["message_action"] = "VERIFY_FAILED"
            # end if
        except:
            self.webapp.logger.debug (traceback.format_exc())
            response["message_action"] = "VERIFY_FAILED"
            response["message_action"] = "VERIFY_FAILED: " + str(sys.exc_info())
        # end try
        return response
    
