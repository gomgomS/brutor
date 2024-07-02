import config_core
import sys
import traceback
import json
import ast
import time
import random
import re

sys.path.append("pytavia_core")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")

from pytavia_stdlib     import cfs_lib
from pytavia_core       import helper
from pytavia_core       import config
from pytavia_core       import database
from pytavia_stdlib     import utils
from pytavia_stdlib     import idgen
from xml.sax            import saxutils as su



class online_survey_proc:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def _add(self, params):
        response = helper.response_msg(
            "ADD_ONLINE_SURVEY_SUCCESS", "ADD ONLINE SURVEY SUCCESS", {}, "0000"
        )
        try:

            image = params["files"]["image"]

            #process image
            file_image = ""
            file_name = ""
            if image.filename != "":
                try:
                    now_time = int(time.time() * 1000)
                    random_int = random.randint(1000000, 9999999)
                    file_name = "file_" + str(now_time) + "_" + str(random_int)
                    created_time = time.strftime(
                        "%d-%m-%Y", time.localtime(int(time.time())))
                    file_resp = cfs_lib.store_file_to_cfs({
                        "bucket": config.G_IMAGE_BUCKET,
                        "label": config.G_IMAGE_LABEL,
                        "file_data": image,
                        "extension": "DEFAULT",
                        "allow_type": ["DEFAULT"],
                        "file_name": "/online_survey/" + created_time + "/" + file_name
                    })

                    self.webapp.logger.debug(
                        "------------------------------------------")
                    self.webapp.logger.debug(file_resp)
                    self.webapp.logger.debug(
                        "------------------------------------------")

                    action_file = file_resp["message_action"]
                    desc_file = file_resp["message_desc"]
                    data_file = file_resp["message_data"]

                    if action_file != "ADD_CFS_FILE_SUCCES":
                        response.put("status", "ADD_ONLINE_SURVEY_FAILED")
                        response.put("desc", "Upload Image Failed")
                        response.put("status_code", "1001")
                        response.put("data", {"error_message": desc_file})
                        return response
                    #endif

                    file_image = data_file["path"]
                    file_name = data_file["key"]
                except:
                    self.webapp.logger.debug(traceback.format_exc())
                    file_image = ""
                #endtry

            # SAVE ONLINE SURVEY RECORD

            # CONVERT STR DATETIME TO TIMESTAMP
            start_datetime_obj = utils._get_datetime_from_str_date(params["start_datetime"], date_format='%d/%m/%Y %H:%M')
            start_timestamp = utils._convert_datetime_to_timestamp(start_datetime_obj)

            end_datetime_obj = utils._get_datetime_from_str_date(params["end_datetime"], date_format='%d/%m/%Y %H:%M')
            end_timestamp = utils._convert_datetime_to_timestamp(end_datetime_obj)

            # POSISI NAME
            posisi_rec  = self.mgdDB.db_config.find_one(
                {   
                    "config_type"   : "POSISI_DI_APLIKASI",
                    "value"         : params["fk_posisi_value"],
                    "is_deleted"    : False
                }
            )

            # deskripsi_html
            deskripsi_html = su.unescape(params["deskripsi"])

            clean = re.compile('<.*?>')
            params["deskripsi"] = re.sub( clean, '', deskripsi_html)



            online_survey_rec = database.new(self.mgdDB, "db_online_survey")
            online_survey_rec.put("fk_user_id",         params["fk_user_id"             ])
            online_survey_rec.put("fk_posisi_value",    params["fk_posisi_value"        ])
            online_survey_rec.put("posisi_name",		posisi_rec["name"               ])
            online_survey_rec.put("nama_survey",        params["nama_survey"            ])
            online_survey_rec.put("deskripsi",			params["deskripsi"              ])
            online_survey_rec.put("deskripsi_html",		deskripsi_html                   )
            online_survey_rec.put("url",                params["url"                    ])
            online_survey_rec.put("urutan",             int(params["urutan"             ]))
            online_survey_rec.put("start_timestamp",    start_timestamp                 )
            online_survey_rec.put("end_timestamp",      end_timestamp                   )
            online_survey_rec.put("str_start_datetime", params["start_datetime"         ])
            online_survey_rec.put("str_end_datetime",   params["end_datetime"           ])
            online_survey_rec.put("image",              file_image                      )
            online_survey_rec.put("status_value",       "PROSES"                        )
            online_survey_rec.insert()

            # SAVE IMAGE RECORD
            online_survey_pkey = online_survey_rec.get()["pkey"]

            image_rec = database.new(self.mgdDB, "db_online_survey_img")
            image_rec.put("fk_survey_id",    online_survey_pkey)
            image_rec.put("image",          file_image)
            image_rec.insert()

            status_history_rec = database.new(self.mgdDB, "db_online_survey_status_history")
            status_history_rec.put("fk_user_id",    params["fk_user_id" ])
            status_history_rec.put("fk_survey_id",  online_survey_pkey  )
            status_history_rec.put("status_value",  "PROSES"            )
            status_history_rec.put("update_from",   "Tambah Form"       )
            status_history_rec.insert()

        except:
            trace_back_msg = traceback.format_exc()
            self.webapp.logger.debug(traceback.format_exc())

            response.put("status", "ADD_ONLINE_SURVEY_FAILED")
            response.put("desc", "ADD ONLINE SURVEY FAILED")
            response.put("status_code", "9999")
            response.put("data", {"error_message": trace_back_msg})
        # end try
        return response
    # end def

    def _edit(self, params):
        response = helper.response_msg(
            "UPDATE_ONLINE_SURVEY_SUCCESS", "UPDATE ONLINE SURVEY SUCCESS", {}, "0000"
        )
        try:

            image = params["files"]["image"]
            file_image = ""
            file_name = ""
            if image.filename != "":
                try:
                    now_time        = int(time.time() * 1000)
                    random_int      = random.randint(1000000, 9999999)
                    file_name       = "file_" + str(now_time) + "_" + str(random_int)
                    created_time    = time.strftime("%d-%m-%Y", time.localtime(int(time.time())))
                    file_resp = cfs_lib.store_file_to_cfs({
                        "bucket": config.G_IMAGE_BUCKET,
                        "label": config.G_IMAGE_LABEL,
                        "file_data": image,
                        "extension": "DEFAULT",
                        "allow_type": ["DEFAULT"],
                        "file_name": "/online_survey/" + created_time + "/" + file_name
                    })

                    self.webapp.logger.debug(
                        "------------------------------------------")
                    self.webapp.logger.debug(file_resp)
                    self.webapp.logger.debug(
                        "------------------------------------------")

                    action_file = file_resp["message_action"]
                    desc_file = file_resp["message_desc"]
                    data_file = file_resp["message_data"]

                    if action_file != "ADD_CFS_FILE_SUCCES":
                        response.put("status", "ADD_ONLINE_SURVEY_FAILED")
                        response.put("desc", "Upload Image Failed")
                        response.put("status_code", "1001")
                        response.put("data", {"error_message": desc_file})
                        return response
                    #endif

                    file_image = data_file["path"]
                    file_name = data_file["key"]
                except:
                    self.webapp.logger.debug(traceback.format_exc())
                    file_image = ""

                #end try

                self.mgdDB.db_online_survey_img.update_one(
                    {"fk_survey_id": params["fk_survey_id"], "is_deleted": False}, {"$set": {"is_deleted": True}})

                image_rec = database.new(self.mgdDB, "db_online_survey_img")
                image_rec.put("fk_survey_id",      params["fk_survey_id"])
                image_rec.put("image",             file_image)
                image_rec.insert()

            # CONVERT STR DATETIME TO TIMESTAMP
            start_datetime_obj = utils._get_datetime_from_str_date(params["start_datetime"], date_format='%d/%m/%Y %H:%M')
            start_timestamp = utils._convert_datetime_to_timestamp(start_datetime_obj)

            end_datetime_obj = utils._get_datetime_from_str_date(params["end_datetime"], date_format='%d/%m/%Y %H:%M')
            end_timestamp = utils._convert_datetime_to_timestamp(end_datetime_obj)

            # POSISI NAME
            posisi_rec  = self.mgdDB.db_config.find_one(
                {   
                    "config_type"   : "POSISI_DI_APLIKASI",
                    "value"         : params["fk_posisi_value"],
                    "is_deleted"    : False
                }
            )

            # deskripsi_html
            deskripsi_html = su.unescape(params["deskripsi"])

            clean = re.compile('<.*?>')
            params["deskripsi"] = re.sub( clean, '', deskripsi_html)

            # ORIGINAL ONLINE SURVEY REC
            rec_before = self.mgdDB.db_online_survey.find_one(
                {
                    "pkey": params["fk_survey_id"]
                },
                {
                    "fk_posisi_value"       : 1,
                    "posisi_name"           : 1,
                    "nama_survey"           : 1,
                    "deskripsi"             : 1,
                    "deskripsi_html"        : 1,
                    "url"                   : 1,
                    "urutan"                : 1,
                    "start_timestamp"       : 1,
                    "end_timestamp"         : 1,
                    "str_start_datetime"    : 1,
                    "str_end_datetime"      : 1,
                    "image"                 : 1,
                    "_id"                   : 0
                }
            )

            update_obj = {
                "fk_posisi_value"       : params["fk_posisi_value"  ],
                "posisi_name"           : posisi_rec["name"         ],
                "nama_survey"           : params["nama_survey"      ],
                "deskripsi"             : params["deskripsi"        ],
                "deskripsi_html"        : deskripsi_html,
                "url"                   : params["url"              ],
                "urutan"                : int(params["urutan"       ]),
                "start_timestamp"       : start_timestamp,
                "end_timestamp"         : end_timestamp,
                "str_start_datetime"    : params["start_datetime"   ],
                "str_end_datetime"      : params["end_datetime"     ]
            }

            if file_image != "":
                update_obj["image"] = file_image
            else:
                update_obj["image"] = rec_before["image"]

            # UPDATE ONLINE SURVEY
            self.mgdDB.db_online_survey.update(
                {"pkey": params["fk_survey_id"]},
                {"$set": update_obj}
            )

            # ADD TO UPDATE HISTORY
            update_online_survey_history_rec = database.new(self.mgdDB, "db_update_online_survey_history")
            update_online_survey_history_rec.put("fk_user_id",     params["fk_user_id"      ])
            update_online_survey_history_rec.put("fk_survey_id",   params["fk_survey_id"    ])
            update_online_survey_history_rec.put("update_notes",   params["update_notes"    ])
            update_online_survey_history_rec.put("rec_before",     rec_before                )
            update_online_survey_history_rec.put("rec_after",      update_obj                )
            update_online_survey_history_rec.insert()

        except:
            trace_back_msg = traceback.format_exc()
            self.webapp.logger.debug(traceback.format_exc())

            response.put("status", "UPDATE_ONLINE_SURVEY_FAILED")
            response.put("desc", "UPDATE ONLINE SURVEY FAILED")
            response.put("status_code", "9999")
            response.put("data", {"error_message": trace_back_msg})
        # end try
        return response
    # end def

    def _update_status(self, params):
        response = helper.response_msg(
            "UPDATE_ONLINE SURVEY_STATUS_SUCCESS", "UPDATE ONLINE SURVEY STATUS SUCCESS", {}, "0000"
        )
        try:

            self.mgdDB.db_online_survey.update_one(
                {"pkey": params["fk_survey_id"]},
                {"$set": {
                    "status_value": params["status_value"]
                }
                }
            )

            status_history_rec = database.new(self.mgdDB, "db_online_survey_status_history")
            status_history_rec.put("fk_user_id",     params["fk_user_id"    ])
            status_history_rec.put("fk_survey_id",   params["fk_survey_id"  ])
            status_history_rec.put("status_value",   params["status_value"  ])
            status_history_rec.put("update_from",    params["update_from"   ])
            status_history_rec.insert()

        except:
            trace_back_msg = traceback.format_exc()
            self.webapp.logger.debug(traceback.format_exc())

            response.put("status", "UPDATE_ONLINE SURVEY_STATUS_FAILED")
            response.put("desc", "UPDATE ONLINE SURVEY STATUS FAILED")
            response.put("status_code", "9999")
            response.put("data", {"error_message": trace_back_msg})
        # end try
        return response
    # end def

    def _delete(self, params):
        response = helper.response_msg(
            "DELETE_ONLINE_SURVEY_SUCCESS", "DELETE ONLINE SURVEY SUCCESS", {}, "0000"
        )
        try:

            self.mgdDB.db_online_survey.update_one(
                {"pkey": params["fk_survey_id"]},
                {"$set": {
                    "is_deleted": True
                }
                }
            )

        except:
            trace_back_msg = traceback.format_exc()
            self.webapp.logger.debug(traceback.format_exc())

            response.put("status", "DELETE_ONLINE_SURVEY_FAILED")
            response.put("desc", "DELETE ONLINE SURVEY FAILED")
            response.put("status_code", "9999")
            response.put("data", {"error_message": trace_back_msg})
        # end try
        return response
    # end def

# end class
