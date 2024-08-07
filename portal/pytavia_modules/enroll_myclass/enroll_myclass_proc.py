import config_core
import sys
import traceback
import json
import ast
import time
import random
import re
from datetime import datetime
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


class enroll_myclass_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def


    def buy_enroll_myclass(self, params):    
        result_url = "/enrollMyClass" 

        # find activation open class
        buy_activation_class_rec            = self.mgdDB.db_activation_class.find_one(
            {"activation_class_id"          : params["activation_class_id"]}
        )

        # check saldo first
        check_saldo_buyer                   = self.mgdDB.db_user.find_one(
            {"fk_user_id"                   : params["fk_user_id"]}
        )

        if check_saldo_buyer['balance'] < int(buy_activation_class_rec['price_class']):
            response = {
                    "result_url"   : result_url,
                    "notif_type"   : "warning",
                    "msg"   : "Your balance is not enough. Please top up first."        
                }
            return response
            

        # find prerequisite_class_id, so before you can buy class you should pass prerequisite class
        class_rec = self.mgdDB.db_class.find_one({
            "class_id" : buy_activation_class_rec["class_id"]
        })


        #find every activation class relate with this prerequisite class
        prerequisite_class_rec = self.mgdDB.db_activation_class.find({
            "class_id" : { '$in': class_rec['prerequisite_class_id']}
        })

        for prerequisite_class_item in prerequisite_class_rec:
            check_if_already_pass_class        = self.mgdDB.db_enrollment.find_one(
                {
                    "activation_class_id"         : prerequisite_class_item["activation_class_id"],
                    "fk_user_id"                  : params["fk_user_id" ],
                    "enrollment_status"           : 'PASS'
                }
            )  

            if check_if_already_pass_class is None:
                response = {
                    "result_url"   : result_url,
                    "notif_type"   : "warning",
                    "msg"   : "You need to pass prerequisite class first, check on 'read more' ",           
                }
                return response
        
        has_purchased_before              = self.mgdDB.db_enrollment.find_one(
            {
                "activation_class_id"         : params["activation_class_id"],
                "fk_user_id"                  : params["fk_user_id" ],
                "enrollment_status"           : 'REGISTERED'
            }
        )        

        if has_purchased_before:
            response = {
                "result_url"   : result_url,
                "notif_type"   : "warning",
                "msg"   : "You have already purchased "+buy_activation_class_rec["active_class_name"]+", you just only buy once every class ",           
            }
        else:  

            # Get the current date
            today_date           = datetime.now().strftime('%Y-%m-%d %H:%M:%S')       

            # register student in db_enrollment
            enrollment_rec  = database.new(self.mgdDB, "db_enrollment")
            enrollment_rec.put("enrollment_id",                  enrollment_rec.get()["pkey"                  ])
            enrollment_rec.put("fk_user_id",                     params["fk_user_id"              ]) #pkey from db_user
            enrollment_rec.put("activation_class_id",            params["activation_class_id"     ])
            enrollment_rec.put("enrollment_date",                today_date  )        
            enrollment_rec.put("enrollment_status",              "REGISTERED"  )        
            enrollment_rec.insert()   
            

             # record data in db_trasaction
            ref_transaction_id = self.generate_reference_id()

            enrollment_rec  = database.new(self.mgdDB, "db_transaction")
            enrollment_rec.put("transaction_id",                 enrollment_rec.get()["pkey"                  ])
            enrollment_rec.put("ref_transaction_id",             ref_transaction_id)
            enrollment_rec.put("name_db_product",                "db_activation_class") #pkey from db_user
            enrollment_rec.put("fk_product_id",                  params["activation_class_id"])
            enrollment_rec.put("fk_buyer_id",                    params["fk_user_id"])
            enrollment_rec.put("type_product",                   "Enrollment Class")        
            enrollment_rec.put("name_product",                   buy_activation_class_rec["active_class_name"]  )        
            enrollment_rec.put("amount",                         int(buy_activation_class_rec["price_class"])  )        
            enrollment_rec.put("transaction_date",               today_date )        
            enrollment_rec.insert()    

            # last UPDATE BALANCE USER
            update_obj = {
                "balance" : check_saldo_buyer['balance'] - int(buy_activation_class_rec['price_class']),                
            }
            self.mgdDB.db_user.update(
                {"pkey" : params["fk_user_id"]},
                {"$set" : update_obj }
            ) 

            response = {
                "result_url"   : result_url,
                "notif_type"   : "success",
                "msg"   : "buying class "+buy_activation_class_rec["active_class_name"]+" success! \n Now you can got tutor from experience tutor",           
            }                    
                
        return response

    def generate_reference_id(self, prefix='TRANSAC'):
        # Get current date in YYYYMMDD format
        today_date = datetime.now().strftime('%Y%m%d')
        
        # Generate random alphanumeric string
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        # Concatenate parts to form transaction ID
        reference_id = f"{prefix}_{today_date}_{random_chars}"
        
        return reference_id    

        
# end class
