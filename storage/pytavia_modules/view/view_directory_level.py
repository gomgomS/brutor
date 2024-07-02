import sys
import os
import traceback

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

sys.path.append("pytavia_modules/view" )

from flask          import render_template
from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config

class view_directory_level:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self,app):
        self.webapp = app
    # end def

    """
        This is how we print the current working directory. 
            We are able to see the folders in the directory that
            has been clicked by the user
    """
    def show_pwd(self, params):
        parent_node_id  = params["pnode_id"]
        list_directory  = []
        dsp_file_path   = ""
        filesystem_view = self.mgdDB.db_filesystem.find({
            "parent_node_id" : parent_node_id,
        }).sort("current_node", 1)
        for filesystem_rec in filesystem_view:
            child_node = filesystem_rec["child_node"]
            if child_node == None:
                key_file_path = filesystem_rec["file_path"   ]
                fk_bucket_id  = filesystem_rec["fk_bucket_id"]
                cfs_rec = self.mgdDB.db_blipcom_cfs.find_one({
                    "key" : key_file_path
                })
                file_download_link = config.G_FILE_LINK.replace(
                    "__REPLACE__KEY__"    , key_file_path
                ).replace(
                    "__REPLACE__BUCKET__" , fk_bucket_id
                )
                filesystem_rec["down_link"   ] = file_download_link
                filesystem_rec["icon_type"   ] = config.G_FILE_ICON
                filesystem_rec["file_size"   ] = cfs_rec["convert_size_bytes"]
                filesystem_rec["content_type"] = cfs_rec["content_type"      ]
                filesystem_rec["extension"   ] = cfs_rec["extension"         ]
            else:
                child_pnode_id = filesystem_rec["pkey"]
                filesystem_rec["down_link"   ] = config.G_DIR_LINK + child_pnode_id
                filesystem_rec["icon_type"   ] = config.G_DIR_ICON
                filesystem_rec["file_size"   ] = "--"
                filesystem_rec["content_type"] = "File Folder"
                filesystem_rec["extension"   ] = "NA"
            # end if
            dsp_file_path         = filesystem_rec["file_path"]
            basename              = os.path.basename(dsp_file_path)
            dsp_file_path         = dsp_file_path.replace("/" + basename , "")
            list_directory.append( filesystem_rec )
        # end for
        #
        # This is where we create the breadcrumb link so that it can be
        #       clicked by the user to navigate and jump paths
        #
        file_path_list        = dsp_file_path.split("/")
        file_working_path     = ""
        bc_file_system_list   = []
        root_bucket_item      = { "bucket_name" : "", "bucket_id" : "" }
        if len(file_path_list) > 0:
            file_path_list.pop( 0 )
            for file_item in file_path_list:
                file_working_path = file_working_path + "/" + file_item 
                bc_filesystem_rec = self.mgdDB.db_filesystem.find_one({
                    "file_path"    : file_working_path,
                    "current_node" : file_item
                })
                bc_current_node_id = bc_filesystem_rec["current_node_id"]
                file_item_elem     = {
                    "pnode_id"     : bc_current_node_id,
                    "current_node" : file_item
                }
                bc_file_system_list.append( file_item_elem )
            # end for
            #
            # Get the bucket that this is all tied to so we can display
            #   the bottom root directories
            #
            bucket_rec            = None
            root_bucket_item      = None 
            bucket_filesystem_rec = self.mgdDB.db_filesystem.find_one({
                "current_node_id"  : parent_node_id 
            })
            if bucket_filesystem_rec != None:
                bucket_value  = bucket_filesystem_rec["fk_bucket_id"]
                bucket_rec    = self.mgdDB.db_bucket.find_one({ 
                    "value" : bucket_value 
                })
            else:
                bucket_rec    = self.mgdDB.db_bucket.find_one({ 
                    "pkey"  : parent_node_id 
                })
            # end if
            bucket_name       = bucket_rec["name"]
            bucket_id         = bucket_rec["pkey"]
            root_bucket_item  = {
                "bucket_name" : bucket_name,
                "bucket_id"   : bucket_id
            }
        # end if
        response     = { 
            "list_directory"      : list_directory,
            "dsp_file_path"       : dsp_file_path.replace("/"," / "),
            "bc_file_system_list" : bc_file_system_list,
            "root_bucket_item"    : root_bucket_item
        }
        return response
    # end def

    """
        Build the page that renders all of the directories
            files and all the details of each of the files
    """
    def html(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "DISPLAY_TEMPLATE_SUCCESS",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            display_directory       = self.show_pwd( params ) 
            pnode_id                = params["pnode_id"]
            list_directory          = display_directory["list_directory"     ]
            dsp_file_path           = display_directory["dsp_file_path"      ]
            bc_file_system_list     = display_directory["bc_file_system_list"]
            root_bucket_item        = display_directory["root_bucket_item"   ]
            return render_template(
                "directory.html",
                list_directory      = list_directory   ,
                dsp_file_path       = dsp_file_path    ,
                pnode_id            = pnode_id         ,
                root_bucket_item    = root_bucket_item ,
                bc_file_system_list = bc_file_system_list
            )                
        except:
            self.webapp.logger.debug (traceback.format_exc())
            response["message_action"] = "DISPLAY_TEMPLATE_FAILED"
            response["message_action"] = "DISPLAY_TEMPLATE_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
# end class
