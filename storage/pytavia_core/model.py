import time
import copy
import pymongo
import os
import sys

from bson.objectid import ObjectId

"""
FOR APP DISPLAY  
    - name : logo, value                : logo_path
    - name : text_color                 : "hex" 
    - name : core_color                 : "hex"
    - name : secondary_color            : "hex"

    - name : bar_graph_color            : {"color1":"hex", "color2":"hex"}
    - name : line_graph_color           : {"color1":"hex", "color2":"hex"}

    - name : button_color               : "hex"
    - name : button_text_color          : "hex"

    - name : summary_panel_color_1      : "hex" 
    - name : summary_panel_color_2      : "hex" 
    - name : summary_panel_color_3      : "hex" 
    - name : summary_panel_color_4      : "hex" 

    - name : summary_panel_text_color_1 : "hex" 
    - name : summary_panel_text_color_2 : "hex" 
    - name : summary_panel_text_color_3 : "hex" 
    - name : summary_panel_text_color_4 : "hex" 
"""


#
# Define the models/collections here for the mongo db
#
db = {
    "db_admin_user"          : {
        "username"           : "",
        "password"           : "",
        "active"             : "TRUE",
        "role"               : "ADMIN"
    },
    "db_bucket"              : {
        "name"               : "",
        "value"              : "",
        "public"             : 1 ,
        "encrypted"          : 0 ,
        "compressed"         : 0 ,
        "str_created_time"   : "",
    },
    "db_filesystem"          : {
        "file_path"          : "", # full path of the file
        "filename"           : "", # the basename of the file
        "parent_node"        : "",
        "parent_node_id"     : "",
        "child_node"         : "",
        "child_node_id"      : "",
        "current_node"       : "",
        "current_node_id"    : "",
        "deleted"            : 0 ,
        "writeable"          : 0 ,
        "hidden"             : 0 ,
        "str_created_time"   : "",
        "fk_bucket_id"       : "",
    },
    "db_blipcom_cfs"         : {
        "key"                : "",
        "file_md5"           : "",
        "fk_file_id"         : "",
        "content_type"       : "",
        "extension"          : "",
        "encode"             : "",
        "bucket"             : "",
        "label"              : "",
        "convert_size_bytes" : "",
        "ori_size_bytes"     : "",
        "rec_timestamp"      : 0
    },      
    "db_content_type"        : {
        "key"                : "",
        "content_type"       : "",
        "desc"               : "",
        "rec_timestamp"      : 0        
    },
    "db_security_api_core"   : {
        "api_key"            : "",
        "api_secret"         : "",
        "active"             : "TRUE",
        "description"        : ""
    },
    "db_security_user"       : {
        "token_value"        : "",
        "username"           : "",
        "password"           : "",
        "expire_time"        : "",
        "active"             : "TRUE"
    }, 
    "db_security_cfs"          : {
        "token_value"           : "",
        "username"              : "",
        "password"              : "",
        "expire_time"           : "",
        "active"                : "TRUE"
    },  
    
}
