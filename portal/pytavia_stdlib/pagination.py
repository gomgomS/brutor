import boto
import json
import urllib.parse

from pytavia_core import config

class pagination:

    def __init__(self):
        pass
    
    def _find_button(self, params):
        url_params  = params["url_params"   ]
        url         = params["url"          ]
        page        = params["page"         ]
        block_count = params["block_count"  ]

        prev_button     = {
            "url"       : "",
            "type"      : "",
            "page"      : ""
        }
        next_button     = {
            "url"       : "",
            "type"      : "",
            "page"      : ""
        }
        
        
        if block_count == 1 or block_count == 0:
            # previous and first button is disabled
            prev_button["type"] = "disabled"
            next_button["type"] = "disabled"
        elif page == 1:
            # previous and first button is disabled
            prev_button["type"  ] = "disabled"
            next_button["page"  ] = page + 1

            url_params["page"   ] = str(page + 1)
            str_url_params        = urllib.parse.urlencode(url_params)
            next_button["url"   ] = url + str_url_params
        elif page == block_count:
            #next and third button is disabled
            next_button["type"  ] = "disabled"
            prev_button["page"  ] = page - 1

            url_params["page"   ] = str(page - 1)
            str_url_params        = urllib.parse.urlencode(url_params)
            prev_button["url"   ] = url + str_url_params
        else:
            
            prev_button["page"  ] = page - 1
            url_params["page"   ] = str(page - 1)
            str_url_params        = urllib.parse.urlencode(url_params)
            prev_button["url"   ] = url + str_url_params 
            
            next_button["page"  ] = page + 1
            url_params["page"   ] = str(page + 1)
            str_url_params = urllib.parse.urlencode(url_params)
            next_button["url"   ] = url + str_url_params
        

        response = {
            "prev_button"   : prev_button,
            "next_button"   : next_button
        }

        return response
    # end def


