import config_core
import sys
import traceback
import json
import ast
import time
import random
import re
from   datetime import datetime

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


class payment_confirmation_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def


    def _find_request_topup(self,params):                                         
        topup_request_rec = self.mgdDB.db_topup_request.find_one({
            "topup_request_id" : params['topup_request_id']
        })
        
        response =  topup_request_rec
        return response

    def topup(self, params):    
        result_url = "/payment_confirmation"

        # FIND REQUEST TOPUP
        topup_request_rec                     = self._find_request_topup( params )     

        # Get the current date
        today_date           = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    

        # Insert new top transaction in to db_topup_transaction
        topup_transaction_rec   = database.new(self.mgdDB, "db_topup_transaction")
        topup_transaction_rec.put("topup_transaction_id",           topup_transaction_rec.get()["pkey"          ])        
        topup_transaction_rec.put("topup_request_id",               topup_request_rec["topup_request_id"        ]) # 
        topup_transaction_rec.put("request_user_id",                topup_request_rec["request_user_id"         ]) #pkey from db_user
        topup_transaction_rec.put("fk_admin_id",                    params["fk_user_id"                         ]) #pkey from db_user
        topup_transaction_rec.put("amount",                         int(topup_request_rec["amount"              ]))
        topup_transaction_rec.put("transaction_status",             "APPROVE"                                   )
        topup_transaction_rec.put("transaction_date",               today_date                                  )
        topup_transaction_rec.put("payment_method",                 topup_request_rec["payment_method"          ])
        topup_transaction_rec.put("reference_id",                   topup_request_rec["reference_id"          ])                                
        topup_transaction_rec.put("topup_request_date",             topup_request_rec["created_at"              ])
        topup_transaction_rec.put("update_by_admin_at",             today_date                                  )                    
        topup_transaction_rec.insert()   

        # update progress top up in db_topup_request 
        update_rec = {
                "request_status"            : "APPROVE",
                "update_by_admin_at"        : today_date
        }   

        
        request_rec           = self.mgdDB.db_topup_request.update_one(
            {"topup_request_id"   : params["topup_request_id"]},            
            {
                '$set'            : update_rec                
            }      
        )

        # update saldo in db_user field: "balance"            
        user_rec             = self.mgdDB.db_user.find_one(
            {"fk_user_id"   : topup_request_rec["request_user_id" ]}                       
        )

        current_balance = user_rec["balance"]
        topup_amount    = topup_request_rec["amount"]

        # sum the old balance with a new one
        balance = current_balance + topup_amount
        request_rec           = self.mgdDB.db_user.update_one(
            {"fk_user_id"   : topup_request_rec["request_user_id" ]},                       
            {
                '$set'            : { "balance" : balance}                
            }      
        )
        
        return result_url
        

# end class
