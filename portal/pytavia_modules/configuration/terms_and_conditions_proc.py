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

class terms_and_conditions_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def _add(self, params):
        response = helper.response_msg(
            "ADD_TERMS_AND_CONDITIONS_SUCCESS", "ADD TERMS AND CONDITIONS SUCCESS", {} , "0000"
        )

        try:

            terms_and_conditions_html = su.unescape(params["terms_and_conditions"])

            clean = re.compile('<.*?>')
            params["terms_and_conditions"] = re.sub( clean, '', terms_and_conditions_html)

            tnc_rec  = database.new(self.mgdDB, "db_terms_and_conditions")
            tnc_rec.put("name"                      , params["name"                   ])
            tnc_rec.put("terms_and_conditions_html" , terms_and_conditions_html       )
            tnc_rec.put("terms_and_conditions"      , params["terms_and_conditions"   ])
            tnc_rec.put("misc"                      , params["misc"                   ])
            tnc_rec.put("kategori"                  , params["kategori"               ])
            tnc_rec.insert()

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "ADD_TERMS_AND_CONDITIONS_FAILED" )
            response.put( "desc"        , "ADD TERMS AND CONDITIONS FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def

    def _update(self, params):
        response = helper.response_msg(
            "UPDATE_TERMS_AND_CONDITIONS_SUCCESS", "UPDATE TERMS AND CONDITIONS SUCCESS", {} , "0000"
        )
        try:
            
            terms_and_conditions_html = su.unescape(params["terms_and_conditions"])

            clean = re.compile('<.*?>')
            params["terms_and_conditions"] = re.sub( clean, '', terms_and_conditions_html)
            

            
            self.mgdDB.db_terms_and_conditions.update_one(
                {"pkey" : params["fk_tnc_id"]},
                {"$set" : {
                    "name"                      : params["name"                 ],
                    "terms_and_conditions_html" : terms_and_conditions_html,
                    "terms_and_conditions"      : params["terms_and_conditions" ],
                    "misc"                      : params["misc"                 ],
                    "kategori"                  : params["kategori"             ]
                }
            })



        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "UPDATE_TERMS_AND_CONDITIONS_FAILED" )
            response.put( "desc"        , "UPDATE TERMS_AND_CONDITIONS FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })

        # end try
        return response
    # end def

    def _delete(self, params):
        response = helper.response_msg(
            "DELETE_TERMS_AND_CONDITIONS_SUCCESS", "DELETE TERMS AND CONDITIONS SUCCESS", {} , "0000"
        )

        try:
            
            self.mgdDB.db_terms_and_conditions.update_one(
                { "pkey" : params["fk_terms_and_conditions_pkey"] },
                {"$set" : { 
                    "is_deleted" : True 
                    }
                }
            )

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "DELETE_TERMS_AND_CONDITIONS_FAILED" )
            response.put( "desc"        , "DELETE TERMS AND CONDITIONS FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def



    

# end class
