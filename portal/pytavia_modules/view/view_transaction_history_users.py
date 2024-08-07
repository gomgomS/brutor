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


class view_transaction_history_users:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def

    

    def _find_transaction_history_users(self, params):
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

        order_by = 'desc' # i add this because there is no filter
        if order_by == "asc":
            order = pymongo.ASCENDING
        else:
            order = pymongo.DESCENDING
        

        query = {             
            # "status_value"      : "PROSES"
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

        transaction_history_users_list = []
        transaction_history_users_view = self.mgdDB.db_transaction.find(query).sort('rec_timestamp', order)
        block_count = utils.ceildiv(transaction_history_users_view.count(), entry)

        
        # PROCESS THE BUTTONS
        pagination_params = {
            "url_params"    : url_params,
            "url"           : "/transaction_history_users",
            "page"          : page,
            "block_count"   : block_count
        }
        pagination_resp = pagination.pagination()._find_button(pagination_params)
        prev_button = pagination_resp["prev_button"]
        next_button = pagination_resp["next_button"]
        

        # END OF PAGINATION

        for transaction_history_users_item in transaction_history_users_view:
            # find name base fk_buyer_id
            find_name_user                              = self._get_buyer_information(transaction_history_users_item["fk_buyer_id"] )            
           
            if find_name_user is not None:
                transaction_history_users_item["name"] = find_name_user["name"]
            else:
                transaction_history_users_item["name"] = ""

            # Convert amount to Rupiah currency format
            if 'amount' in transaction_history_users_item: 
                transaction_history_users_item['amount'] = self.format_currency(transaction_history_users_item['amount'])

            transaction_history_users_list.append(transaction_history_users_item)

        response = {
            "transaction_history_users_list"   : transaction_history_users_list,
            "block_count"   : block_count,
            "prev_button"   : prev_button,
            "next_button"   : next_button
        }

        return response
    # end def
    

    def html(self, params):
        response = helper.response_msg(
            "FIND_transaction_history_users_PROSES_SUCCESS", "FIND KONTEN PROSES SUCCESS", {} , "0000"
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

            # FIND transaction_history_users
            transaction_history_users_resp             = self._find_transaction_history_users( params )
            transaction_history_users_list             = transaction_history_users_resp["transaction_history_users_list"     ]
            block_count             = transaction_history_users_resp["block_count"     ]
            prev_button             = transaction_history_users_resp["prev_button"     ]
            next_button             = transaction_history_users_resp["next_button"     ]

            
            html = render_template(
                "payment_confirmation/transaction_history_users_list.html",
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
                transaction_history_users_list      = transaction_history_users_list,
                user_rec                = user_rec,
                # sort_by_list            = sort_by_list
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

    def _get_buyer_information(self,user_id):              
        query = { "fk_user_id": user_id}
        user = self.mgdDB.db_user.find_one(query,{'_id':0,'name':1})     
          

        return user
    
    def format_currency(self,amount):
        """Format the amount into Rupiah currency format."""
        try:
            amount = float(amount)  # Convert to float if it's a string
            return f"Rp {amount:,.0f}".replace(',', '.')
        except ValueError:
            return "Rp 0"  # Default value if conversion fails
    # end def
    
# end class

