import sys
import traceback
import requests
import socket
import rapidjson as json

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
from pytavia_core   import helper

from view import view_core_menu
from view import view_core_display
from view import view_core_header
from view import view_core_footer
from view import view_core_script
from view import view_core_css
from view import view_core_dialog_message

from collections import deque

class view_employee:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self):
        pass
    # end def

    def show_menu_list(self, params):
        args            = params['args'] 
        mode            = args["mode"] if "mode" in args else None
        pkey            = args["key"] if "key" in args else None

        doc_edit        = None
        data_list       = None

        form            = {}
        form['name' ]   = "Employee"
        template_string = "employees/employee-list.html"

        terms           = None
        cities          = None
        terms           = self.mgdDB.db_general_config_term_of_payment.find({})
        cities          = self.mgdDB.db_config_city.find({})
        region          = self.mgdDB.db_config_region.find({})
        division        = self.mgdDB.db_config_division.find({})
        role            = self.mgdDB.db_config_role.find({})

        form['cities'   ]   = list( cities )
        form['terms'    ]   = list( terms  )
        form['role'     ]   = list( role   )
     
        form['region'       ]   = list( region   )
        form['division'     ]   = list( division )

        if mode == "insert":
            form['mode'     ]   = "insert"
            template_string     = "employees/employee-add.html"

        elif mode == "edit_profile":
            lst1             = []
            lst2             = []
            form['mode'     ]   = "edit_profile"
            template_string     = "employees/employee-add.html"
            doc_edit            = self.get_employee_by_pkey(pkey)
            if doc_edit:
                ct = self.mgdDB.db_config_region.find_one({ "pkey" : doc_edit['region']}, {"_id":0})
                if ct:
                    lst1.append(ct)
                # end if

                ct1 = self.mgdDB.db_config_division.find_one({ "pkey" : doc_edit['division']}, {"_id":0})
                if ct:
                    lst2.append(ct1)
                # end if

            role                   = self.mgdDB.db_config_role.find_one({"value": doc_edit.get("role")})
            doc_edit['role'     ]  = role
            doc_edit['region'   ]  = lst1
            doc_edit['division' ]  = lst2

        elif mode == "edit_uname":
            form['mode'     ]   = "edit_uname"
            template_string     = "employees/change_user.html"
            doc_edit            = self.get_employee_by_pkey(pkey)

        elif mode == "edit_pwd":
            form['mode'     ]   = "edit_pwd"
            template_string     = "employees/change_password.html"
            doc_edit            = self.get_employee_by_pkey(pkey)
        else:
            lst1             = []
            lst2             = []

            body                = {}
            data_list           = self.get_employee_list(body)
            for i in data_list:
                if i['region']:
                    ct = self.mgdDB.db_config_region.find_one({ "pkey" : i['region']}, {"_id":0})
                    if ct:
                        i['region'] = ct['name']
                    # end if

                if i['division']:
                    ct1 = self.mgdDB.db_config_division.find_one({ "pkey" : i['division']}, {"_id":0})
                    if ct:
                        i['division'] = ct['name']
                # end if

        #end if

        form['template' ]       = template_string

        response = {
            "employee_list"    : data_list,
            "edit_item_rec"    : doc_edit,
            "form"             : form
        }

        return response
    # end def

    def html(self, params):
        menu_list               = view_core_menu.view_core_menu().html(params)
        core_display            = view_core_display.view_core_display().html(params)
        params["core_display"]  = core_display         
        core_header             = view_core_header.view_core_header().html(params)
        core_footer             = view_core_footer.view_core_footer().html(params)
        core_script             = view_core_script.view_core_script().html(params)
        core_css                = view_core_css.view_core_css().html(params)
        core_dialog_message     = view_core_dialog_message.view_core_dialog_message().html(params)
        username                = params["username"      ]
        role_position           = params["role_position" ]
        show_menu_data          = self.show_menu_list( params )
        employee_list           = show_menu_data["employee_list"   ] 
        edit_item_rec           = show_menu_data["edit_item_rec"   ]
        form                    = show_menu_data["form"            ]
        return render_template(
            form['template' ],
            menu_list_html      = menu_list,
            username            = username,
            role_position       = role_position,
            employee_list       = employee_list,
            edit_item_rec       = edit_item_rec,
            form                = form,
            core_display        = core_display,
            core_header         = core_header, 
            core_footer         = core_footer, 
            core_script         = core_script,  
            core_css            = core_css,
            core_dialog_message = core_dialog_message     
        )                
    # end def

    def get_user_role(self, id):
        role                    = ""
        su                      = self.mgdDB.db_super_user.find_one({"pkey": id})
        if not su:
            user                = self.mgdDB.db_user.find_one({"pkey": id})
            if user:
                role            = user['role']
        else:
            role                = "SUPER_USER"
        return role
    # end def

    def req_data(self, params):
        body         = params.get("body"  )
        route        = params.get("route" )
        method       = params.get("method")

        resp = requests.get(config.G_EMPLOYEE_URL + '/v1/api' + route)
        resp.raise_for_status()
        resp = json.loads(resp.text)

        return resp
    # end def

    def get_employee_list(self, body):
        params={}
        params['route' ] = '/employees/list'
        params['method'] = 'POST'
        params['body'  ] =  body
        return self.req_data(params).get("data")
    #end def
    def get_employee_by_pkey(self, pkey):
        params={}
        params['route' ] = '/employees/' + pkey + '/get'
        params['method'] = 'GET'
        return self.req_data(params).get("data")
    #end def
        