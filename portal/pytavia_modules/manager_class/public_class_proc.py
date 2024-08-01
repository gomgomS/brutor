import config_core
import sys
import traceback
import json
import ast
import time
import random
import re

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


class public_class_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def


    def buy_public_class(self, params):    
        result_url = "/public_class" 
      
        # Update the document in MongoDB
        buy_class_rec                    = self.mgdDB.db_class.find_one(
            {"class_id"         : params["class_id"]}
        )

        has_purchased_before              = self.mgdDB.db_class.find_one(
            {
                "original_class_id"         : params["class_id"],
                "buyer_user_id"             : params["fk_user_id" ]
            }
        )

        if has_purchased_before:
            response = {
                "result_url"   : result_url,
                "notif_type"   : "warning",
                "msg"   : "You have already purchased "+buy_class_rec["name_class"]+", you cannot buy it again. ",           
            }  

        else:  
            # clone class   
            class_rec  = database.new(self.mgdDB, "db_class")
            class_rec.put("class_id",                   class_rec.get()["pkey"             ])
            class_rec.put("original_class_id",          buy_class_rec["class_id"                   ])
            class_rec.put("creator_id",                 buy_class_rec["creator_id" ]               ) #pkey from db_user
            class_rec.put("level_id",                   buy_class_rec["level_id"                   ])
            class_rec.put("name_class",                 buy_class_rec["name_class"                 ])
            class_rec.put("desc_class",			        buy_class_rec["desc_class"                 ])
            class_rec.put("desc_class_html",		    buy_class_rec["desc_class_html"                 ])
            class_rec.put("desc_class_preview",         buy_class_rec["desc_class_preview"                 ])
            class_rec.put("status_class",               "PAID")    
            class_rec.put("prerequisite_class_id",      buy_class_rec["prerequisite_class_id"                 ])
            class_rec.put("pass_requirement",		    buy_class_rec["pass_requirement"                 ])
            class_rec.put("pass_requirement_html",	    buy_class_rec["pass_requirement_html"                 ])
            class_rec.put("pass_requirement_preview",   buy_class_rec["pass_requirement_preview"                 ])
            class_rec.put("buyer_user_id",              params["fk_user_id" ]               )                     
            class_rec.put("price_class",                "NOT_FOR_SALE"                          )    
            class_rec.insert()         


            response = {
                "result_url"   : result_url,
                "notif_type"   : "success",
                "msg"   : "buying class "+buy_class_rec["name_class"]+" success! \n Now you can add class as 'Prerequisite Class' and also use the Class",           
            }              
        
        
        return response

        
# end class
