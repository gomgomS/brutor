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

class chk_server:
        
    mgdDB = database.get_db_conn(config.mainDB)
    
    def __init__(self,app):
        self.webapp = True
    # end def

    def html(self, params):
        call_id  = idgen._get_api_call_id()
        conType_view = self.mgdDB.db_content_type.find({},{
                    "_id":0,
                    "key":1,
                    "content_type":1
        })
        
        conType_list = list(conType_view)        
        return render_template(
            "chk_server.html",
            conType_list = conType_list
        )                
    # end def

# end class
