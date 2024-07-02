import config_core
import sys
import traceback
import requests
import json
import ast

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib   import idgen
from pytavia_stdlib   import utils
from pytavia_core     import database
from pytavia_core     import config
from pytavia_core     import helper

class config_notif_event_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def


    def _add(self, params):
        response = helper.response_msg(
            "ADD_NOTIF_EVENT_SUCCESS", "ADD NOTIF EVENT SUCCESS", {} , "0000"
        )
        try:

            channel_rec = self.mgdDB.db_config.find_one({"config_type" : "CHANNEL", "value" : params["fk_channel_value"], "is_deleted" : False })

            notif_event_rec  = database.new(self.mgdDB, "db_notif_event")
            notif_event_rec.put("fk_channel_value", params["fk_channel_value"   ])
            notif_event_rec.put("channel_name",     channel_rec["name"          ])
            notif_event_rec.put("event" ,           params["event"              ])
            notif_event_rec.put("desc",             params["desc"               ])
            notif_event_rec.insert()


        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "ADD_NOTIF_EVENT_FAILED" )
            response.put( "desc"        , "ADD NOTIF EVENT FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def
    
    def _edit(self, params):
        response = helper.response_msg(
            "UPDATE_NOTIF_EVENT_SUCCESS", "UPDATE NOTIF EVENT SUCCESS", {} , "0000"
        )
        try:

            channel_rec = self.mgdDB.db_config.find_one({"config_type" : "CHANNEL", "value" : params["fk_channel_value"], "is_deleted" : False })
            
            self.mgdDB.db_notif_event.update(
                {"pkey" : params["fk_notif_event_id"]},
                {"$set" : {
                    "fk_channel_value"  : params["fk_channel_value"     ],
                    "channel_name"      : channel_rec["name"            ],
                    "event"             : params["event"                ],
                    "desc"              : params["desc"                 ]
                }
            })


        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "UPDATE_NOTIF_EVENT_FAILED" )
            response.put( "desc"        , "UPDATE NOTIF EVENT FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def

    def _delete(self, params):
        response = helper.response_msg(
            "DELETE_NOTIF_EVENT_SUCCESS", "DELETE NOTIF EVENT SUCCESS", {} , "0000"
        )
        try:
            
            self.mgdDB.db_notif_event.delete_one(
                { "pkey" : params["fk_notif_event_id"] },
            )

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "DELETE_NOTIF_EVENT_FAILED" )
            response.put( "desc"        , "DELETE NOTIF EVENT FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def


# end class
