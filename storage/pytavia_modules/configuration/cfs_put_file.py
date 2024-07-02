import os
import sys
import traceback
import base64
import re
import time
import gridfs

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config

from streaming_form_data         import StreamingFormDataParser
from streaming_form_data.targets import FileTarget, ValueTarget
from streaming_form_data.targets import BaseTarget

class cfs_put_file:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self,app):
        self.webapp = app
    # end def

    def put(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "ADD_CFS_FILE_SUCCES",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            stream          = params["stream" ]
            header          = params["header" ]
            self.webapp.logger.debug( "---------------------------------" )
            self.webapp.logger.debug( stream )
            self.webapp.logger.debug( "---------------------------------" )
            #
            # Now get the header data
            #
            key_file_name   = header["key"      ]
            bucket          = header["bucket"   ]
            label           = header["label"    ]
            extension       = header["extension"]
            conType         = header["conType"  ]
            #
            # Read the raw data and start reading it 
            # into the file
            #
            raw             = stream.read(1024)
            handle_mgd_grid = gridfs.GridFS(self.mgdDB)
            file_name       = key_file_name
            mgd_grid_fs     = handle_mgd_grid.new_file(filename=file_name) 

            parser          = StreamingFormDataParser(headers=header)
            parser.register('stream', grid_fs_proc( mgd_grid_fs ))
            while raw:
                parser.data_received( raw )
                raw    = stream.read(1024)
                # hide log for now due to highly increase in nohup log size
                #self.webapp.logger.debug( "----------------raw-----------------" )
                #self.webapp.logger.debug( raw )
                #self.webapp.logger.debug( "----------------raw-----------------" )
            # end while
            mgd_grid_fs.close()
            fs_file_rec = self.mgdDB.fs.files.find_one({
                "filename" : file_name
            })
            file_md5        = fs_file_rec["md5"      ]
            save_file_name  = fs_file_rec["filename" ]
            file_size       = fs_file_rec["length"   ]
            chunk_size      = fs_file_rec["chunkSize"]
            fk_file_id      = fs_file_rec["_id"      ]
            #
            #  now we add it into the file system
            #
            cfs_rec = database.get_record("db_blipcom_cfs")
            cfs_rec["key"               ] = save_file_name
            cfs_rec["file_md5"          ] = file_md5
            cfs_rec["fk_file_id"        ] = fk_file_id
            cfs_rec["content_type"      ] = conType
            cfs_rec["extension"         ] = extension
            cfs_rec["encode"            ] = file_md5
            cfs_rec["bucket"            ] = bucket
            cfs_rec["label"             ] = label
            cfs_rec["convert_size_bytes"] = file_size
            cfs_rec["ori_size_bytes"    ] = chunk_size
            cfs_rec_check = self.mgdDB.db_blipcom_cfs.find_one({
                "$and" : [
                    {"key"    : key_file_name },
                    {"bucket" : bucket }
                ]
            })
            if cfs_rec_check == None:
                self.mgdDB.db_blipcom_cfs.insert( cfs_rec )
                response["message_data"] = {
                    "key"  :  key_file_name,
                    "path" : "key=" + key_file_name + "&bucket=" + bucket ,
                    "size" :  file_size,
                }
                self.create_bucket({ "bucket" : bucket })
                self.create_path  ({ 
                    "full_path" : key_file_name , 
                    "bucket"    : bucket 
                })
            else:
                response["message_action"] = "CFS_FILE_EXIST"
            #end if
        except :
            self.webapp.logger.debug (traceback.format_exc())
            response["message_action"] = "ADD_CFS_FILE_FAILED"
            response["message_action"] = "ADD_CFS_FILE_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def

    """
        This will create a bucket if it does not exist
        if it does this function will do nothing
    """
    def create_bucket(self, params):
        bucket       = params["bucket"]
        bucket_value = bucket.replace(" ","_").upper()
        bucket_rec   = self.mgdDB.db_bucket.find_one({
            "value" : bucket_value,
        })
        if bucket_rec == None:
            str_created_time = time.strftime(
                    "%d-%m-%Y %H:%M:%S", 
                    time.localtime(int(time.time()))
            )
            new_bucket_rec   = database.get_record("db_bucket")
            new_bucket_rec["name"            ] = bucket
            new_bucket_rec["value"           ] = bucket_value
            new_bucket_rec["str_created_time"] = str_created_time
            self.mgdDB.db_bucket.insert( new_bucket_rec )
        # end if
    # end def

    """
        This will create the directory structure for each type of file 
            that has been updated into the system
    """
    def create_path(self, params):
        file_full_path  = params["full_path"]
        bucket          = params["bucket"   ]
        file_name       = os.path.basename( file_full_path ) 
        file_path_array = file_full_path.split("/")
        path_build_up   = ""
        path_idx_count  = 0
        file_path_array.pop( 0 )  
        for file_directory in file_path_array:
            parent_node_id = None
            child_node_id  = None
            path_build_up  = path_build_up + "/" + file_directory
            filesystem_rec = self.mgdDB.db_filesystem.find_one({ 
                "file_path"    : path_build_up,
                "current_node" : file_directory
            })
            if filesystem_rec  == None:
                curr_child_dir  = None
                curr_parent_dir = None
                """
                    Create the parent and child linkage for the directory
                        This links the current directory to its parent
                """
                if path_idx_count > 0:
                    curr_parent_dir       = file_path_array[ path_idx_count - 1]
                    curr_parent_fullpath  = path_build_up.replace("/" + file_directory , "")
                    parent_filesystem_rec = self.mgdDB.db_filesystem.find_one({
                        "file_path" : curr_parent_fullpath
                    })
                    if parent_filesystem_rec != None:
                        parent_node_id = parent_filesystem_rec["pkey"]
                    # end if
                else:
                    parent_bucket_rec = self.mgdDB.db_bucket.find_one({ "value" : bucket })
                    parent_node_id    = parent_bucket_rec["pkey"]
                    curr_parent_dir   = "BUCKET"
                # end if
                """
                    Create the current directory to the child directory
                        if it is null then we just assign it to null and 
                        the value is none
                """
                if path_idx_count < len( file_path_array ) - 1:
                    curr_child_dir        = file_path_array[ path_idx_count + 1] 
                    curr_child_fullpath   = path_build_up + "/" + curr_child_dir
                    child_filesystem_rec  = self.mgdDB.db_filesystem.find_one({
                        "file_path" : curr_child_fullpath
                    })
                    if child_filesystem_rec != None:
                        child_node_id = child_filesystem_rec["pkey"]
                    # end if
                # end if
                """
                    Essentially this is like creating an iNODE for a directory
                        Here we create the directory and all the details associated
                        with the directory
                """
                str_created_time = time.strftime(
                        "%d-%m-%Y %H:%M:%S", time.localtime(int(time.time()))
                )
                db_filespec_rec  = database.get_record("db_filesystem")
                db_filespec_rec["file_path"       ] = path_build_up
                db_filespec_rec["filename"        ] = file_name
                db_filespec_rec["parent_node"     ] = curr_parent_dir
                db_filespec_rec["parent_node_id"  ] = parent_node_id
                db_filespec_rec["child_node"      ] = curr_child_dir
                db_filespec_rec["child_node_id"   ] = child_node_id
                db_filespec_rec["current_node"    ] = file_directory
                db_filespec_rec["current_node_id" ] = db_filespec_rec["pkey"]
                db_filespec_rec["fk_bucket_id"    ] = bucket
                db_filespec_rec["str_created_time"] = str_created_time
                self.mgdDB.db_filesystem.insert( db_filespec_rec )
            # end if
            path_idx_count += 1
        # end for
    # end def

    """
        This will update files into the system and arrange the 
        structure as needed
    """
    def update(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "ADD_CFS_FILE_SUCCES",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            key       = params["key"      ]
            document  = params["document" ]
            bucket    = params["bucket"   ]
            label     = params["label"    ]
            extension = params["extension"]     
            conType   = params["conType"  ] 
            file_size = params["file_size"] if "file_size" in params else 0

            self.create_bucket({ "bucket"    : bucket })
            self.create_path  ({ "full_path" : key , "bucket" : bucket })
            #
            # convert and get size document 
            #
            encode = base64.encodestring(document.read())
            encode_file = open("Output.txt","w")
            encode_file.write(str(encode))
            encode_size = encode_file.tell()
            encode_file.close()         
            
            cfs_rec = database.get_record("db_blipcom_cfs")       
            cfs_rec["key"               ] = key
            cfs_rec["content_type"      ] = conType
            cfs_rec["extension"         ] = extension            
            cfs_rec["encode"            ] = encode
            cfs_rec["bucket"            ] = bucket
            cfs_rec["label"             ] = label
            cfs_rec["convert_size_bytes"] = encode_size
            cfs_rec["ori_size_bytes"    ] = file_size
            cfs_rec_check = self.mgdDB.db_blipcom_cfs.find_one({
                "$and" : [
                    {"key"    : key    },
                    {"bucket" : bucket }
                ]
            })
            if cfs_rec_check == None:
                self.mgdDB.db_blipcom_cfs.insert( cfs_rec )                
                response["message_data"] = {
                    "key"  : key                          ,
                    "path" : "key="+key+"&bucket="+bucket ,
                    "size" : encode_size                  ,
                }
            else:
                response["message_action"] = "CFS_FILE_EXIST"
            #end if
        except :
            self.webapp.logger.debug (traceback.format_exc())
            response["message_action"] = "ADD_CFS_FILE_FAILED"
            response["message_action"] = "ADD_CFS_FILE_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def
# end class

class grid_fs_proc(BaseTarget):

    def __init__(self, handle_grid_fs):
        self.g_handle_grid_fs = handle_grid_fs
        self._validator = None
    # end def

    def on_data_received(self, raw):
        self.g_handle_grid_fs.write(raw)
    # end def
# end class
