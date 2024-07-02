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


class view_users_inactive:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def

    

    def _find_users(self, params):
        #PAGINATION
        page            = params["page"         ]
        keyword         = params["keyword"      ]
        entry           = params["entry"        ]
        order_by        = params["order_by"     ]
        sort_by         = params["sort_by"      ]
        
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

        now         = utils._get_current_datetime(hours = config.JKTA_TZ)
        timestamp   = utils._convert_datetime_to_timestamp(now)
        
        
        query = { 
            "status"        : "INACTIVE",
            "is_deleted"    : False,
        }

        if params["role_position"] != "SYSADMIN":
            query["role_position_value"] = {"$ne" : "SYSADMIN" }

        if keyword != "":
            query["$text"] = { "$search" : keyword }

        # COMPUTE HOW MANY RECORDS TO SKIP
        block_skip = (page - 1) * entry

        user_list = []
        users_view = self.mgdDB.db_user.find(query).sort(sort_by, order).skip(block_skip).limit(entry)
        block_count = utils.ceildiv(users_view.count(), entry)

        
        # PROCESS THE BUTTONS
        pagination_params = {
            "url_params"    : url_params,
            "url"           : "/users/inactive?",
            "page"          : page,
            "block_count"   : block_count
        }
        pagination_resp = pagination.pagination()._find_button(pagination_params)
        prev_button = pagination_resp["prev_button"]
        next_button = pagination_resp["next_button"]
        

        # END OF PAGINATION

        for users_item in users_view:
            user_list.append(users_item)

        response = {
            "user_list"     : user_list,
            "block_count"   : block_count,
            "prev_button"   : prev_button,
            "next_button"   : next_button
        }

        return response
    # end def
    

    def html(self, params):
        response = helper.response_msg(
            "FIND_USER_LIST_SUCCESS", "FIND USER LIST SUCCESS", {} , "0000"
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


            sort_by_list = [
                { 
                    "name" : "Date" ,
                    "value" : "rec_timestamp" 
                },
                { 
                    "name" : "Nama Lengkap" ,
                    "value" : "nama_lengkap" 
                }
                
            ]


            entry_resp      = utils._find_table_entries()
            entry_list      = entry_resp["entry_list"]

            # FIND PROGRAM
            users_resp  = self._find_users( params )
            user_list  = users_resp["user_list"   ]
            block_count = users_resp["block_count"  ]
            prev_button = users_resp["prev_button"  ]
            next_button = users_resp["next_button"  ]

            
            html = render_template(
                "users/users_inactive.html",
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
                sort_by_list            = sort_by_list,
                user_list               = user_list
                
            )

            response.put( "data", {
                    "html" : html
                }
            )


        except:
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "FIND_USER_LIST_FAILED" )
            response.put( "desc"        , "Find users list failed" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })

        # end try

        return response
    # end def
    
# end class

