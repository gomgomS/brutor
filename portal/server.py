import json
import time
import pymongo
import sys
import urllib.parse
import base64
import urllib
import ast
import pdfkit
import html as html_unescape

from urllib.parse import urlencode

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_modules/auth")
sys.path.append("pytavia_modules/configuration")
sys.path.append("pytavia_modules/cookie")
sys.path.append("pytavia_modules/middleware")
sys.path.append("pytavia_modules/security")
sys.path.append("pytavia_modules/user")
sys.path.append("pytavia_modules/view")



##########################################################
from pytavia_core       import database
from pytavia_core       import config

from pytavia_stdlib     import utils
from pytavia_stdlib     import cfs_lib
from pytavia_stdlib     import idgen
from pytavia_stdlib     import sanitize
from pytavia_stdlib     import security_lib
from pytavia_stdlib     import emailproc


##########################################################
from auth               import auth_util
from auth               import auth_proc
from configuration      import config_all
from configuration      import config_config_general
from configuration      import config_menu_webapp_item_all
from configuration      import config_role
from configuration      import config_setting_menu
from configuration      import config_setting_security_timeout


from cookie             import cookie_engine
from middleware         import browser_security
from security           import security_login
from user               import user_proc

from view               import view_config
from view               import view_config_add_new
from view               import view_config_add_webapp_menu
from view               import view_config_edit_existing
from view               import view_config_general
from view               import view_config_role
from view               import view_config_setting_menu
from view               import view_dashboard
from view               import view_login
from view               import view_signup
from view               import view_user_custom

from view               import view_error_page
##########################################################
# ADDITIONAL
##########################################################
# profile

from view               import view_profile
from view               import view_apply_for_tutor

# _pr ngak bisa dibaca
from _profile          import profile_proc


##########################################################
# LANDINGPAGE
##########################################################

from view               import view_landing_page

##########################################################
# BRUTOR-CMS
##########################################################

from view               import view_general_config
from view               import view_config_menu
from view               import view_config_menu_permission
from view               import view_config_starter
from view               import view_starter

from configuration      import general_config_proc
from configuration      import config_menu_proc
from configuration      import config_menu_permission_proc
from configuration      import config_starter_proc

##########################################################
# USERS
##########################################################

from view               import view_users_active
from view               import view_users_inactive
from view               import view_users_edit_form
from view               import view_users_tambah_form
from view               import view_users_change_password_form

from user               import brutor_user_proc



##########################################################
# MAGISTER CLASS
##########################################################
# REGISTER CLASS

from view               import view_register_class
from view               import view_register_class_add

from manager_class      import register_class_proc

from view               import view_activation_class
from view               import view_activation_class_add

from manager_class      import activation_class_proc

from view               import view_public_class

from manager_class      import public_class_proc

##########################################################
# MAGISTER TEST
##########################################################
# REGISTER TEST

from view               import view_register_test
from view               import view_register_test_add

from manager_test       import register_test_proc

##########################################################
# MAGISTER MEETING
##########################################################
# REGISTER MEETING

from view               import view_register_meeting
from view               import view_register_meeting_add

from manager_meeting       import register_meeting_proc

##########################################################
# MAGISTER USERS
##########################################################
# TUTOR APPROVAL

from view               import view_tutor_approval
from view               import view_tutor_approval_add

from manager_users      import tutor_approval_proc


##########################################################
# MAGISTER PAYMENT
##########################################################
# PAYMENT CONFIRMATION

from view               import view_payment_confirmation

from manager_payment   import payment_confirmation_proc

##########################################################
# PAYMENT
##########################################################
# TOPUP

from view               import view_topup

from payment            import topup_proc

##########################################################
# CONFIG
##########################################################
# LEVEL CLASS

from view               import view_level_class
# from view               import view_terms_and_conditions_edit_form
# from view               import view_tnc_public

from configuration      import level_class_proc

##########################################################


from flask              import request
from flask              import render_template
from flask              import Flask
from flask              import session
from flask              import make_response
from flask              import redirect
from flask              import url_for
from flask              import flash
from flask              import abort
from flask              import jsonify 

from wtforms            import ValidationError

from flask_wtf.csrf     import CSRFProtect
from flask_wtf.csrf     import CSRFError

#
# Main app configurations
#
app                   = Flask( __name__, config.G_STATIC_URL_PATH )
app.secret_key        = config.G_FLASK_SECRET
app.session_interface = cookie_engine.MongoSessionInterface()
csrf                  = CSRFProtect(app)



#
# Utility Function
#
# @app.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     return redirect(url_for("login_html"))
# # end def


def login_precheck(params):
    fk_user_id  = session.get("fk_user_id")

    if fk_user_id == None:
        session.clear()
        return redirect(url_for("login_html"))
    # end if
# end def

def role_precheck(params):
    role  = session.get("role")
  
    if role not in params['role_with_access']:     
        flash("You do not have the authority to access this page.", "danger")   
        return redirect(url_for("dashboard_html"))


# 
# Authentication
#
# @app.route('/')
# def hello():
#     return redirect(url_for('login_html'))
# end def


@app.route("/send")
def send_ver_email():      
    
    html   = emailproc.send_verification_email(email)
    return redirect(url_for("landingpage"))

@app.route("/auth/send_verification_email")
def auth_send_verification_email():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["email"]           = session.get("email")
    params["fk_user_id"     ] = session.get("fk_user_id")
    params["username"       ] = session.get("username")
    params["role_position"  ] = session.get("role_position")

    logging_tm           = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : ""
    })

    landing_url = auth_proc.auth_proc(app).send_verification_email( params )
    return redirect( landing_url )
   
    # end if

@app.route("/auth/check_verification_email", methods=["POST"])
def auth_check_verification_email():
    redirect_return = login_precheck({})
    params     = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id")
    landing_url   = auth_proc.auth_proc(app).check_verification_email( params )   
       
    return redirect( landing_url )   
    # end if

@app.route("/")
def landingpage():
    fk_user_id  = session.get("fk_user_id")
    params = request.form.to_dict()

    if fk_user_id != None:
        landing_url = auth_proc.auth_proc(app).get_landing_url( params )
        return redirect( landing_url )
    # end if

    html   = view_landing_page.view_landing_page().html( params )
    return html

@app.route("/signup")
def signup_html():
    fk_user_id  = session.get("fk_user_id")
    params = request.form.to_dict()

    if fk_user_id != None:
        landing_url = auth_proc.auth_proc(app).get_landing_url( params )
        return redirect( landing_url )
    # end if

    html   = view_signup.view_signup().html( params )
    return html
# end def

@app.route("/auth/register", methods=["POST"])
def auth_register():
    token      = session.pop('_csrf_token', None)
    params     = sanitize.clean_html_dic(request.form.to_dict())
    response   = auth_proc.auth_proc(app).register( params )   
    
    return redirect(url_for("login_html"))
    # end if
# end def

@app.route("/login")
def login_html():
    fk_user_id  = session.get("fk_user_id")
    params = request.form.to_dict()

    if fk_user_id != None:
        landing_url = auth_proc.auth_proc(app).get_landing_url( params )
        return redirect( landing_url )
    # end if

    html   = view_login.view_login().html( params )
    return html
# end def

@app.route("/auth/login", methods=["POST"])
def auth_login():
    token      = session.pop('_csrf_token', None)
    params     = sanitize.clean_html_dic(request.form.to_dict())
    response   = auth_proc.auth_proc(app).login( params )
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "LOGIN_SUCCESS":
        session["user_uuid"     ] = m_data["user_uuid"     ]
        session["fk_user_id"    ] = m_data["fk_user_id"     ]
        session["username"      ] = m_data["username"       ]
        session["role"          ] = m_data["role"           ]
        session["email"         ] = m_data["email"           ]
        security_login.security_login(app).add_cookie({})

        landing_url = auth_proc.auth_proc(app).get_landing_url( params )
        return redirect( landing_url )
    else:
        return redirect(url_for("login_html"))
    # end if
# end def

@app.route("/auth/logout", methods=["GET", "POST"])
def auth_logout():
    params = {}
    params["fk_user_id"] = session.get("fk_user_id")
    logging_tm = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "AUTH_LOGOUT"
    })
    response = auth_proc.auth_proc(app).logout( params )
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "LOGOUT_SUCCESS":
        session.clear()
        return redirect(url_for("login_html"))
    else:
        return False
    # end if
# end def

#
# Profile
#
@app.route("/profile")
def profile_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id")
    params["username"       ] = session.get("username")
    params["role_position"  ] = session.get("role_position")

    logging_tm           = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "USER_DASHBOARD"
    })
    
    html      = view_profile.view_profile(app).html( params )
    html_resp = make_response( html )
    html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return html_resp
# end def

@app.route("/profile/update", methods=["POST"])
def profile_update_cv():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["old_email"]           = session.get("email")
    params["old_username"   ] = session.get("username")
    params["fk_user_id"     ] = session.get("fk_user_id")
    params["role_position"  ] = session.get("role_position")

    logging_tm           = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : ""
    })

    landing_url = profile_proc.profile_proc(app).update_cv( params )
    return redirect( landing_url )
   
    # end if

@app.route("/profile/send_cv", methods=["POST"])
def profile_send_cv():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["email"]           = session.get("email")
    params["fk_user_id"     ] = session.get("fk_user_id")
    params["username"       ] = session.get("username")
    params["role_position"  ] = session.get("role_position")

    logging_tm           = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : ""
    })

    landing_url = profile_proc.profile_proc(app).send_cv( params )
    return redirect( landing_url )
   
    # end if

@app.route("/profile/change_portal/tutor")
def profile_change_portal_tutor():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["email"]           = session.get("email")
    params["fk_user_id"     ] = session.get("fk_user_id")
    params["username"       ] = session.get("username")
    params["role_position"  ] = session.get("role_position")

    logging_tm           = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : ""
    })

    landing_url = profile_proc.profile_proc(app).change_portal_tutor( params )

    session["role"          ] = 'TUTOR'
    return redirect( landing_url )
   
    # end if

@app.route("/apply_for_tutor")
def apply_for_tutor_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id")
    params["username"       ] = session.get("username")
    params["role_position"  ] = session.get("role_position")

    logging_tm           = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "USER_DASHBOARD"
    })
    
    html      = view_apply_for_tutor.view_apply_for_tutor(app).html( params )
    html_resp = make_response( html )
    html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return html_resp
# end def
#
# Dashboard
#
@app.route("/user/dashboard")
def dashboard_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id")
    params["username"       ] = session.get("username")
    params["role_position"  ] = session.get("role_position")
   
    logging_tm           = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "USER_DASHBOARD"
    })
    
    html      = view_dashboard.view_dashboard(app).html( params )
    html_resp = make_response( html )
    html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return html_resp
# end def



#
# List User
#
@app.route("/user/list")
def list_user_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "USER_LIST"
    })
    
    html = view_user_custom.view_user_custom(app).html( params )
    html_resp = make_response( html )
    html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return html_resp
# end def

@app.route("/process/admin/user/add", methods=["POST"])
def proc_user_add():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "PROCESS_ADMIN_USER_ADD"
    })
    response   = user_proc.user_proc(app).update(params)
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    return redirect("/user/list")
# end def

@app.route("/process/admin/user/edit", methods=["POST"])
def proc_user_edit():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params              = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "PROCESS_ADMIN_USER_EDIT"
    })
    response     = user_proc.user_proc(app).edit( params )
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "EDIT_USER_SUCCESS":
        return redirect("/user/list")
    else:
        return redirect("/login")
    # end if
# end def

@app.route("/process/admin/user/activate", methods=["POST"])
def proc_user_activated():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params              = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "PROCESS_ADMIN_USER_ACTIVATE"
    })
    response     = user_proc.user_proc(app).activate( params )
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "ACTIVE_USER_SUCCESS":
        return redirect("/user/list")
    else:
        return redirect("/login")
    # end if
# end def

@app.route("/process/admin/user/remove", methods=["POST"])
def proc_user_remove():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params              = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "PROCESS_ADMIN_USER_REMOVE"
    })
    response     = user_proc.user_proc(app).remove(params)
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "REMOVE_USER_SUCCESS":
        return redirect("/user/list")
    else:
        return redirect("/login")
    # end if
# end def



#
# Configuration
#
@app.route("/user/config")
def view_config_list_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params                     = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id")
    params["username"       ] = session.get("username")
    params["role"  ] = session.get("role")
    

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "USER_CONFIG"
    })
    

    html      = view_config.view_config().html( params )
    html_resp = make_response( html )
    html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return html_resp
# end def

@app.route("/user/config-add-new")
def view_config_add_new_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                    = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id")
    params["username"       ] = session.get("username")
    params["role_position"  ] = session.get("role_position")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "USER_CONFIG-ADD-NEW"
    })
    
    html      = view_config_add_new.view_config_add_new().html( params )
    html_resp = make_response( html )
    html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return html_resp
# end def

@app.route("/user/config-edit-existing")
def view_config_edit_current_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params                    = sanitize.clean_html_dic(request.args.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id")
    params["username"       ] = session.get("username")
    params["role_position"  ] = session.get("role_position")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "USER_CONFIG-EDIT-EXISTING"
    })
    
    html      = view_config_edit_existing.view_config_edit_existing().html(params)
    html_resp = make_response( html )
    html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return html_resp
# end def

@app.route("/process/config/add/all", methods=["POST"])
def proc_config_update_all():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
    "fk_user_id"  : params["fk_user_id"] ,
    "route_name"  : "CONFIG_ADD_ALL"
    })
    response = config_all.config_all().add(params)
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "ADD_CONFIG_ALL_SUCCESS":
        return redirect("/user/config")
    else:
        return redirect("/login")
    # end if
# end def

@app.route("/process/config/edit/all", methods=["POST"])
def proc_config_edit_all():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"] ,
        "route_name"  : "PROCESS_CONFIG_EDIT_ALL"
        })
    response = config_all.config_all().edit(params)
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "EDIT_CONFIG_ALL_SUCCESS":
        return redirect("/user/config")
    else:
        return redirect("/login")
    # end if
# end def



#
# System Setting
#
@app.route("/user/config/setting-menu/add", methods=["GET"])
def config_setting_menu_config():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params                    = sanitize.clean_html_dic(request.args.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id")
    params["username"       ] = session.get("username")
    params["role_position"  ] = session.get("role_position")
    
    logging_tm   = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "USER_CONFIG_SETTING-MENU"
    })
    html     = view_config_setting_menu.view_config_setting_menu().html(params)
    html_resp = make_response( html )
    html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return html_resp
# end def

@app.route("/process/user/setting/security", methods=["POST"])
def config_user_setting_security():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "PROCESS_USER_SETTIING_SECURITY"
    })
    response = config_setting_security_timeout.config_setting_security_timeout().update_security( params )
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "UPDATE_CONFIG_SET_SECURITY_SUCCESS":
        return redirect("/user/setting")
    else:
        return redirect("/login")
    # end if
# end def


@app.route("/process/config/add/setting-menu", methods=["POST"])
def proc_config_setting_menu():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "PROCES_CONFIG_ADD_SETTING-MENU"
    })
    response = config_setting_menu.config_setting_menu().update( params )
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "ADD_CONFIG_MENU_SETTING_SUCCESS":
        return redirect("/user/config/setting-menu/add?id=CONF_SETTING_MENU")
    else:
        return redirect("/login")
    # end if
# end def

@app.route("/process/user/setting/timeout", methods=["POST"])
def config_user_setting_timeout():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "PROCESS_USER_SETTIING_TIMEOUT"
    })
    response = config_setting_security_timeout.config_setting_security_timeout().update_timeout( params )
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "UPDATE_CONFIG_SET_TIMEOUT_SUCCESS":
        return redirect("/user/setting")
    else:
        return redirect("/login")
    # end if
# end def



#
# System General
#
@app.route("/user/config/general/add", methods=["GET"])
def config_webapp_general_config():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.args.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"    )
    params["username"       ] = session.get("username"      )
    params["role_position"  ] = session.get("role_position" )

    logging_tm   = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "USER_CONFIG_GENERAL-CONF"
    })
    html     = view_config_general.view_config_general().html(params)
    html_resp = make_response( html )
    html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return html_resp
# end def



@app.route("/process/config/add/general", methods=["POST"])
def proc_config_update_general_config():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
    "fk_user_id"  : params["fk_user_id"] ,
    "route_name"  : "PROCESS_CONFIG_ADD_GENERAL"
    })
    response = config_config_general.config_config_general().update( params )
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "ADD_CONFIG_GENERAL_SUCCESS":
        return redirect("/user/config/general/add?id=GENERAL_CONFIGURATION")
    else:
        return redirect("/login")
    # end if
# end def

@app.route("/process/config/del/general", methods=["GET"])
def proc_config_remove_general_config():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.args.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
    "fk_user_id"  : params["fk_user_id"] ,
    "route_name"  : "PROCESS_CONFIG_DEL_GENERAL"
    })
    response = config_config_general.config_config_general().remove(params)
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "REMOVE_CONFIG_DONGLE_FUNCTION_SUCCESS":
        return redirect("/user/config/general/add?id=GENERAL_CONFIGURATION")
    else:
        return redirect("/login")
    # end if
# end def



#
# Config Menu
#
@app.route("/user/config/webapp-menu-all/add", methods=["GET"])
def config_webapp_menu_all_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params                    = sanitize.clean_html_dic(request.args.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id")
    params["username"       ] = session.get("username")
    params["role_position"  ] = session.get("role_position")

    logging_tm   = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "USER_CONFIG_WEBAPP-MENU"
    })
    html     = view_config_add_webapp_menu.view_config_add_webapp_menu().html(params)
    html_resp = make_response( html )
    html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return html_resp
# end def

@app.route("/process/config/add/web_menu", methods=["POST"])
def proc_config_update_web_menu_all():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
    "fk_user_id"  : params["fk_user_id"] ,
    "route_name"  : "PROCESS_CONFIG_ADD_WEB-MENU"
    })
    response = config_menu_webapp_item_all.config_menu_webapp_item_all().update(params)
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "ADD_MENU_CONFIG_ITEM_SUCCESS":
        return redirect("/user/config/webapp-menu-all/add?id=WEBAPP_MENU_ALL_ITEMS")
    else:
        return redirect("/login")
    # end if
# end def

@app.route("/process/config/del/web_menu", methods=["GET"])
def proc_config_del_web_menu_all():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.args.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
    "fk_user_id"  : params["fk_user_id"] ,
    "route_name"  : "PROCESS_CONFIG_DEL_WEB-MENU"
    })
    response = config_menu_webapp_item_all.config_menu_webapp_item_all().remove(params)
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "REMOVE_MENU_CONFIG_ITEM_SUCCESS":
        return redirect("/user/config/webapp-menu-all/add?id=WEBAPP_MENU_ALL_ITEMS")
    else:
        return redirect("/login")
    # end if
# end def




#
# Config Role
#
@app.route("/user/config/role/add", methods=["GET"])
def config_webapp_role_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params                    = sanitize.clean_html_dic(request.args.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id")
    params["username"       ] = session.get("username")
    params["role_position"  ] = session.get("role_position")



    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : "USER_CONFIG_ROLE_ADD"
    })
    html     = view_config_role.view_config_role().html(params)
    html_resp = make_response( html )
    html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return html_resp
# end def

@app.route("/process/config/add/role", methods=["POST"])
def proc_config_update_role():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
    "fk_user_id"  : params["fk_user_id"] ,
    "route_name"  : "PROCESS_CONFIG_ADD_ROLE"
    })
    response = config_role.config_role().update( params )
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "ADD_CONFIG_ROLE_SUCCESS":
        return redirect("/user/config/role/add?id=USER_ROLE")
    else:
        return redirect("/login")
    # end if
# end def

@app.route("/process/config/del/role", methods=["GET"])
def proc_config_remove_role():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.args.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"] ,
        "route_name"  : "PROCESS_CONFIG_DEL_ROLE"
        })
    response = config_role.config_role().remove(params)
    
    m_action   = response["message_action" ]
    m_title    = response["message_title"  ]
    m_desc     = response["message_desc"   ]
    m_data     = response["message_data"   ]
    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if
    if m_action == "REMOVE_CONFIG_ROLE_SUCCESS":
        return redirect("/user/config/role/add?id=USER_ROLE")
    else:
        return redirect("/login")
    # end if
# end def


# CONFIGURATION GENERAL

@app.route("/configuration/general_config")
def view_general_config_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                           = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    params["config_type"    ] = request.args.get('config_type'  )

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_GENERAL_CONFIG"
    })
    
    response = view_general_config.view_general_config(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : ""
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/configuration/general_config/add", methods=["POST"])
def proc_general_config_add():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_GENERAL_CONFIG_ADD"
    })

    response   = general_config_proc.general_config_proc(app)._add(params)
    
    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect("/configuration/general_config?config_type=" + params["config_type"])
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : "/configuration/general_config?config_type=" + params["config_type"]
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/configuration/general_config/update", methods=["POST"])
def proc_general_config_update():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_GENERAL_CONFIG_UPDATE"
    })

    response   = general_config_proc.general_config_proc(app)._update(params)
    
    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect("/configuration/general_config?config_type=" + params["config_type"])
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : "/configuration/general_config?config_type=" + params["config_type"]
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/configuration/general_config/delete", methods=["POST"])
def proc_general_config_delete():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    logging_tm = int(time.time() * 1000)

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_GENERAL_CONFIG_DELETE"
    })

    response   = general_config_proc.general_config_proc(app)._delete(params)

    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect("/configuration/general_config?config_type=" + params["config_type"])
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : "/configuration/general_config?config_type=" + params["config_type"]
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def


@app.route("/configuration/menu")
def view_config_menu_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                    = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_CONFIG_MENU"
    })

    response = view_config_menu.view_config_menu(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : "/user/config"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/configuration/config_menu/add", methods=["POST"])
def proc_config_menu_add():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_CONFIG_MENU_ADD"
    })

    response   = config_menu_proc.config_menu_proc(app)._add(params)

    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect("/configuration/menu")
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : "/configuration/menu"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/configuration/config_menu/update", methods=["POST"])
def proc_config_menu_update():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_CONFIG_MENU_UPDATE"
    })

    response   = config_menu_proc.config_menu_proc(app)._update(params)

    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect("/configuration/menu")
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : "/configuration/menu"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/configuration/config_menu/delete", methods=["POST"])
def proc_config_menu_delete():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_CONFIG_MENU_DELETE"
    })
    
    response   = config_menu_proc.config_menu_proc(app)._delete(params)

    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect("/configuration/menu")
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : "/configuration/menu"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/configuration/starter")
def view_config_starter_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                    = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_CONFIG_STARTER"
    })

    response = view_config_starter.view_config_starter(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : "/user/config"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/configuration/config_starter/add", methods=["POST"])
def proc_config_starter_add():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_CONFIG_STARTER_ADD"
    })

    response   = config_starter_proc.config_starter_proc(app)._add(params)

    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect("/configuration/starter")
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : "/configuration/starter"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/configuration/config_starter/update", methods=["POST"])
def proc_config_starter_update():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_CONFIG_STARTER_UPDATE"
    })
    
    response   = config_starter_proc.config_starter_proc(app)._update(params)

    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect("/configuration/starter")
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : "/configuration/starter"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/configuration/config_starter/delete", methods=["POST"])
def proc_config_starter_delete():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_CONFIG_STARTER_DELETE"
    })
    
    response   = config_starter_proc.config_starter_proc(app)._delete(params)

    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect("/configuration/starter")
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : "/configuration/starter"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def 


@app.route("/configuration/menu_permission")
def view_config_menu_permission_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                           = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_CONFIG_MENU_PERMISSION"
    })

    response = view_config_menu_permission.view_config_menu_permission(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : "/user/config"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def


@app.route("/configuration/config_menu_permission/add", methods=["POST"])
def proc_config_menu_permission_add():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_CONFIG_MENU_PERMISSION_ADD"
    })

    response   = config_menu_permission_proc.config_menu_permission_proc(app)._add(params)

    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect("/configuration/menu_permission")
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : "/configuration/menu_permission"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/configuration/config_menu_permission/update", methods=["POST"])
def proc_config_menu_permission_update():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_CONFIG_MENU_PERMISSION_UPDATE"
    })

    response   = config_menu_permission_proc.config_menu_permission_proc(app)._update(params)

    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect("/configuration/menu_permission")
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : "/configuration/menu_permission"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/configuration/config_menu_permission/delete", methods=["POST"])
def proc_config_menu_permission_delete():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"] = session.get("fk_user_id")
    logging_tm = int(time.time() * 1000)

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_CONFIG_MENU_PERMISSION_DELETE"
    })
    
    response   = config_menu_permission_proc.config_menu_permission_proc(app)._delete(params)

    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect("/configuration/menu_permission")
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : "/configuration/menu_permission"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def


##########################################################
# STARTER
##########################################################
@app.route("/starter")
def view_starter_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                    = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role"     )
    params["username"       ] = session.get("username"          )
    params["menu_value"     ] = request.args.get('menu_value'     )

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_STARTER"
    })


    response = view_starter.view_starter(app).html( params )
    response_data  = response.get("data") 


    # check permission access user    
    role_have_access = response_data["permission_role_list"]

    dashboard_return = role_precheck({"role_with_access":role_have_access})
    if dashboard_return:
        return dashboard_return

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : "#"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

##########################################################
# USERS
##########################################################
@app.route("/users/active")
def view_users_active_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    dashboard_return = role_precheck({"role_with_access":["ADMIN"]})
    if dashboard_return:
        return dashboard_return

    



    params = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"    )
    params["role"           ] = session.get("role" )
    params["username"       ] = session.get("username"      )
    params["order_by"       ] = request.args.get('order_by' )
    params["keyword"        ] = request.args.get('keyword'  )
    params["page"           ] = request.args.get('page'     )
    params["entry"          ] = request.args.get('entry'    )
    params["sort_by"        ] = request.args.get('sort_by'  )


    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id": params["fk_user_id"],
        "route_name": "VIEW_USERS_ACTIVE"
    })

    response = view_users_active.view_users_active(app).html(params)
    response_data = response.get("data")

    if "SUCCESS" in response.get("status"):
        html = response_data["html"]
        html_resp = make_response(html)
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action": response.get("status"),
            "message_desc": response.get("desc"),
            "message_data": response_data["error_message"],
            "redirect": "/login"
        }
        return redirect(url_for("view_error_page_html", data=err_message))
# end def

@app.route("/users/inactive")
def view_users_inactive_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"    )
    params["role_position"  ] = session.get("role_position" )
    params["username"       ] = session.get("username"      )
    params["order_by"       ] = request.args.get('order_by' )
    params["keyword"        ] = request.args.get('keyword'  )
    params["page"           ] = request.args.get('page'     )
    params["entry"          ] = request.args.get('entry'    )
    params["sort_by"        ] = request.args.get('sort_by'  )


    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id": params["fk_user_id"],
        "route_name": "VIEW_USERS_INACTIVE"
    })

    response = view_users_inactive.view_users_inactive(app).html(params)
    response_data = response.get("data")

    if "SUCCESS" in response.get("status"):
        html = response_data["html"]
        html_resp = make_response(html)
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action": response.get("status"),
            "message_desc": response.get("desc"),
            "message_data": response_data["error_message"],
            "redirect": "/users/active"
        }
        return redirect(url_for("view_error_page_html", data=err_message))
# end def

@app.route("/users/tambah_user_form")
def view_users_tambah_form_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                      = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"         ] = session.get("fk_user_id"            )
    params["role_position"      ] = session.get("role_position"         )
    params["username"           ] = session.get("username"              )
    params["redirect"           ] = request.args.get('redirect'         )

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_USERS_EDIT_FORM"
    })

    response = view_users_tambah_form.view_users_tambah_form(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : params["redirect"]
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def


@app.route("/users/edit_users_form")
def view_users_edit_form_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                           = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"         ] = session.get("fk_user_id"            )
    params["role_position"      ] = session.get("role_position"         )
    params["username"           ] = session.get("username"              )
    params["redirect"           ] = request.args.get('redirect'         )
    params["fk_edit_user_id"    ] = request.args.get('fk_edit_user_id'  )

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_USERS_EDIT_FORM"
    })

    response = view_users_edit_form.view_users_edit_form(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : params["redirect"]
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/users/change_password_form")
def view_users_change_password_form_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                           = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"         ] = session.get("fk_user_id"            )
    params["role_position"      ] = session.get("role_position"         )
    params["username"           ] = session.get("username"              )
    params["redirect"           ] = request.args.get('redirect'         )
    params["fk_edit_user_id"    ] = request.args.get('fk_edit_user_id'  )
    params["username"           ] = request.args.get('username'         )

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_USERS_EDIT_FORM"
    })

    response = view_users_change_password_form.view_users_change_password_form(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : params["redirect"]
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def


@app.route("/users/add", methods=["POST"])
def proc_users_add():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    files = request.files
    params = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id" ] = session.get("fk_user_id")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id": params["fk_user_id"],
        "route_name": "PROC_USERS_ADD"
    })

    response = brutor_user_proc.brutor_user_proc(app)._add(params)

    m_action    = response.get("status" )
    m_title     = response.get("status" )
    m_desc      = response.get("desc"   )
    m_data      = response.get("data"   )

    if m_title != "" or m_desc != "":
        flash(m_title, "title")
        flash(m_desc, "desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect(params["redirect"])
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"    ],
            "redirect"          : params["redirect"         ]
        }
        return redirect(url_for("view_error_page_html", data=err_message))
# end def

@app.route("/users/edit", methods=["POST"])
def proc_users_update():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    files = request.files
    params = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"    )
    params["role_position"  ] = session.get("role_position" )

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id": params["fk_user_id"],
        "route_name": "PROC_USERS_UPDATE"
    })

    response = brutor_user_proc.brutor_user_proc(app)._update_details(params)

    m_action    = response.get("status" )
    m_title     = response.get("status" )
    m_desc      = response.get("desc"   )
    m_data      = response.get("data"   )

    if m_title != "" or m_desc != "":
        flash(m_title, "title")
        flash(m_desc, "desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect(params["redirect"])
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"    ],
            "redirect"          : params["redirect"         ]
        }
        return redirect(url_for("view_error_page_html", data=err_message))
# end def

@app.route("/users/change_password", methods=["POST"])
def proc_users_password_change():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    files = request.files
    params = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"    )
    params["role_position"  ] = session.get("role_position" )

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id":   params["fk_user_id"],
        "route_name":   "PROC_USER_CHANGE_PASSWORD"
    })

    response = brutor_user_proc.brutor_user_proc(app)._change_password(params)

    m_action    = response.get("status" )
    m_title     = response.get("status" )
    m_desc      = response.get("desc"   )
    m_data      = response.get("data"   )

    if m_title != "" or m_desc != "":
        flash(m_title, "title")
        flash(m_desc, "desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect(params["redirect"])
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"    ],
            "redirect"          : params["redirect"         ]
        }
        return redirect(url_for("view_error_page_html", data=err_message))
# end def


@app.route("/users/toggle_status", methods=["POST"])
def proc_users_status_update():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    files = request.files
    params = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"    )
    params["role_position"  ] = session.get("role_position" )

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id":   params["fk_user_id"],
        "route_name":   "PROC_USER_TOGGLE_STATUS"
    })

    response = brutor_user_proc.brutor_user_proc(app)._toggle_status(params)

    m_action    = response.get("status" )
    m_title     = response.get("status" )
    m_desc      = response.get("desc"   )
    m_data      = response.get("data"   )

    if m_title != "" or m_desc != "":
        flash(m_title, "title")
        flash(m_desc, "desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect(params["redirect"])
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"    ],
            "redirect"          : params["redirect"         ]
        }
        return redirect(url_for("view_error_page_html", data=err_message))
# end def


##########################################################
# MANAGER CLASS - Register Class
##########################################################
@app.route("/register_class")
def view_register_class_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                           = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    params["order_by"       ] = request.args.get('order_by'     )
    params["keyword"        ] = request.args.get('keyword'      )
    params["page"           ] = request.args.get('page'         )
    params["entry"          ] = request.args.get('entry'        )
    params["sort_by"        ] = request.args.get('sort_by'      )

    params["start_date"     ] = request.args.get('start_date'   )
    params["end_date"       ] = request.args.get('end_date'     )
    

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_KONTEN_PROSES"
    })

    response = view_register_class.view_register_class(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html        = html_unescape.unescape( html )
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : "/pengelolaan_konten/proses"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/register_class/register_class_add_form")
def view_register_class_add_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                           = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    params["redirect"       ] = request.args.get('redirect'     )

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_KONTEN_TAMBAH_FORM"
    })
    
    response = view_register_class_add.view_register_class_add(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : params["redirect"]
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/register_class/add", methods=["POST"])
def proc_register_class_add():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    #tandai
    files                 = request.files
    params                = sanitize.clean_html_dic(request.form.to_dict())

    classId               = sanitize.clean_html_dic(request.form.to_dict(flat=False)) # get form data with list values    
    params['classId']     = classId.get('classId', [])
    params["fk_user_id" ] = session.get("fk_user_id")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_register_class_ADD"
    })


    response   = register_class_proc.register_class_proc(app)._add(params)

    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect(params["redirect"])
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : params["redirect"]
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

##########################################################
# MANAGER CLASS - Activation Class
##########################################################
@app.route("/activation_class")
def view_activation_class_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                           = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    params["order_by"       ] = request.args.get('order_by'     )
    params["keyword"        ] = request.args.get('keyword'      )
    params["page"           ] = request.args.get('page'         )
    params["entry"          ] = request.args.get('entry'        )
    params["sort_by"        ] = request.args.get('sort_by'      )

    params["start_date"     ] = request.args.get('start_date'   )
    params["end_date"       ] = request.args.get('end_date'     )
    

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_KONTEN_PROSES"
    })

    response = view_activation_class.view_activation_class(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html        = html_unescape.unescape( html )
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : "/pengelolaan_konten/proses"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/activation_class/activation_class_add_form")
def view_activation_class_add_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                           = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    params["redirect"       ] = request.args.get('redirect'     )

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_KONTEN_TAMBAH_FORM"
    })
    
    response = view_activation_class_add.view_activation_class_add(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : params["redirect"]
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/activation_class/add", methods=["POST"])
def proc_activation_class_add():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    #tandai
    files                 = request.files
    params                = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id" ] = session.get("fk_user_id")
    params["files"      ] = files
    app.logger.debug(files)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_activation_class_ADD"
    })


    response   = activation_class_proc.activation_class_proc(app)._add(params)

    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect(params["redirect"])
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : params["redirect"]
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

##########################################################
# MANAGER CLASS - Public Class
##########################################################
@app.route("/public_class")
def view_public_class_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                    = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    params["order_by"       ] = request.args.get('order_by'     )
    params["keyword"        ] = request.args.get('keyword'      )
    params["page"           ] = request.args.get('page'         )
    params["entry"          ] = request.args.get('entry'        )
    params["sort_by"        ] = request.args.get('sort_by'      )

    params["start_date"     ] = request.args.get('start_date'   )
    params["end_date"       ] = request.args.get('end_date'     )
    

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_KONTEN_PROSES"
    })

    response = view_public_class.view_public_class(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html        = html_unescape.unescape( html )
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : "/pengelolaan_konten/proses"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/buy_public_class/<class_id>")
def buy_public_class_(class_id):
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return


    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"   ] = session.get("fk_user_id")
    params["class_id"   ] = class_id

    logging_tm           = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : ""
    })

    # landing_url = tutor_approval_proc.tutor_approval_proc(app).approval_tutor( params )
    landing_url = public_class_proc.public_class_proc(app).buy_public_class( params )
    return redirect( landing_url )



##########################################################
# MANAGER TEST - Register Test
##########################################################
@app.route("/register_test")
def view_register_test_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                    = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    params["order_by"       ] = request.args.get('order_by'     )
    params["keyword"        ] = request.args.get('keyword'      )
    params["page"           ] = request.args.get('page'         )
    params["entry"          ] = request.args.get('entry'        )
    params["sort_by"        ] = request.args.get('sort_by'      )

    params["start_date"     ] = request.args.get('start_date'   )
    params["end_date"       ] = request.args.get('end_date'     )
    

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_TEST_PROSES"
    })

    response = view_register_test.view_register_test(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html        = html_unescape.unescape( html )
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : "/register_test"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/register_test/register_test_add_form")
def view_register_test_add_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                           = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    params["redirect"       ] = request.args.get('redirect'     )

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_REGISTER_TEST_TAMBAH_FORM"
    })
    
    response = view_register_test_add.view_register_test_add(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : params["redirect"]
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/register_test/add", methods=["POST"])
def proc_register_test_add():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    #tandai
    files                 = request.files
    params                = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id" ] = session.get("fk_user_id")
    params["files"      ] = files
    app.logger.debug(files)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_register_test_ADD"
    })


    response   = register_test_proc.register_test_proc(app)._add(params)

    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect(params["redirect"])
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : params["redirect"]
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

##########################################################
# MANAGER MEETING - Register Meeting
##########################################################
@app.route("/register_meeting")
def view_register_meeting_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                    = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    params["order_by"       ] = request.args.get('order_by'     )
    params["keyword"        ] = request.args.get('keyword'      )
    params["page"           ] = request.args.get('page'         )
    params["entry"          ] = request.args.get('entry'        )
    params["sort_by"        ] = request.args.get('sort_by'      )

    params["start_date"     ] = request.args.get('start_date'   )
    params["end_date"       ] = request.args.get('end_date'     )
    

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_meeting_PROSES"
    })

    response = view_register_meeting.view_register_meeting(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html        = html_unescape.unescape( html )
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : "/register_meeting"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/register_meeting/register_meeting_add_form")
def view_register_meeting_add_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                    = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    params["redirect"       ] = request.args.get('redirect'     )

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_REGISTER_meeting_TAMBAH_FORM"
    })
    
    response = view_register_meeting_add.view_register_meeting_add(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : params["redirect"]
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/register_meeting/add", methods=["POST"])
def proc_register_meeting_add():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    #tandai
    files                 = request.files
    params                = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id" ] = session.get("fk_user_id")
    params["files"      ] = files
    app.logger.debug(files)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "PROC_register_meeting_ADD"
    })


    response   = register_meeting_proc.register_meeting_proc(app)._add(params)

    m_action   = response.get("status"  )
    m_title    = response.get("status"  )
    m_desc     = response.get("desc"    )
    m_data     = response.get("data"    )

    if m_title != "" or m_desc != "":
        flash(m_title,"title")
        flash(m_desc,"desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect(params["redirect"])
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : params["redirect"]
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

##########################################################
# LEVEL CLASS LIST
##########################################################


@app.route("/configuration/level_class")
def view_level_class_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"         ] = session.get("fk_user_id"                )
    params["role_position"      ] = session.get("role_position"             )
    params["username"           ] = session.get("username"                  )
    params["order_by"           ] = request.args.get('order_by'             )
    params["keyword"            ] = request.args.get('keyword'              )
    params["page"               ] = request.args.get('page'                 )
    params["entry"              ] = request.args.get('entry'                )
    params["sort_by"            ] = request.args.get('sort_by'              )


    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id": params["fk_user_id"],
        "route_name": "VIEW_TERMS_AND_CONDITIONS_AKTIF"
    })

    response = view_level_class.view_level_class(app).html(params)
    response_data = response.get("data")

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html_resp   = make_response(html)
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action": response.get("status"),
            "message_desc": response.get("desc"),
            "message_data": response_data["error_message"],
            "redirect": "/user/config"
        }
        return redirect(url_for("view_error_page_html", data=err_message))
# end def

@app.route("/configuration/level_class/add", methods=["POST"])
def proc_level_class_add():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id" ] = session.get("fk_user_id")

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id": params["fk_user_id"],
        "route_name": "PROC_LEVEL_CLASS_ADD"
    })

    response = level_class_proc.level_class_proc(app)._add(params)

    m_action    = response.get("status")
    m_title     = response.get("status")
    m_desc      = response.get("desc")
    m_data      = response.get("data")

    if m_title != "" or m_desc != "":
        flash(m_title, "title")
        flash(m_desc, "desc")
    #end if

    if "SUCCESS" in m_action:
        return redirect(url_for("view_level_class_html"))
    else:
        err_message = {
            "message_action"    : m_action,
            "message_desc"      : m_desc,
            "message_data"      : m_data["error_message"],
            "redirect"          : "/configuration/terms_and_conditions"
        }
        return redirect(url_for("view_error_page_html", data=err_message))
# end def

##########################################################
# MANAGER USER - tutor approval
##########################################################
@app.route("/tutor_approval")
def view_tutor_approval_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    dashboard_return = role_precheck({"role_with_access":["ADMIN"]})
    if dashboard_return:
        return dashboard_return

    params                    = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["user_uuid"      ] = session.get("user_uuid"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    params["order_by"       ] = request.args.get('order_by'     )
    params["keyword"        ] = request.args.get('keyword'      )
    params["page"           ] = request.args.get('page'         )
    params["entry"          ] = request.args.get('entry'        )
    params["sort_by"        ] = request.args.get('sort_by'      )

    params["start_date"     ] = request.args.get('start_date'   )
    params["end_date"       ] = request.args.get('end_date'     )
    

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_meeting_PROSES"
    })

    response = view_tutor_approval.view_tutor_approval(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html        = html_unescape.unescape( html )
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : "/tutor_approval"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/setMeeting", methods=["POST"])
def set_meeting_approval():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return

    dashboard_return = role_precheck({"role_with_access":["ADMIN"]})
    if dashboard_return:
        return dashboard_return

    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id")

    logging_tm           = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : ""
    })

    landing_url = tutor_approval_proc.tutor_approval_proc(app).set_meeting( params )
    return redirect( landing_url )

@app.route("/approve_tutor/<uuid>")
def approval_tutor(uuid):
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    
    dashboard_return = role_precheck({"role_with_access":["ADMIN"]})
    if dashboard_return:
        return dashboard_return

    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"   ] = session.get("fk_user_id")
    params["user_uuid"   ] = uuid

    logging_tm           = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : ""
    })

    landing_url = tutor_approval_proc.tutor_approval_proc(app).approval_tutor( params )
    return redirect( landing_url )

##########################################################
# MANAGER PAYMENT - Payment Confirmation
##########################################################
@app.route("/payment_confirmation")
def view_payment_confirmation_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                           = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    params["order_by"       ] = request.args.get('order_by'     )
    params["keyword"        ] = request.args.get('keyword'      )
    params["page"           ] = request.args.get('page'         )
    params["entry"          ] = request.args.get('entry'        )
    params["sort_by"        ] = request.args.get('sort_by'      )

    params["start_date"     ] = request.args.get('start_date'   )
    params["end_date"       ] = request.args.get('end_date'     )
    

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_KONTEN_PROSES"
    })

    response = view_payment_confirmation.view_payment_confirmation(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html        = html_unescape.unescape( html )
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : "/payment_confirmation"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/approve_topup/<topup_request_id>")
def approval_topup(topup_request_id):
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    
    dashboard_return = role_precheck({"role_with_access":["ADMIN"]})
    if dashboard_return:
        return dashboard_return

    # end if

    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"   ] = session.get("fk_user_id")
    params["topup_request_id"  ] = topup_request_id

    logging_tm           = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : ""
    })

    landing_url = payment_confirmation_proc.payment_confirmation_proc(app).topup( params )
    return redirect( landing_url )



##########################################################
# PAYMENT - Topup
##########################################################
@app.route("/topup")
def view_topup_html():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if

    params                    = sanitize.clean_html_dic(request.form.to_dict())
    params["fk_user_id"     ] = session.get("fk_user_id"        )
    params["role_position"  ] = session.get("role_position"     )
    params["username"       ] = session.get("username"          )
    params["order_by"       ] = request.args.get('order_by'     )
    params["keyword"        ] = request.args.get('keyword'      )
    params["page"           ] = request.args.get('page'         )
    params["entry"          ] = request.args.get('entry'        )
    params["sort_by"        ] = request.args.get('sort_by'      )

    params["start_date"     ] = request.args.get('start_date'   )
    params["end_date"       ] = request.args.get('end_date'     )
    

    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id"  : params["fk_user_id"],
        "route_name"  : "VIEW_KONTEN_PROSES"
    })

    response = view_topup.view_topup(app).html( params )
    response_data  = response.get("data") 

    if "SUCCESS" in response.get("status"):
        html        = response_data["html"]
        html        = html_unescape.unescape( html )
        html_resp   = make_response( html )
        html_resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return html_resp
    else:
        err_message = {
            "message_action"    : response.get("status" ),
            "message_desc"      : response.get("desc"   ),
            "message_data"      : response_data["error_message"],
            "redirect"          : "/pengelolaan_konten/proses"
        }
        return redirect(url_for("view_error_page_html" , data=err_message ))
# end def

@app.route("/topup/submit", methods=["POST"])
def topup():
    redirect_return = login_precheck({})
    if redirect_return:
        return redirect_return
    # end if
    params               = sanitize.clean_html_dic(request.form.to_dict())
    params["email"]           = session.get("email")
    params["fk_user_id"     ] = session.get("fk_user_id")
    params["username"       ] = session.get("username")
    params["role_position"  ] = session.get("role_position")

    logging_tm           = int(time.time() * 1000)
    browser_resp = browser_security.browser_security(app).check_route({
        "fk_user_id" : params["fk_user_id"],
        "route_name" : ""
    })

    landing_url = topup_proc.topup_proc(app).topup_submit( params )

    flash("Your payment of "+params['amount']+" has been successfully processed. Please wait for confirmation.", "success")   
    return redirect( landing_url )
   
    # end if

