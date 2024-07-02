import boto
import json
import pusher
import sys

sys.path.append("pytavia_core"    )

from pytavia_core import config

class pusher_client_proc:

    def __init__(self):
        pass
    
    def _get_pusher_client(self):
        response = {
            "message_action" : "GET_PUSHER_CLIENT_SUCCESS",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            app_id      = config.PUSHER_APP_ID
            app_key     = config.PUSHER_APP_KEY
            secret_key  = config.PUSHER_SECRET_KEY
            cluster     = config.PUSHER_CLUSTER

            pusher_client = pusher.Pusher(
                app_id  = app_id, 
                key     = app_key, 
                secret  = secret_key,
                cluster = cluster
                )
            
            response["message_data"] = {
                "pusher_client" : pusher_client
            }
            
        except :
            response["message_action"   ] = "GET_PUSHER_CLIENT_FAILED"
            response["message_desc"     ] = "GET_PUSHER_CLIENT_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def