import config_core
import sys
import traceback
import json
import ast
import time
import random
import re
from datetime           import datetime
import string

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



class topup_proc:
    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def topup_submit(self, params):    
        result_url = "/topup"
        
        # Get the current date
        apply_date           = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
        reference_id = self.generate_reference_id()
             
        meeting_rec   = database.new(self.mgdDB, "db_topup_request")
        meeting_rec.put("topup_request_id",           meeting_rec.get()["pkey"          ])        
        meeting_rec.put("request_user_id",            params["fk_user_id" ]               ) #pkey from db_user
        meeting_rec.put("amount",                     int(params["amount"             ]))
        meeting_rec.put("request_status",             "PENDING")
        meeting_rec.put("request_date",               apply_date )
        meeting_rec.put("payment_method",             params["payment_method" ])
        meeting_rec.put("reference_id",               reference_id)
        meeting_rec.put("created_at",                 apply_date)            
        meeting_rec.put("update_by_admin_at",         "")   
        meeting_rec.put("source",                     "source/example.txt")
        meeting_rec.insert()   

        return result_url

    def generate_reference_id(self, prefix='TOPUP'):
        # Get current date in YYYYMMDD format
        today_date = datetime.now().strftime('%Y%m%d')
        
        # Generate random alphanumeric string
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        # Concatenate parts to form transaction ID
        reference_id = f"{prefix}_{today_date}_{random_chars}"
        
        return reference_id        

# end class
