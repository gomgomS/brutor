import json
import pusher
import sys
import traceback

from flask      import Flask
from xml.sax    import saxutils as su

sys.path.append("pytavia_core"    )
from pytavia_core import helper
from pytavia_core import config

app                   = Flask( __name__, config.G_STATIC_URL_PATH )
app.secret_key        = config.G_FLASK_SECRET



# Library for triggering push notification to PUSHER
# All things to do with Pusher has to be defined here.

def _get_pusher_client():
    pusher_client = None
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
        
    except :
        app.logger.debug( str(sys.exc_info()) )
    # end try
    return pusher_client
# end def

# for channel and personal
def send_notification(params) :
    response = helper.response_msg(
        "SEND_NOTIF_SUCCESS", "SEND NOTIF SUCCESS", {} , "0000"
    )
    try :
        # MANDATORY
        topic_name      = params["topic_name"   ]   # STRING 
        event_item      = params["event_item"   ]   # STRING
        
       
        judul           = ""
        short_deskripsi = ""
        url             = ""
        image           = ""

        if "judul" in params and params["judul"] != None :
            judul = su.unescape( params["judul"] )

        if "short_deskripsi" in params and params["short_deskripsi"] != None :
            short_deskripsi = su.unescape( params["short_deskripsi"] )

        if "url" in params and params["url"] != None :
            url = su.unescape( params["url"] )

        if "image" in params and params["image"] != None :
            image = params["image"]

        data_message = {
            "message_data" : {
                    "judul"           : judul,
                    "short_deskripsi" : short_deskripsi,
                    "url"             : url,
                    "image"           : image
                }
        }

        app.logger.debug( "--------------------------"              )
        app.logger.debug( "PUSHER SEND NOTIF"                     )
        app.logger.debug( "topic_name    = " + str(topic_name)      )
        app.logger.debug( "event_item    = " + str(event_item)      )
        app.logger.debug( "data_message  = " + str(data_message)    )
        app.logger.debug( "--------------------------"              )
        
        pusher_service = _get_pusher_client()

        if pusher_service == None :
            response.put( "status_code" , "1001" )
            response.put( "status"      , "SEND_NOTIF_FAILED" )
            response.put( "desc"        , "Pusher Service Error!" )
            response.put( "data"        , { "error_message" : "Pusher Service Error!" })
            return response
        # endif
        
        resp = pusher_service.trigger( 
            topic_name,
            event_item,
            data_message
        )
        app.logger.debug( "\n---------------------" )
        app.logger.debug( "PUSHER CLIENT SEND NOTIF RESP" )
        app.logger.debug( str(resp) )
        app.logger.debug( "---------------------" )

        if resp != {} :
            response.put( "status_code" , "1002" )
            response.put( "status"      , "SEND_NOTIF_FAILED" )
            response.put( "desc"        , "Pusher Client Failed, Error! Channel = " + str(topic_name) + ", Event = " + str(event_item) )
            response.put( "data"        , { "error_message" : "Pusher Service Failed" })
            return response
        # endif

        response.put("data", resp)

    except :
        trace_back_msg = traceback.format_exc() 
        print( str(trace_back_msg) )
        response.put( "status_code" , "9999" )
        response.put( "status"      , "SEND_NOTIF_FAILED" )
        response.put( "desc"        , "SEND NOTIF FAILED" )
        response.put( "data"        , { "error_message" : trace_back_msg })
    # end try
    return response
# end def