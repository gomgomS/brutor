import config_core
import sys
import traceback
import json
import ast
import time
import random
import re
from datetime import datetime

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib     import idgen
from pytavia_stdlib     import utils
from pytavia_core       import database
from pytavia_core       import config
from pytavia_core       import helper
from pytavia_stdlib     import cfs_lib
from xml.sax            import saxutils as su


class enroll_myclass_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def


    def buy_enroll_myclass(self, params):    
        result_url = "/enrollMyClass" 
      
        print(params)
        print("wow")

        # Get the current date
        today_date           = datetime.now().strftime('%Y-%m-%d %H:%M:%S')       

        enrollment_rec  = database.new(self.mgdDB, "db_enrollment")
        enrollment_rec.put("enrollment_id",                  enrollment_rec.get()["pkey"                  ])
        enrollment_rec.put("fk_user_id",                     params["fk_user_id"              ]) #pkey from db_user
        enrollment_rec.put("activation_class_id",            params["activation_class_id"     ])
        enrollment_rec.put("enrollment_date",                today_date  )        
        enrollment_rec.put("enrollment_status",              "REGISTERED"  )        
        enrollment_rec.insert()                       
                
        return result_url

        
# end class
