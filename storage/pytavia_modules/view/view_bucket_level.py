import sys
import traceback

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

sys.path.append("pytavia_modules/view" )

from flask          import render_template
from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config

class view_bucket_level:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self,app):
        self.webapp = app
    # end def

    def bucket(self, params):
        bucket_public_view  = self.mgdDB.db_bucket.find({"public" : 1})
        bucket_view         = self.mgdDB.db_bucket.find({})
        bucket_list         = list( bucket_view )
        response            = { 
            "bucket_list"  : bucket_list,
            "bucket_count" : len( bucket_list ),
            "bucket_public": bucket_public_view.count()
        }
        return response
    # end def

    def html(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "DISPLAY_TEMPLATE_SUCCESS",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            display_bucket  = self.bucket( params ) 
            bucket_list     = display_bucket["bucket_list"  ]
            bucket_count    = display_bucket["bucket_count" ]
            bucket_public   = display_bucket["bucket_public"]
            return render_template(
                "bucket.html",
                bucket_list   = bucket_list,
                bucket_count  = bucket_count,
                bucket_public = bucket_public
            )                
        except:
            self.webapp.logger.debug (traceback.format_exc())
            response["message_action"] = "DISPLAY_TEMPLATE_FAILED"
            response["message_action"] = "DISPLAY_TEMPLATE_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
# end class
