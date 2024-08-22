import sys
import traceback
import pymongo
import urllib.parse

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

sys.path.append("pytavia_modules/view" )

from flask          import render_template
from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_stdlib import pagination
from pytavia_core   import helper
from pytavia_core   import database
from pytavia_core   import config

from view import view_core_menu
from view import view_core_display
from view import view_core_header
from view import view_core_footer
from view import view_core_script
from view import view_core_css
from view import view_core_dialog_message


class view_enroll_myclass:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def

    def _find_creator_class(self,fk_user_id):                                    
        user = self.mgdDB.db_user.find_one({
            "fk_user_id" : fk_user_id
        })
        
        response =  user
        return response

    

    def _find_activation_class(self, params):
        #PAGINATION
        page            = params["page"         ]
        keyword         = params["keyword"      ]
        entry           = params["entry"        ]
        order_by        = params["order_by"     ]
        sort_by         = params["sort_by"      ]
        start_date      = params["start_date"   ]
        end_date        = params["end_date"     ]
        
        url_params = {
            "order_by"      : params["order_by"     ],
            "keyword"       : params["keyword"      ],
            "entry"         : params["entry"        ],
            "sort_by"       : params["sort_by"      ]
        }

        if order_by == "asc":
            order = pymongo.ASCENDING
        else:
            order = pymongo.DESCENDING
        

        query = { 
            # "is_deleted"        : False, 
            # "status_value"      : "PROSES"
        }

       # Construct the query
        query = {
            "$or": [
                { "status_activation": "OPEN_REGISTRATION" },  # Include documents with status "OPEN"                
            ]
        }
        

        
        start_timestamp = 0
        end_timestamp   = 0

        if start_date != "":
            start_obj = utils._get_datetime_from_str_date(start_date, date_format = '%d/%m/%Y')
            start_timestamp = utils._convert_datetime_to_timestamp(start_obj)
            url_params["start_date"] = start_date
        
        if end_date != "":
            end_obj = utils._get_datetime_from_str_date(end_date, date_format = '%d/%m/%Y')
            end_timestamp = utils._convert_datetime_to_timestamp(end_obj)
            end_timestamp += config.MS_24_HOURS
            url_params["end_date"] = end_date


        if start_timestamp != 0 and end_timestamp != 0:
            query["start_timestamp" ] = { "$gte" : start_timestamp  }
            query["end_timestamp"   ] = { "$lte" : end_timestamp    }
            
        elif start_timestamp != 0 :
            query["start_timestamp" ] = { "$gte" : start_timestamp  }

        elif end_timestamp != 0:
            query["end_timestamp"   ] = { "$lte" : end_timestamp    }

        if keyword != "":
            query["$text"] = { "$search" : keyword }

        # COMPUTE HOW MANY RECORDS TO SKIP
        block_skip = (page - 1) * entry

        # konten_list = []
        # konten_view = self.mgdDB.db_class.find(query).sort(order).skip(block_skip).limit(entry)
        # block_count = utils.ceildiv(konten_view.count(), entry)

        
        class_view = self.mgdDB.db_activation_class.find(query)
      
        block_count = utils.ceildiv(class_view.count(), entry)

        
        # PROCESS THE BUTTONS
        pagination_params = {
            "url_params"    : url_params,
            "url"           : "/enroll_myclass",
            "page"          : page,
            "block_count"   : block_count
        }
        pagination_resp = pagination.pagination()._find_button(pagination_params)
        prev_button = pagination_resp["prev_button"]
        next_button = pagination_resp["next_button"]
        

        # # END OF PAGINATION
        # for test_item in test_view:                     
        #     class_resp                          = self._find_activation_class( test_item["activation_class_id"] )            
        #     test_item["active_class_name"]      = class_resp["active_class_name"     ] 
        #     test_list.append(test_item)


        class_list = []

        # Lists to hold items to be appended at the end
        owner_classes = []
        paid_classes = []

        for class_item in class_view:  
            #find creator class
            creator_class                       = self._find_creator_class(class_item['fk_user_id'])
            class_item['creator_name']          = creator_class['name']     

            #find inforamtion class and enrollment status   
            class_info                          = self._find_class_and_enrollment_status(class_item['class_id'],params['fk_user_id'])
            class_item['class_info']            = class_info

            #find inforamtion class and enrollment status   
            total_already_registered                  = self._total_already_registered(class_item['activation_class_id'])
            class_item['total_already_registered']    = total_already_registered

            # Convert price to Rupiah currency format
            if 'price_class' in class_item:
                class_item['price_class'] = self.format_currency(class_item['price_class'])
   
            class_list.append(class_item)
            
           

        response = {
            "class_list"   : class_list,
            "block_count"   : block_count,
            "prev_button"   : prev_button,
            "next_button"   : next_button
        }

        return response
    # end def
    

    def html(self, params):
        response = helper.response_msg(
            "FIND_CLASS_PROSES_SUCCESS", "FIND KONTEN PROSES SUCCESS", {} , "0000"
        )
        try:
            menu_list_html         = view_core_menu.view_core_menu().html(params)
            core_display           = view_core_display.view_core_display().html(params)
            params["core_display"] = core_display         
            core_header            = view_core_header.view_core_header().html(params)
            core_footer            = view_core_footer.view_core_footer().html(params)
            core_script            = view_core_script.view_core_script().html(params)
            core_css               = view_core_css.view_core_css().html(params)
            core_dialog_message    = view_core_dialog_message.view_core_dialog_message().html(params)


            # PAGINATION
            if params["order_by"] == None :
                params["order_by"] = "desc"
            
            if params["keyword"] == None:
                params["keyword"] = ""
        
            if params["page"] == None:
                params["page"] = 1
            else:
                params["page"] = int(params["page"])
            
            if params["entry"] == None:
                params["entry"] = 25
            else:
                params["entry"]   = int(params["entry"])
            
            if params["sort_by"] == None:
                params["sort_by" ] = "rec_timestamp"

            if params["start_date"] == None:
                params["start_date" ] = ""
            
            if params["end_date"] == None:
                params["end_date" ] = ""        


            entry_resp              = utils._find_table_entries()
            entry_list              = entry_resp["entry_list"]

            # FIND user
            user_rec                = self._data_user(params)       


            # FIND class
            class_resp             = self._find_activation_class( params )
            class_list             = class_resp["class_list"     ]
            block_count             = class_resp["block_count"     ]
            prev_button             = class_resp["prev_button"     ]
            next_button             = class_resp["next_button"     ]

            
            html = render_template(
                "enroll_myclass/enroll_myclass_list.html",
                menu_list_html          = menu_list_html,
                core_display            = core_display,
                core_header             = core_header, 
                core_footer             = core_footer, 
                core_script             = core_script,  
                core_css                = core_css,
                core_dialog_message     = core_dialog_message,
                username                = params["username"      ],
                role_position           = params["role_position" ],
                page                    = params["page"          ],
                sort_by                 = params["sort_by"       ],
                order_by                = params["order_by"      ],
                keyword                 = params["keyword"       ],
                entry                   = params["entry"         ],
                entry_list              = entry_list,
                block_count             = block_count,
                prev_button             = prev_button,
                next_button             = next_button,                
                start_date              = params["start_date"   ],
                end_date                = params["end_date"     ],
                class_list              = class_list,
                user_rec                = user_rec
            )


            response.put( "data", {
                    "html" : html
                }
            )


        except:
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "FIND_KONTEN_PROSES_FAILED" )
            response.put( "desc"        , "FIND_KONTEN_PROSES_FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })

        # end try

        return response
    # end def

    def _data_user(self,params):              
        query = { "fk_user_id": params["fk_user_id"]}
        user = self.mgdDB.db_user.find_one(query)             

        return user
    
    def format_currency(self,amount):
        """Format the amount into Rupiah currency format."""
        try:
            amount = float(amount)  # Convert to float if it's a string
            return f"Rp {amount:,.0f}".replace(',', '.')
        except ValueError:
            return "Rp 0"  # Default value if conversion fails
    # end def

    def _find_creator_class(self,fk_user_id):                                    
        user_rec = self.mgdDB.db_user.find_one({
            "fk_user_id" : fk_user_id
        })
        
        response =  user_rec
        return response
    # end def

    def _total_already_registered(self,activation_class_id):                                    
        total_already_registered = self.mgdDB.db_enrollment.find({
            "activation_class_id" : activation_class_id
        }).count()
        
        response =  total_already_registered
        return response
    # end def
        
        
    def _find_class_and_enrollment_status(self, class_id, fk_student_id):
        # Find the class record
        class_rec = self.mgdDB.db_class.find_one({
            "class_id": class_id
        })
        
        if not class_rec:
            return None  # Return None if the class is not found
        
        # Find prerequisite classes
        prerequisite_class_rec = self.mgdDB.db_class.find({
            "class_id": { '$in': class_rec['prerequisite_class_id'] }
        })
        class_rec['prerequisite_class'] = list(prerequisite_class_rec)
        
        # Retrieve activation class data
        activation_class_data = list(self.mgdDB.db_activation_class.find({}))
        activation_class_map = {item['class_id']: item['activation_class_id'] for item in activation_class_data}
     
        # Retrieve enrollment data
        enrollment_data = list(self.mgdDB.db_enrollment.find({'fk_user_id':fk_student_id}))
        enrollment_map = {item['activation_class_id']: item['enrollment_status'] for item in enrollment_data}

        # Insert enrollment status into prerequisite classes
        for prerequisite in class_rec['prerequisite_class']:
            prerequisite['enrollment_status'] = 'UNREGISTERED'
            prerequisite_class_id = prerequisite['class_id']
            if prerequisite_class_id in activation_class_map:
                activation_class_id = activation_class_map[prerequisite_class_id]
                if activation_class_id in enrollment_map:
                    prerequisite['enrollment_status'] = enrollment_map[activation_class_id]       

        response = class_rec
        return response
    # enfif

    # end class

