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


class activation_class_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def


    def _add(self, params):
        response = helper.response_msg(
            "ADD_REGISTER_CLASS_SUCCESS", "ADD REGISTER CLASS SUCCESS", {} , "0000"
        )
        try:     

            # CONVERT STR DATETIME TO TIMESTAMP
            activate_datetime_obj = utils._get_datetime_from_str_date(params["activate_timestamp"] ,date_format = '%d/%m/%Y %H:%M' )
            activate_timestamp    = utils._convert_datetime_to_timestamp(activate_datetime_obj)            
          
            
            class_rec  = database.new(self.mgdDB, "db_activation_class")
            class_rec.put("activation_class_id",        class_rec.get()["pkey"             ])
            class_rec.put("fk_user_id",                 params["fk_user_id" ]               ) #pkey from db_user
            class_rec.put("active_class_name",          params["active_class_name"         ]) 
            class_rec.put("class_id",                   params["class_id"                  ]) 
            class_rec.put("activate_timestamp",         activate_timestamp                  )            
            class_rec.put("str_activate_timestamp",      params["activate_timestamp"         ])            
            class_rec.put("student_limit",              params["student_limit"             ])
            class_rec.put("can_just_test_to_pass",      params["can_just_test_to_pass"     ])
            class_rec.put("price_class",			    params["price_class"               ])
            class_rec.put("status_activation",		    params["status_activation"         ])                        
            class_rec.insert()                       

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "ADD_REGISTER_CLASS_FAILED" )
            response.put( "desc"        , "ADD REGISTER CLASS FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def
    
    def _edit(self, params):
        response = helper.response_msg(
            "UPDATE_KONTEN_SUCCESS", "UPDATE KONTEN SUCCESS", {} , "0000"
        )
        try:

            image           = params["files"]["image"]
            file_image      = ""
            file_name       = ""
            if image.filename != "":
                try:    
                    now_time        = int(time.time() * 1000)
                    random_int      = random.randint(1000000,9999999)
                    file_name       = "file_" + str( now_time ) + "_" + str(random_int)
                    created_time    = time.strftime("%d-%m-%Y", time.localtime(int(time.time())))
                    file_resp       = cfs_lib.store_file_to_cfs({
                        "bucket"     : config.G_IMAGE_BUCKET,
                        "label"      : config.G_IMAGE_LABEL,
                        "file_data"  : image,
                        "extension"  : "DEFAULT",
                        "allow_type" : ["DEFAULT"],
                        "file_name"  : "/konten/"  + created_time + "/" + file_name
                    })
                    
                    self.webapp.logger.debug( "------------------------------------------" )
                    self.webapp.logger.debug( file_resp )
                    self.webapp.logger.debug( "------------------------------------------" )
                    
                    action_file     = file_resp["message_action"]
                    desc_file       = file_resp["message_desc"  ]
                    data_file       = file_resp["message_data"  ]
                    
                    if action_file != "ADD_CFS_FILE_SUCCES":
                        response.put( "status"      , "ADD_KONTEN_FAILED" )
                        response.put( "desc"        , "Upload Image Failed" )
                        response.put( "status_code" , "1001" )
                        response.put( "data"        , { "error_message" : desc_file })
                        return response
                    #endif

                    file_image      = data_file["path"]
                    file_name       = data_file["key"]   
                except:
                    self.webapp.logger.debug(traceback.format_exc())
                    file_image      = ""

                #end try

                self.mgdDB.db_konten_img.update_one({ "fk_konten_id" : params["fk_konten_id"], "is_deleted" : False }, {"$set" : {"is_deleted" : True }})

                image_rec  = database.new(self.mgdDB, "db_konten_img")
                image_rec.put("fk_konten_id",      params["fk_konten_id"]   )
                image_rec.put("image",             file_image               )
                image_rec.insert()

            # CONVERT STR DATETIME TO TIMESTAMP
            start_datetime_obj = utils._get_datetime_from_str_date(params["start_datetime"] ,date_format = '%d/%m/%Y %H:%M' )
            start_timestamp    = utils._convert_datetime_to_timestamp(start_datetime_obj)

            end_datetime_obj = utils._get_datetime_from_str_date(params["end_datetime"] ,date_format = '%d/%m/%Y %H:%M' )
            end_timestamp    = utils._convert_datetime_to_timestamp(end_datetime_obj)
            
            # FIND BRUTOR DAFTAR
            partner_rec = self.mgdDB.db_brutor_partner.find_one({"pkey" : params["fk_perusahaan_id"]})

            # POSISI NAME
            posisi_rec  = self.mgdDB.db_config.find_one(
                {   
                    "config_type"   : "POSISI_DI_APLIKASI",
                    "value"         : params["fk_posisi_value"],
                    "is_deleted"    : False
                }
            )

            # JENIS TAMPILAN NAME
            jenis_tampilan_rec = self.mgdDB.db_config.find_one(
                {   
                    "config_type"   : "JENIS_TAMPILAN",
                    "value" : params["fk_jenis_tampilan_value"],
                    "is_deleted"    : False
                }
            )

            # deskripsi_html
            deskripsi_html = su.unescape(params["deskripsi"])

            clean = re.compile('<.*?>')
            params["deskripsi"] = re.sub( clean, '', deskripsi_html)

            list_deskripsi = params["deskripsi"].split(' ')
            list_deskripsi = list_deskripsi[0:10]
            list_deskripsi.append("...")
            deskripsi_preview = " ".join(list_deskripsi)

            # ORIGINAL KONTEN REC
            rec_before = self.mgdDB.db_konten.find_one(
                { 
                    "pkey" : params["fk_konten_id"]
                },
                {
                    "fk_perusahaan_id"          : 1,
                    "fk_posisi_value"           : 1,
                    "fk_jenis_tampilan_value"   : 1,
                    "perusahaan_name"           : 1,
                    "posisi_name"               : 1,
                    "jenis_tampilan_name"       : 1,
                    "urutan"                    : 1,
                    "judul_konten"              : 1,
                    "deskripsi"                 : 1,
                    "deskripsi_html"            : 1,
                    "deskripsi_preview"         : 1,
                    "url"                       : 1,
                    "start_timestamp"           : 1,
                    "end_timestamp"             : 1,
                    "str_start_datetime"        : 1,
                    "str_end_datetime"          : 1,
                    "image"                     : 1,
                    "_id"                       : 0
                }
            )

            update_obj = {
                "fk_perusahaan_id"          : params["fk_perusahaan_id"         ],
                "fk_posisi_value"           : params["fk_posisi_value"          ],
                "fk_jenis_tampilan_value"   : params["fk_jenis_tampilan_value"  ],
                "perusahaan_name"           : partner_rec["nama_perusahaan"     ],
                "posisi_name"               : posisi_rec["name"                 ],
                "jenis_tampilan_name"       : jenis_tampilan_rec["name"         ],
                "urutan"                    : int(params["urutan"               ]),
                "judul_konten"              : params["judul_konten"             ],
                "deskripsi"                 : params["deskripsi"                ],
                "deskripsi_html"            : deskripsi_html,
                "deskripsi_preview"         : deskripsi_preview,
                "url"                       : params["url"                      ],
                "start_timestamp"           : start_timestamp,  
                "end_timestamp"             : end_timestamp,    
                "str_start_datetime"        : params["start_datetime"           ],
                "str_end_datetime"          : params["end_datetime"             ]
            }


            if file_image != "":
                update_obj["image"] = file_image
            else:
                update_obj["image"] = rec_before["image"]
            
            # UPDATE KONTEN
            self.mgdDB.db_konten.update(
                {"pkey" : params["fk_konten_id"]},
                {"$set" : update_obj }
            )

            # ADD TO UPDATE HISTORY
            update_konten_history_rec  = database.new(self.mgdDB, "db_update_konten_history")
            update_konten_history_rec.put("fk_user_id",     params["fk_user_id"     ])
            update_konten_history_rec.put("fk_konten_id",   params["fk_konten_id"   ])
            update_konten_history_rec.put("update_notes",   params["update_notes"   ])
            update_konten_history_rec.put("rec_before",     rec_before               )
            update_konten_history_rec.put("rec_after",      update_obj               )
            update_konten_history_rec.insert()



        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "UPDATE_KONTEN_FAILED" )
            response.put( "desc"        , "UPDATE KONTEN FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def

    def _update_status(self, params):
        response = helper.response_msg(
            "UPDATE_KONTEN_STATUS_SUCCESS", "UPDATE KONTEN STATUS SUCCESS", {} , "0000"
        )
        try:
            
            self.mgdDB.db_konten.update_one(
                { "pkey" : params["fk_konten_id"] },
                { "$set" : {
                        "status_value" : params["status_value"]
                    }
                }
            )

            status_history_rec  = database.new(self.mgdDB, "db_konten_status_history")
            status_history_rec.put("fk_user_id",    params["fk_user_id"     ])
            status_history_rec.put("fk_konten_id",  params["fk_konten_id"   ])
            status_history_rec.put("status_value",  params["status_value"   ])
            status_history_rec.put("update_from",   params["update_from"    ])
            status_history_rec.insert()

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "UPDATE_KONTEN_STATUS_FAILED" )
            response.put( "desc"        , "UPDATE KONTEN STATUS FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def

    def _delete(self, params):
        response = helper.response_msg(
            "DELETE_KONTEN_SUCCESS", "DELETE KONTEN SUCCESS", {} , "0000"
        )
        try:
            
            self.mgdDB.db_konten.update_one(
                { "pkey" : params["fk_konten_id"] },
                { "$set" : {
                        "is_deleted" : True
                    }
                }
            )

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "DELETE_KONTEN_FAILED" )
            response.put( "desc"        , "DELETE KONTEN FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def

# end class
