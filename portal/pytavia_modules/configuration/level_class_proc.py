import config_core
import sys
import traceback
import requests
import json
import ast
import re

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
from xml.sax    import saxutils as su

class level_class_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def _add(self, params):
        response = helper.response_msg(
            "ADD_LEVEL_CLASS_SUCCESS", "ADD TERMS AND CONDITIONS SUCCESS", {} , "0000"
        )

        try:

            desc_html = su.unescape(params["desc"])

            clean = re.compile('<.*?>')
            params["desc"] = re.sub( clean, '', desc_html)

            tnc_rec  = database.new(self.mgdDB, "db_level_class")
            tnc_rec.put("level_name"     , params["level_name"        ])
            tnc_rec.put("desc_html"      , desc_html                   )
            tnc_rec.put("desc"           , params["desc"              ])        
            tnc_rec.insert()

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "ADD_LEVEL_CLASS_FAILED" )
            response.put( "desc"        , "ADD LEVEL CLASS FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def

    def _update(self, params):
        response = helper.response_msg(
            "UPDATE_LEVEL_CLASS_SUCCESS", "UPDATE TERMS AND CONDITIONS SUCCESS", {} , "0000"
        )
        try:
            
            level_class_html = su.unescape(params["level_class"])

            clean = re.compile('<.*?>')
            params["level_class"] = re.sub( clean, '', level_class_html)
            

            
            self.mgdDB.db_level_class.update_one(
                {"pkey" : params["fk_tnc_id"]},
                {"$set" : {
                    "name"                      : params["name"                 ],
                    "level_class_html" : level_class_html,
                    "level_class"      : params["level_class" ],
                    "misc"                      : params["misc"                 ],
                    "kategori"                  : params["kategori"             ]
                }
            })



        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "UPDATE_LEVEL_CLASS_FAILED" )
            response.put( "desc"        , "UPDATE LEVEL_CLASS FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })

        # end try
        return response
    # end def

    def _delete(self, params):
        response = helper.response_msg(
            "DELETE_LEVEL_CLASS_SUCCESS", "DELETE TERMS AND CONDITIONS SUCCESS", {} , "0000"
        )

        try:
            
            self.mgdDB.db_level_class.update_one(
                { "pkey" : params["fk_level_class_pkey"] },
                {"$set" : { 
                    "is_deleted" : True 
                    }
                }
            )

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "DELETE_LEVEL_CLASS_FAILED" )
            response.put( "desc"        , "DELETE TERMS AND CONDITIONS FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def



    

# end class
