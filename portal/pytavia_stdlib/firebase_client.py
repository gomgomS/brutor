import traceback
import json
import sys


from flask      import Flask
from pyfcm      import FCMNotification
from xml.sax    import saxutils as su


sys.path.append("pytavia_core"    )

from pytavia_core import config
from pytavia_core import helper

app                   = Flask( __name__, config.G_STATIC_URL_PATH )
app.secret_key        = config.G_FLASK_SECRET



# Library for triggering push notification to Firebase
# All things to do with Firebase has to be defined here. Refer to : https://github.com/olucurious/pyfcm

def _get_firebase_client():
    firebase_service = None
    try:
        api_key = config.FIREBASE_API_KEY

        firebase_service = FCMNotification( api_key=api_key )
        
    except :
        app.logger.debug( str(sys.exc_info()) )
    # end try
    return firebase_service
# end def

def subscribe_user_to_topic(params) :
    response = helper.response_msg(
        "SUBSCRIBE_USER_TO_FIREBASE_TOPIC_SUCCESS", "SUBSCRIBE USER TO FIREBASE TOPIC SUCCESS", {} , "0000"
    )
    try :
        reg_ids = params["reg_ids"  ] # must be a list type
        topic   = params["topic"    ]
        
        firebase_service = _get_firebase_client()

        if firebase_service == None :
            response.put( "status_code" , "1001" )
            response.put( "status"      , "SUBSCRIBE_USER_TO_FIREBASE_TOPIC_FAILED" )
            response.put( "desc"        , "Firebase Service Error!" )
            response.put( "data"        , { "error_message" : "Firebase Service Error!" })
            return response
        # endif
        
        resp = firebase_service.subscribe_registration_ids_to_topic(reg_ids, topic)
        app.logger.debug( "\n---------------------" )
        app.logger.debug( "FIREBASE CLIENT TOPIC SUBSCRIPTION RESP"   )
        app.logger.debug( "fcm_token  : " + str(reg_ids)       )
        app.logger.debug( "topic name : " + str(topic  )       )
        app.logger.debug( str(resp)                            )
        app.logger.debug( "---------------------"              )
        response.put("data", {"subscribe_resp" : resp})

    except :
        trace_back_msg = traceback.format_exc() 
        app.logger.debug( str(trace_back_msg) )
        response.put( "status_code" , "9999" )
        response.put( "status"      , "SUBSCRIBE_USER_TO_FIREBASE_TOPIC_FAILED" )
        response.put( "desc"        , "SUBSCRIBE USER TO FIREBASE TOPIC FAILED" )
        response.put( "data"        , { "error_message" : trace_back_msg })
    # end try
    return response

# end def

def unsub_user_to_topic(params) :
    response = helper.response_msg(
        "SUBSCRIBE_USER_TO_FIREBASE_TOPIC_SUCCESS", "SUBSCRIBE USER TO FIREBASE TOPIC SUCCESS", {} , "0000"
    )
    try :
        reg_ids = params["reg_ids"  ] # must be a list type
        topic   = params["topic"    ]
        
        firebase_service = _get_firebase_client()

        if firebase_service == None :
            response.put( "status_code" , "1001" )
            response.put( "status"      , "SUBSCRIBE_USER_TO_FIREBASE_TOPIC_FAILED" )
            response.put( "desc"        , "Firebase Service Error!" )
            response.put( "data"        , { "error_message" : "Firebase Service Error!" })
            return response
        # endif
        
        resp = firebase_service.unsubscribe_registration_ids_from_topic(reg_ids, topic)
        app.logger.debug( "\n------------------------------------"  )
        app.logger.debug( "FIREBASE CLIENT TOPIC UNSUBSCRIBE RESP"  )
        app.logger.debug( "fcm_token  : " + str(reg_ids)            )
        app.logger.debug( "topic name : " + str(topic  )            )
        app.logger.debug( str(resp)                                 )
        app.logger.debug( "---------------------"                   )
        response.put("data", {"firebase_resp" : resp})

    except :
        trace_back_msg = traceback.format_exc() 
        app.logger.debug( str(trace_back_msg) )
        response.put( "status_code" , "9999" )
        response.put( "status"      , "SUBSCRIBE_USER_TO_FIREBASE_TOPIC_FAILED" )
        response.put( "desc"        , "SUBSCRIBE USER TO FIREBASE TOPIC FAILED" )
        response.put( "data"        , { "error_message" : trace_back_msg })
    # end try
    return response

# end def



# send notification for channel
def send_topic_notification(params) :
    response = helper.response_msg(
        "SEND_TOPIC_NOTIF_SUCCESS", "SEND TOPIC NOTIF SUCCESS", {} , "0000"
    )
    try :
        # mandatory
        topic_name      = params["topic_name"   ]   # STRING | NONE 
        
        # ONLY FOR MRTJ-APPS, generalized additional params
        # OPTIONAL
        judul           = ""
        short_deskripsi = ""
        url             = ""
        image           = ""
        event_name      = ""

        if "judul" in params and params["judul"] != None :
            judul = su.unescape( params["judul"] )

        if "short_deskripsi" in params and params["short_deskripsi"] != None :
            short_deskripsi = su.unescape( params["short_deskripsi"])

        if "url" in params and params["url"] != None :
            url = su.unescape( params["url"] )

        if "image" in params and params["image"] != None :
            image = params["image"]

        if "event_name" in params and params["event_name"] != None :
            event_name = params["event_name"]

        data_message = {
            "data" : {
                "header_version": "1.0",
                "cmd"           : "notif",
                "channel_name"  : topic_name,
                "event_name"    : event_name,
                "message_data"  : {
                    "judul"           : judul,
                    "short_deskripsi" : short_deskripsi,
                    "url"             : url,
                    "image"           : image
                }
            }
        }

        app.logger.debug( "--------------------------"              )
        app.logger.debug( "FIREBASE SEND TOPIC NOTIF"               )
        app.logger.debug( "topic_name    = " + str(topic_name)      )
        app.logger.debug( "message_title = " + str(judul)           )
        app.logger.debug( "message_body  = " + str(short_deskripsi) )
        app.logger.debug( "message_icon  = " + str(image)           )
        app.logger.debug( "data_message  = " + str(data_message)    )
        app.logger.debug( "--------------------------"              )
        
        firebase_service = _get_firebase_client()

        if firebase_service == None :
            response.put( "status_code" , "1001" )
            response.put( "status"      , "SEND_TOPIC_NOTIF_FAILED" )
            response.put( "desc"        , "Firebase Service Error!" )
            response.put( "data"        , { "error_message" : "Firebase Service Error!" })
            return response
        # endif
        
        resp = firebase_service.notify_topic_subscribers(
            topic_name      = topic_name,
            message_title   = judul,
            message_body    = short_deskripsi,
            message_icon    = image,
            data_message    = data_message
        )
        app.logger.debug( "\n---------------------" )
        app.logger.debug( "FIREBASE CLIENT SEND NOTIF TOPIC RESP" )
        app.logger.debug( str(resp) )
        app.logger.debug( "---------------------" )
        response.put("data", resp)

    except :
        trace_back_msg = traceback.format_exc() 
        print( str(trace_back_msg) )
        response.put( "status_code" , "9999" )
        response.put( "status"      , "SEND_TOPIC_NOTIF_FAILED" )
        response.put( "desc"        , "SEND TOPIC NOTIF FAILED" )
        response.put( "data"        , { "error_message" : trace_back_msg })
    # end try
    return response
# end def

# send notification for single device/token
def send_single_device_notification(params) :
    response = helper.response_msg(
        "SEND_SINGLE_DEVICE_NOTIF_SUCCESS", "SEND SINGLE DEVICE NOTIF SUCCESS", {} , "0000"
    )
    try :
        # MANDATORY
        reg_id          = params["reg_id"       ]   # STRING | NONE
        
        # ONLY FOR MRTJ-APPS, generalized additional params
        # OPTIONAL
        judul           = ""
        short_deskripsi = ""
        url             = ""
        image           = ""
        event_name      = ""
        topic_name      = "personal"

        if "judul" in params and params["judul"] != None :
            judul = su.unescape( params["judul"] )

        if "short_deskripsi" in params and params["short_deskripsi"] != None :
            short_deskripsi = su.unescape( params["short_deskripsi"] )

        if "url" in params and params["url"] != None :
            url = su.unescape( params["url"] )

        if "image" in params and params["image"] != None :
            image = params["image"]

        if "event_name" in params and params["event_name"] != None :
            event_name = params["event_name"]

        if "topic_name" in params and params["topic_name"] != None :
            topic_name = params["topic_name"]

        data_message = {
            "data" : {
                "header_version": "1.0",
                "cmd"           : "notif",
                "channel_name"  : topic_name,
                "event_name"    : event_name,
                "message_data"  : {
                    "judul"           : judul,
                    "short_deskripsi" : short_deskripsi,
                    "url"             : url,
                    "image"           : image
                }
            }
        }

        app.logger.debug( "--------------------------"              )
        app.logger.debug( "FIREBASE SEND SINGLE DEVICE NOTIF"         )
        app.logger.debug( "FCM TOKEN     = " + str(reg_id)          )
        app.logger.debug( "message_title = " + str(judul)           )
        app.logger.debug( "message_body  = " + str(short_deskripsi) )
        app.logger.debug( "message_icon  = " + str(image)           )
        app.logger.debug( "data_message  = " + str(data_message)    )
        app.logger.debug( "--------------------------"              )
        
        firebase_service = _get_firebase_client()

        if firebase_service == None :
            response.put( "status_code" , "1001" )
            response.put( "status"      , "SEND_SINGLE_DEVICE_NOTIF_FAILED" )
            response.put( "desc"        , "Firebase Service Error!" )
            response.put( "data"        , { "error_message" : "Firebase Service Error!" })
            return response
        # endif

        resp = firebase_service.notify_single_device(
            registration_id = reg_id,
            message_title   = judul,
            message_body    = short_deskripsi,
            message_icon    = image,
            data_message    = data_message
        )

        app.logger.debug( "\n---------------------" )
        app.logger.debug( "FIREBASE CLIENT SEND SINGLE DEVICE RESP" )
        app.logger.debug( str(resp) )
        app.logger.debug( "---------------------" )
        response.put("data", resp)

    except :
        trace_back_msg = traceback.format_exc() 
        print( str(trace_back_msg) )
        response.put( "status_code" , "9999" )
        response.put( "status"      , "SEND_SINGLE_DEVICE_NOTIF_FAILED" )
        response.put( "desc"        , "SEND SINGLE DEVICE NOTIF FAILED" )
        response.put( "data"        , { "error_message" : trace_back_msg })
    # end try
    return response

# end def

# send notification for multiple devices/tokens
def send_multiple_device_notification(params) :
    response = helper.response_msg(
        "SEND_MULTIPLE_DEVICE_NOTIF_SUCCESS", "SEND MULTIPLE DEVICE NOTIF SUCCESS", {} , "0000"
    )
    try :
        # MANDATORY
        reg_ids         = params["reg_ids"]   # STRING | NONE
        
        # ONLY FOR MRTJ-APPS, generalized additional params
        # OPTIONAL
        judul           = ""
        short_deskripsi = ""
        url             = ""
        image           = ""
        event_name      = ""
        topic_name      = "personal"

        if "judul" in params and params["judul"] != None :
            judul = su.unescape( params["judul"] )

        if "short_deskripsi" in params and params["short_deskripsi"] != None :
            short_deskripsi = su.unescape( params["short_deskripsi"] )

        if "url" in params and params["url"] != None :
            url = su.unescape( params["url"] )

        if "image" in params and params["image"] != None :
            image = params["image"]

        if "event_name" in params and params["event_name"] != None :
            event_name = params["event_name"]

        if "topic_name" in params and params["topic_name"] != None :
            topic_name = params["topic_name"]

        data_message = {
            "data" : {
                "header_version": "1.0",
                "cmd"           : "notif",
                "channel_name"  : topic_name,
                "event_name"    : event_name,
                "message_data"  : {
                    "judul"           : judul,
                    "short_deskripsi" : short_deskripsi,
                    "url"             : url,
                    "image"           : image
                }
            }
        }

        app.logger.debug( "--------------------------"              )
        app.logger.debug( "FIREBASE SEND MULTIPLE DEVICE NOTIF"         )
        app.logger.debug( "FCM TOKEN     = " + str(reg_ids)          )
        app.logger.debug( "message_title = " + str(judul)           )
        app.logger.debug( "message_body  = " + str(short_deskripsi) )
        app.logger.debug( "message_icon  = " + str(image)           )
        app.logger.debug( "data_message  = " + str(data_message)    )
        app.logger.debug( "--------------------------"              )
        
        firebase_service = _get_firebase_client()

        if firebase_service == None :
            response.put( "status_code" , "1001" )
            response.put( "status"      , "SEND_MULTIPLE_DEVICE_NOTIF_FAILED" )
            response.put( "desc"        , "Firebase Service Error!" )
            response.put( "data"        , { "error_message" : "Firebase Service Error!" })
            return response
        # endif

        resp = firebase_service.notify_multiple_devices(
            registration_ids = reg_ids,
            message_title    = judul,
            message_body     = short_deskripsi,
            message_icon     = image,
            data_message     = data_message
        )

        app.logger.debug( "\n---------------------" )
        app.logger.debug( "FIREBASE CLIENT SEND MULTIPLE DEVICE RESP" )
        app.logger.debug( str(resp) )
        app.logger.debug( "---------------------" )
        response.put("data", resp)

    except :
        trace_back_msg = traceback.format_exc() 
        print( str(trace_back_msg) )
        response.put( "status_code" , "9999" )
        response.put( "status"      , "SEND_MULTIPLE_DEVICE_NOTIF_FAILED" )
        response.put( "desc"        , "SEND MULTIPLE DEVICE NOTIF FAILED" )
        response.put( "data"        , { "error_message" : trace_back_msg })
    # end try
    return response

# end def
