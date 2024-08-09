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


class view_topup:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def


    def _find_latest_topup_request(self,params):  
                                     
        latest_topup_request = self.mgdDB.db_topup_request.find({
            "request_user_id" : params['fk_user_id']
        }).sort("rec_timestamp", -1).limit(1)
        
        check_exist = list(latest_topup_request)
        if check_exist:
            latest_topup_request_list = []
            for latest_topup_request_item in latest_topup_request:  
                        
                # Convert price to Rupiah currency format
                if 'amount' in latest_topup_request_item:
                    latest_topup_request_item['amount'] = self.format_currency(latest_topup_request_item['amount'])

            latest_topup_request_list.append(latest_topup_request_item)        
        
            response =  latest_topup_request_list[0]
        else:
            response =  {}
            

        return response
                          
    # end def

    def _data_user(self,params):              
        query = { "fk_user_id": params["fk_user_id"]}
        user = self.mgdDB.db_user.find_one(query)     
        # ver_status = user['ver_email']          

        return user
    

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

            # FOR CHECK THE LATEST TOPUP REQUEST
            latest_topup_request_resp             = self._find_latest_topup_request( params )
            print(latest_topup_request_resp)
            print("air panas")
            user_rec         = self._data_user(params)                          
                        
            html = render_template(
                "payment/topup.html",
                menu_list_html      = menu_list_html,
                core_display        = core_display,
                core_header         = core_header, 
                core_footer         = core_footer, 
                core_script         = core_script,  
                core_css            = core_css,
                core_dialog_message = core_dialog_message,
                username            = params["username"      ],
                role_position       = params["role_position" ],                        
                latest_topup_request_resp        = latest_topup_request_resp,                
                user_rec                = user_rec
            )

            response.put( "data", {
                    "html" : html,
                    "user_rec" : user_rec
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

    
    
# end class

