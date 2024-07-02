import config_core
import sys
import traceback

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib   import idgen
from pytavia_stdlib   import utils
from pytavia_core     import database
from pytavia_core     import config

class config_fuel_price:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def upsert(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "ADD_FUEL_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            fk_user_id  = params['fk_user_id'   ]
            terms       = params["terms"        ]
            period      = params["period"       ]
            price       = params["price"        ]
            value       = params["value"        ]
            supplier    = params["supplier"     ]
            city        = params["city"         ]
            desc        = params["desc"         ]
            misc        = params["misc"         ]
            context     = params["context"      ]

            doc = self.mgdDB.db_config_fuel_price.find_one({ "value" : value})
            if doc:
                self.mgdDB.db_config_fuel_price.update(
                    { 
                        "pkey"      : doc['pkey'],
                    },
                    { "$set"        : { 
                        "terms"   : terms ,
                        "period"  : period, 
                        "price"   : price , 
                        "supplier": supplier,
                        "city"    : city  , 
                        "desc"    : desc  , 
                        "misc"    : misc  , 
                        "context" : context,
                        }
                    }
                )

                response["message_action"] = "UPDATE_FUEL_SUCCESS"
            else:

                doc = database.get_record("db_config_fuel_price")
                doc["fk_user_id"      ] = fk_user_id  
                doc["terms"           ] = terms   
                doc["period"          ] = period  
                doc["price"           ] = price   
                doc["value"           ] = value   
                doc["supplier"        ] = supplier
                doc["city"            ] = city    
                doc["desc"            ] = desc    
                doc["misc"            ] = misc    
                doc["context"         ] = context 

                self.mgdDB.db_config_fuel_price.insert( doc )

                response["message_action"] = "ADD_FUEL_SUCCESS"
            
        except :
            self.webapp.logger.debug(traceback.format_exc())
            response["message_action"   ] = "ADD_FUEL_FAILED"
            response["message_action"   ] = "ADD_FUEL_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def

    def remove(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "REMOVE_FUEL_SUCCESS",
            "message_code"   : "0",
            "message_title"  : "",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            value = params["value"]
            self.mgdDB.db_config_fuel_price.remove({ "value": value })
        except:
            self.webapp.logger.debug(traceback.format_exc())
            response["message_action"] = "REMOVE_FUEL_FAILED"
            response["message_action"] = "REMOVE_FUEL_FAILED: " + str(sys.exc_info())
        # end try

        return response
    # end def
# end class
