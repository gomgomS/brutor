import config_core
import sys
import traceback
import json
import ast
import time
import random
import re
from datetime import datetime

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


class register_test_proc:

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
            start_datetime_obj = utils._get_datetime_from_str_date(params["start_datetime"] ,date_format = '%d/%m/%Y %H:%M' )
            start_timestamp    = utils._convert_datetime_to_timestamp(start_datetime_obj)

            end_datetime_obj = utils._get_datetime_from_str_date(params["end_datetime"] ,date_format = '%d/%m/%Y %H:%M' )
            end_timestamp    = utils._convert_datetime_to_timestamp(end_datetime_obj)
          
            # desc_test_html
            desc_test_html = su.unescape(params["desc_test"])

            clean = re.compile('<.*?>')
            params["desc_test"] = re.sub( clean, '',desc_test_html)

            list_desc_test = params["desc_test"].split(' ')
            list_desc_test = list_desc_test[0:10]
            list_desc_test.append("...")
            desc_test_preview = " ".join(list_desc_test)           

            test_rec  = database.new(self.mgdDB, "db_test")
            test_rec.put("test_id",                   test_rec.get()["pkey"          ])
            test_rec.put("activation_class_id",       params["activation_class_id" ]  ) #pkey from db_user
            test_rec.put("fk_user_id",                 params["fk_user_id" ]               ) #pkey from db_user
            test_rec.put("name_test",                 params["name_test"             ])
            test_rec.put("desc_test",			      params["desc_test"             ])
            test_rec.put("desc_test_html",		      desc_test_html                  )
            test_rec.put("desc_test_preview",         desc_test_preview               )                        
            test_rec.put("score_to_pass",             params["score_to_pass"         ])    
            test_rec.put("start_timestamp",           start_timestamp                 )
            test_rec.put("end_timestamp",             end_timestamp                   )
            test_rec.put("str_start_datetime",        params["start_datetime"        ])
            test_rec.put("str_end_datetime",          params["end_datetime"          ])
            test_rec.put("type_test",                 params["type_test"             ])
            test_rec.put("name_test",                 params["name_test"             ])
            test_rec.put("source",                    params["source"             ])
            test_rec.put("status_test",               params["status_test"             ])
            test_rec.insert()                       

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

    def _update(self, params):
        response = helper.response_msg(
            "UPDATE_REGISTER_TEST_SUCCESS", "UPDATE REGISTER TEST SUCCESS", {}, "0000"
        )
        try:
            # Fetch the existing test record
            existing_test = self.mgdDB.db_test.find_one({"test_id": params["test_id"]})
            
            if not existing_test:
                raise ValueError("Test record not found")

            # Convert str datetime to timestamp
            start_datetime_obj = utils._get_datetime_from_str_date(params["start_datetime"], date_format='%d/%m/%Y %H:%M')
            start_timestamp = utils._convert_datetime_to_timestamp(start_datetime_obj)

            end_datetime_obj = utils._get_datetime_from_str_date(params["end_datetime"], date_format='%d/%m/%Y %H:%M')
            end_timestamp = utils._convert_datetime_to_timestamp(end_datetime_obj)

            # Process desc_test_html
            desc_test_html = su.unescape(params["desc_test"])

            clean = re.compile('<.*?>')
            params["desc_test"] = re.sub(clean, '', desc_test_html)

            list_desc_test = params["desc_test"].split(' ')
            list_desc_test = list_desc_test[0:10]
            list_desc_test.append("...")
            desc_test_preview = " ".join(list_desc_test)

            # Prepare the update object
            update_obj = {
                "activation_class_id": params["activation_class_id"],
                "fk_user_id": params["fk_user_id"],
                "name_test": params["name_test"],
                "desc_test": params["desc_test"],
                "desc_test_html": desc_test_html,
                "desc_test_preview": desc_test_preview,
                "score_to_pass": params["score_to_pass"],
                "start_timestamp": start_timestamp,
                "end_timestamp": end_timestamp,
                "str_start_datetime": params["start_datetime"],
                "str_end_datetime": params["end_datetime"],
                "type_test": params["type_test"],
                "status_test": params["status_test"],
                "source": params["source"]
            }

            # Update the test record
            self.mgdDB.db_test.update_one(
                {"test_id": params["test_id"]},
                {"$set": update_obj}
            )

        except Exception as e:
            trace_back_msg = traceback.format_exc()
            self.webapp.logger.debug(traceback.format_exc())

            response.put("status", "UPDATE_REGISTER_TEST_FAILED")
            response.put("desc", "UPDATE REGISTER TEST FAILED")
            response.put("status_code", "9999")
            response.put("data", {"error_message": trace_back_msg})

        return response

    # end def

    def _delete(self, params):
        response = helper.response_msg(
            "DELETE_TEST_SUCCESS", "DELETE TEST SUCCESS", {} , "0000"
        )
        try:                        
            self.mgdDB.db_test.delete_one(
                { "pkey" : params["test_id"] },                
            )

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "DELETE_TEST_FAILED" )
            response.put( "desc"        , "DELETE TEST FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def

    def _add_score_test(self, params):
        response = helper.response_msg(
            "ADD_REGISTER_CLASS_SUCCESS", "ADD REGISTER CLASS SUCCESS", {} , "0000"
        )
        try:     
            # Get the current date
            updated_at           = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    

            # check if pass or not
            if params['score'] >= params["score_to_pass"]:
                status_test = 'PASS'
            else: 
                status_test = 'FAILED'
            
            test_result_rec = database.new(self.mgdDB, "db_test_result")
            test_result_rec.put("result_id",             test_result_rec.get()["pkey"          ])  # Unique identifier for each test result record
            test_result_rec.put("fk_test_id",            params["fk_test_id"                  ])  # Foreign key referencing the test_id from the db_test table
            test_result_rec.put("fk_user_id",            params["fk_student_id"                  ])  # Foreign key referencing the user_id from the user table
            test_result_rec.put("score",                 params["score"                    ])  # The score the student obtained on the test
            test_result_rec.put("status",                status_test                           )  # Status of the result: PASSED, FAILED, INCOMPLETE
            test_result_rec.put("feedback",              params["feedback"                    ])  # Optional feedback or comments on the result        
            test_result_rec.put("updated_at",            updated_at                           )  # Timestamp for the last update to the record
            test_result_rec.insert()                 

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

    def _update_score_test(self, params):
        response = helper.response_msg(
            "UPDATE_REGISTER_CLASS_SUCCESS", "UPDATE REGISTER CLASS SUCCESS", {} , "0000"
        )
        try:     
            # Get the current date
            updated_at           = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    

            # check if pass or not
            if int(params['score']) >= int(params["score_to_pass"]):
                status_test = 'PASS'
            else: 
                status_test = 'FAILED'
            
            update_obj = {
                "fk_test_id": params["fk_test_id"],
                "fk_user_id": params["fk_student_id"],
                "score": params["score"],
                "status": status_test,
                "feedback": params["feedback"],
                "updated_at": updated_at
            }

            # Update the test result record
            self.mgdDB.db_test_result.update_one(
                {"result_id": params["result_id"]},
                {"$set": update_obj}
            )              

        except :
            trace_back_msg = traceback.format_exc() 
            self.webapp.logger.debug(traceback.format_exc())

            response.put( "status"      , "update_REGISTER_CLASS_FAILED" )
            response.put( "desc"        , "update REGISTER CLASS FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def

# end class
