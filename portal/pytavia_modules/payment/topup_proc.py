import config_core
import sys
import traceback
import json
import ast
import time
import random
import re
from datetime           import datetime
from werkzeug.utils import secure_filename
import os
import string

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



class topup_proc:
    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def topup_submit(self, params, request_files):    
        result_url = "/topup"
        # Get the current date
        apply_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        reference_id = self.generate_reference_id()

        ######################## voucher section ################################################
        if params["voucher"] != "":
            check_voucher_exist = self.mgdDB.db_config.find_one({
                "name" : params["voucher"],
                "config_type": "VOUCHER"
            })

            # check if voucher exist
            if check_voucher_exist:
                count_user_get_voucher = self.mgdDB.db_voucher_log.find({
                    "voucher_name" : params["voucher"],                    
                }).count()

                # check if kuota voucher full
                if count_user_get_voucher >= int(check_voucher_exist['misc']):
                    response = {
                        "result_url"   : result_url,
                        "notif_type"   : "danger",
                        "msg": "Voucher is no longer available."
                    }
                    return response
                    
                else:      
                    check_user_already_get_voucher = self.mgdDB.db_voucher_log.find_one({
                        "fk_user_id" :  params["fk_user_id"],
                    })

                    if check_user_already_get_voucher:
                        response = {
                            "result_url"   : result_url,
                            "notif_type"   : "warning",
                            "msg": "You have already claimed a voucher, and it can only be used once."
                        }
                        
                        return response
                    else: 
                        params['amount'] = check_voucher_exist['desc']

                        # record log vocher
                        voucher_log_rec = database.new(self.mgdDB, "db_voucher_log")   
                        voucher_log_rec.put("fk_user_id", params["fk_user_id"]) 
                        voucher_log_rec.put("amount_voucher", params['amount'])
                        voucher_log_rec.put("voucher_name", params["voucher"])  
                        voucher_log_rec.insert()

                        # Insert into the database
                        meeting_rec = database.new(self.mgdDB, "db_topup_request")
                        meeting_rec.put("topup_request_id", meeting_rec.get()["pkey"])
                        meeting_rec.put("request_user_id", params["fk_user_id"])  # pkey from db_user
                        meeting_rec.put("amount", int(params['amount']))
                        meeting_rec.put("request_status", "APPROVE")
                        meeting_rec.put("request_date", apply_date)
                        meeting_rec.put("payment_method","VOUCHER")
                        meeting_rec.put("reference_id", reference_id)
                        meeting_rec.put("created_at", apply_date)
                        meeting_rec.put("update_by_admin_at", "")
                        meeting_rec.put("source", "")  # Save the uploaded image path
                        meeting_rec.insert()
                        

                        # update saldo in db_user field: "balance"            
                        user_rec             = self.mgdDB.db_user.find_one(
                            {"fk_user_id"   : params["fk_user_id" ]}                       
                        )

                        current_balance = user_rec["balance"]
                        topup_amount    = int(params['amount'])

                        # sum the old balance with a new one
                        balance = current_balance + topup_amount
                        request_rec           = self.mgdDB.db_user.update_one(
                            {"fk_user_id"   : params["fk_user_id" ]},                       
                            {
                                '$set'            : { "balance" : balance}                
                            }      
                        )    

                        # Flash a success message  
                        params['amount'] = self.format_currency(params['amount'])  

                        response = {
                            "result_url"   : result_url,
                            "notif_type"   : "success",                            
                            "msg"   : f"The '{params['voucher']}' voucher worth {params['amount']} IDR has been successfully processed. Your balance has been updated."
                        }
                            
                        return response
                    

            else:
                response = {
                    "result_url"   : result_url,
                    "notif_type"   : "danger",
                    "msg"   : "Voucher not exist"
                }
                
                return response
            
            ######################## end voucher section ################################################



        # Check if the form contains the 'bukti' file part
        if params["payment_method"] == "":
            response = {
                "result_url"   : result_url,
                "notif_type"   : "danger",
                "msg"   : "Masukan Payment Method"
            }
            
            return response
        
        # Check if the form contains the 'bukti' file part
        if 'bukti' not in request_files:
            response = {
                "result_url"   : result_url,
                "notif_type"   : "danger",
                "msg"   : "No Bukti Transfer"
            }
            
            return response

        file = request_files['bukti']
        if file.content_length > 2 * 1024 * 1024:  # 5MB
            response = {
                "result_url"   : result_url,
                "notif_type"   : "danger",
                "msg"   : "File is too large. Please upload a file smaller than 2MB"
            }
            
            return response

        # Validate the file type
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(self.webapp.root_path, 'static/assets/bukti_transfer', filename)
            file.save(file_path)
            params["source"] = file_path.replace(self.webapp.root_path, '')  # Store relative path

        else:
            response = {
                "result_url"   : result_url,
                "notif_type"   : "danger",
                "msg"   : "Invalid Bukti Transfer"
            }
            
            return response



        # Insert into the database
        meeting_rec = database.new(self.mgdDB, "db_topup_request")
        meeting_rec.put("topup_request_id", meeting_rec.get()["pkey"])
        meeting_rec.put("request_user_id", params["fk_user_id"])  # pkey from db_user
        meeting_rec.put("amount", int(params["amount"]))
        meeting_rec.put("request_status", "PENDING")
        meeting_rec.put("request_date", apply_date)
        meeting_rec.put("payment_method", params["payment_method"])
        meeting_rec.put("reference_id", reference_id)
        meeting_rec.put("created_at", apply_date)
        meeting_rec.put("update_by_admin_at", "")
        meeting_rec.put("source", params["source"])  # Save the uploaded image path
        meeting_rec.insert()

        # Flash a success message      

        params['amount'] = self.format_currency(params['amount'])  

        response = {
            "result_url"   : result_url,
            "notif_type"   : "success",
            "msg"   : f"Your payment of {params['amount']} has been successfully processed. Please wait for confirmation."
        }
            
        return response

    # Helper function to validate allowed file types
    def allowed_file(self, filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def generate_reference_id(self, prefix='TOPUP'):
        # Get current date in YYYYMMDD format
        today_date = datetime.now().strftime('%Y%m%d')
        
        # Generate random alphanumeric string
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        # Concatenate parts to form transaction ID
        reference_id = f"{prefix}_{today_date}_{random_chars}"
        
        return reference_id        

    def format_currency(self,amount):
        """Format the amount into Rupiah currency format."""
        try:
            amount = float(amount)  # Convert to float if it's a string
            return f"Rp {amount:,.0f}".replace(',', '.')
        except ValueError:
            return "Rp 0"  # Default value if conversion fails
# end class
