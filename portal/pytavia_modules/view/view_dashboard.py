import sys
import traceback
import time
import json
import datetime
import statistics
from bson import Int64

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

from view import view_core_menu
from view import view_core_display
from view import view_core_header
from view import view_core_footer
from view import view_core_script
from view import view_core_css
from view import view_core_dialog_message

class view_dashboard:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    # FIND DATA USER ACTIVE ------------------THIS NEW DELETE THIS COMMENT AFTER YOU BACK
    def _count_data_user_active(self, params):        
        query = { 
            "status"        : "ACTIVE",
            "is_deleted"    : False,
        }
        users_count = self.mgdDB.db_user.find(query)        
        users_count = users_count.count()   
        #customer_count = 1000
        count_human_format = utils._human_format(users_count)
        return count_human_format
    
    def _count_contact_active(self, params):     
        query = { 
           "status_value"  : "ACTIVE",
            "is_deleted"    : False,
        }
        contact_count = self.mgdDB.db_customer.find(query)   
        contact_count = contact_count.count()
         #customer_count = 1000
        count_human_format = utils._human_format(contact_count)                
        return count_human_format     
    
    def _count_iklan_active(self, params):  
        now            = utils._get_current_datetime(hours = config.JKTA_TZ)
        timestamp      = utils._convert_datetime_to_timestamp(now)   
        
        query = { 
            "is_deleted"        : False,
            "status_value"      : "TAYANG",
            "end_timestamp"     : { "$gte" : timestamp }
        }

        iklan_count = self.mgdDB.db_iklan.find(query)   
        iklan_count = iklan_count.count()       
        #customer_count = 1000
        count_human_format = utils._human_format(iklan_count)                
        return count_human_format
    
    def _count_program_active(self, params):  
        now            = utils._get_current_datetime(hours = config.JKTA_TZ)
        timestamp      = utils._convert_datetime_to_timestamp(now)   
        
        query = { 
            "status_value"      : "TAYANG",
            "end_timestamp"     : { "$gte" : timestamp },
            "is_deleted"        : False
        }
        program_count = self.mgdDB.db_program.find(query)   
        program_count = program_count.count()       
        #customer_count = 1000
        count_human_format = utils._human_format(program_count)                
        return count_human_format
    
    def _count_poi(self, params):         
        query = {            
            "is_deleted"        : False
        }        
        poi_count = self.mgdDB.db_poi.find(query)   
        poi_count = poi_count.count()       
        #customer_count = 1000
        count_human_format = utils._human_format(poi_count)                
        return count_human_format
    
    def _count_rekanan(self, params):        
        query = {            
            "is_deleted"        : False
        }        
        rekanan_count = self.mgdDB.db_brutor_partner.find(query)   
        rekanan_count = rekanan_count.count()       
        #customer_count = 1000
        count_human_format = utils._human_format(rekanan_count)                
        return count_human_format
    
    def _count_tenant_active(self, params):  
        query = { 
            "status_value"      : "ACTIVE",
            "is_deleted"        : False
        }
        tenant_count = self.mgdDB.db_cabang.find(query)   
        tenant_count = tenant_count.count()       
        #customer_count = 1000
        count_human_format = utils._human_format(tenant_count)                
        return count_human_format

    def _count_wisata_active(self, params):  
        now            = utils._get_current_datetime(hours = config.JKTA_TZ)
        timestamp      = utils._convert_datetime_to_timestamp(now)   
        
        query = { 
            "status_value"      : "TAYANG",
            "end_timestamp"     : { "$gte" : timestamp },
            "is_deleted"        : False
        }
        wisata_count = self.mgdDB.db_wisata.find(query)   
        wisata_count = wisata_count.count()       
        #customer_count = 1000
        count_human_format = utils._human_format(wisata_count)                
        return count_human_format
    
    def _count_hunian_active(self, params):  
        now            = utils._get_current_datetime(hours = config.JKTA_TZ)
        timestamp      = utils._convert_datetime_to_timestamp(now)   
        
        query = { 
            "status_value"      : "TAYANG",
            "end_timestamp"     : { "$gte" : timestamp },
            "is_deleted"        : False
        }
        wisata_count = self.mgdDB.db_wisata.find(query)   
        wisata_count = wisata_count.count()       
        #customer_count = 1000
        count_human_format = utils._human_format(wisata_count)                
        return count_human_format
    
    def _count_stasiun(self, params):        
        query = {            
            "is_deleted"        : False
        }        
        rekanan_count = self.mgdDB.db_stasiun.find(query)   
        rekanan_count = rekanan_count.count()       
        #customer_count = 1000
        count_human_format = utils._human_format(rekanan_count)                
        return count_human_format
    

    def _chart_year(self, num_years):     
        # get the current year and month
        now = datetime.datetime.now()
        current_year = now.year
        current_month = now.month
        # num_years = 5
        year_ranges = []
        # FOR YEARS FILTER
        for i in range(num_years):
            target_year = current_year - i

            # Calculate first and last days of target year
            first_day = datetime.datetime(target_year, 1, 1, 0, 0, 0)
            last_day = datetime.datetime(target_year, 12, 31, 23, 59, 59)

            start_date = utils._convert_datetime_to_timestamp(first_day)
            end_date = utils._convert_datetime_to_timestamp(last_day)

            query = { 
                "status_value": "ACTIVE",
                "is_deleted": False,
                "rec_timestamp": {
                    "$gte": Int64(start_date),
                    "$lte": Int64(end_date)
                }
            }

            customer_count = self.mgdDB.db_customer.find(query).count()

            result_date = datetime.date(target_year, 1, 1)
            result_date = result_date.strftime('%Y')

            _year_dict = {"y": customer_count, "x": result_date}
            year_ranges.append(_year_dict)
        year_ranges  = year_ranges[::-1]
        return year_ranges


    def _chart_month(self, num_months):
        # get the current year and month
        now = datetime.datetime.now()
        current_year = now.year
        current_month = now.month

        # FOR MONTH RANGES        
        month_ranges = []
        years_sign = 0
        for i in range(num_months):
           # Calculate target year and month
            target_year = current_year
            target_month = (current_month - i) % 12
            
           
            # Adjust target year if necessary
            if target_month == 0:
                target_month = 12
                years_sign += 1
            
            target_year = target_year - years_sign            
            
            # Calculate first and last days of target month
            first_day = datetime.datetime(target_year, target_month, 1, 0, 0, 0)
            last_day = datetime.datetime(target_year, target_month, 28, 0, 0, 0) + datetime.timedelta(days=4)
            last_day = last_day - datetime.timedelta(days=last_day.day - 1, seconds=1)

            start_date      = utils._convert_datetime_to_timestamp(first_day)            
            end_date        = utils._convert_datetime_to_timestamp(last_day)                      

            query = { 
                "status_value"  : "ACTIVE",
                "is_deleted"    : False,
                "rec_timestamp" : {
                    "$gte"  : Int64(start_date),
                    "$lt"   : Int64(end_date)
                    }
            }

            customer_count = self.mgdDB.db_customer.find(query)               
            customer_count = customer_count.count()

            result_date = datetime.date(target_year, target_month, 1)
            result_date = result_date.strftime('%B %Y')
            
            _month_dict = {"y": customer_count, "x": result_date }
            month_ranges.append(_month_dict)
        
        month_ranges = month_ranges[::-1]
        
        return month_ranges

    def _chart_this_year(self):   
        # get the current year and month
        now = datetime.datetime.now()
        current_year = now.year
        current_month = now.month

         # FOR MONTH IN THIS YEAR
        this_year_ranges = []
        for month in range(1, current_month+1):
            # get the first day of the month
            start_date = datetime.datetime(current_year, month, 1, 0, 0, 0)
            
            # get the last day of the month
            last_day = datetime.date(current_year, month+1, 1) - datetime.timedelta(days=1)
            end_date = datetime.datetime.combine(last_day, datetime.time.max)
                        
            start_date      = utils._convert_datetime_to_timestamp(start_date)            
            end_date        = utils._convert_datetime_to_timestamp(end_date)               
        
            query = { 
                "status_value"  : "ACTIVE",
                "is_deleted"    : False,
                "rec_timestamp" : {
                    "$gte"  : Int64(start_date),
                    "$lt"   : Int64(end_date)
                    }
            }
            customer_count = self.mgdDB.db_customer.find(query)               
            customer_count = customer_count.count()
            
            result_date = datetime.date(current_year, month, 1)
            result_date = result_date.strftime('%B %Y')
            month_dict = {"y": customer_count, "x": result_date }
            
            this_year_ranges.append(month_dict)
        return this_year_ranges



    def _count_growth_customer_date(self, params):     

        now = datetime.datetime.now()
        current_year = now.year
        max_year = int(current_year - 2020)   

        month_list  = [3,6]
        year_list   = [3]
        list_ranges = {}

        list_ranges['this_year'] = self._chart_this_year()

        for i in range(len(month_list)):
            key = f'month_{month_list[i]}'
            list_ranges[key]     = self._chart_month(month_list[i])
            
        for i in range(len(year_list)):
            key = f'year_{year_list[i]}'
            list_ranges[key]     = self._chart_year(year_list[i])

        list_ranges['max_year'] = self._chart_year(max_year)
                   
        return list_ranges

    def html(self, params):
        menu_list               = view_core_menu.view_core_menu().html(params)
        core_display            = view_core_display.view_core_display().html(params)
        params["core_display"]  = core_display         
        core_header             = view_core_header.view_core_header().html(params)
        core_footer             = view_core_footer.view_core_footer().html(params)
        core_script             = view_core_script.view_core_script().html(params)
        core_css                = view_core_css.view_core_css().html(params)
        core_dialog_message     = view_core_dialog_message.view_core_dialog_message().html(params)

        users_total         = self._count_data_user_active(params)  
        contact_total       = self._count_contact_active(params)    
        iklan_total         = self._count_iklan_active(params)   
        program_total       = self._count_program_active(params)   
        poi_total           = self._count_poi(params)   

        rekanan_total       = self._count_rekanan(params)   
        tenant_total        = self._count_tenant_active(params)   
        wisata_total        = self._count_wisata_active(params)   
        hunian_total        = self._count_hunian_active(params)   
        stasiun_total       = self._count_stasiun(params)   

        count_growth_customer_date = self._count_growth_customer_date(params)


        return render_template(
            "dashboard/index.html",
            menu_list_html      = menu_list               ,
            core_display        = core_display            , 
            core_header         = core_header             , 
            core_footer         = core_footer             , 
            core_script         = core_script             , 
            core_css            = core_css                , 
            core_dialog_message = core_dialog_message     ,
            username            = params["username"      ],
            role_position       = params["role_position" ],

            users_total         = users_total,
            contact_total       = contact_total,
            iklan_total         = iklan_total,
            program_total       = program_total,
            poi_total           = poi_total,

            rekanan_total       = rekanan_total,
            tenant_total        = tenant_total,
            wisata_total        = wisata_total,
            hunian_total        = hunian_total,
            stasiun_total       = stasiun_total,
            count_growth_customer_date = count_growth_customer_date
        )                
    # end def
# end class
