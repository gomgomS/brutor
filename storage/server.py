import json
import time
import pymongo
import sys
import base64
import gridfs
import os

sys.path.append("pytavia_core"    ) 
sys.path.append("pytavia_settings") 
sys.path.append("pytavia_stdlib"  ) 
sys.path.append("pytavia_storage" ) 
sys.path.append("pytavia_modules" ) 
sys.path.append("pytavia_modules/view"          ) 
sys.path.append("pytavia_modules/configuration" ) 
sys.path.append("pytavia_modules/security"      ) 
sys.path.append("pytavia_modules/auth"          ) 
sys.path.append("pytavia_modules/bucket"        ) 
sys.path.append("pytavia_modules/directory"     ) 

from configuration   import cfs_put_file
from configuration   import cfs_convert_file
from configuration   import cfs_get_file

from security        import security_proc
from security        import security_gateway

from auth            import auth_register
from auth            import auth_login

from bucket          import bucket_proc
from directory       import directory_proc

from pytavia_core    import database 
from pytavia_core    import config 
from pytavia_stdlib  import idgen 

####################################
from view            import chk_server
from view            import view_bucket_level
from view            import view_directory_level

from flask           import request
from flask           import render_template
from flask           import Flask
from flask           import session
from flask           import make_response
from flask           import redirect
from flask           import url_for
from flask           import stream_with_context
from flask           import Response

from flask           import Flask
from flask_wtf.csrf  import CSRFProtect
#from flask_wtf.csrf import CSRFError

#
# Main app configurations
#
app                   = Flask( __name__, config.G_STATIC_URL_PATH )

app.secret_key        = config.G_FLASK_SECRET

@app.route('/')
def hello():
    return redirect(url_for('user_login'))
# end def

@app.route("/login", methods=["GET"])
def user_login():
    return render_template( "login.html" )
# end def

@app.route("/register", methods=["GET"])
def user_register():
    username = request.args.get('username')
    password = request.args.get('password')
    response = auth_register.auth_register(app).register({
        "username" : username,
        "password" : password
    })
    return json.dumps( response ) 
# end def

@app.route("/console/bucket", methods=["GET"])
def console_root():
    html = view_bucket_level.view_bucket_level(app).html({})
    return html
# end def

@app.route("/console/directory", methods=["GET"])
def console_directory():
    node_id = request.args.get('pnode_id')
    html    = view_directory_level.view_directory_level(app).html({
        "pnode_id" : node_id 
    })
    return html
# end def

####################### UI PROCESS API's BELOW ##################################

@app.route("/v1/process/cfs/api_create_bucket", methods=["POST"])
def create_bucket():
    params   = request.form.to_dict()
    response = bucket_proc.bucket_proc(app).create( params )
    m_action = response["message_action"]
    if m_action == "CREATE_BUCKET_SUCCESS":
        return redirect(url_for("console_root"))
    else:
        return redirect("/login")
    # end if
# end def

@app.route("/v1/process/cfs/api_create_directory", methods=["POST"])
def create_directory():
    params   = request.form.to_dict()
    response = directory_proc.directory_proc(app).create( params )
    m_action = response["message_action"]
    if m_action == "CREATE_DIRECTORY_SUCCESS":
        parent_node_id = response["message_data"]["parent_node_id"]
        return redirect("/console/directory?pnode_id=" + parent_node_id)
    else:
        return redirect("/login")
    # end if
# end def

################################## API's BELOW ##################################

@app.route("/auth/login", methods=["POST"])
def proc_auth_login():
    params   = request.form.to_dict()
    response = auth_login.auth_login(app).login( params )
    m_action = response["message_action"]
    if m_action == "LOGIN_SUCCESS":
        return redirect(url_for("console_root"))
    else:
        return redirect("/login")
    # end if
# end def

"""
    Will get the security token before calling any of the other
    API's
"""
@app.route("/v1/cfs/security/login", methods=["POST"])
def security_login():
    params   = request.form.to_dict()
    response = security_proc.security_proc(app).login( params )
    return json.dumps(response )
# end def

"""
    Will get the security token before calling any of the other
    API's
"""
@app.route("/v1/cfs/security/request_security_token", methods=["POST"])
def security_token():
    params   = request.form.to_dict()
    response = security_proc.security_proc(app).request_security_token( params )
    return json.dumps( response )
# end def

"""
    This will be called periodically to check that 
    the connection is still there
    - DONE
"""
@app.route("/v1/cfs/connection", methods=["POST"])
def get_connection():
    params   = request.form.to_dict()
    response = connection.connection(app).get( params )
    return json.dumps( response )
# end def

@app.route("/v1/cfs/put", methods=["POST"])
def api_put_large_file():
    upload_stream = request.stream
    upload_header = request.headers
    response      = cfs_put_file.cfs_put_file(app).put({
        "stream" : upload_stream,
        "header" : upload_header,
    })
    return json.dumps( response ) 
# end def

@app.route("/v1/cfs/get-file", methods=["GET","POST"])
def api_vi_cfs_get_file():    
    key     = request.args.get('key'   )
    bucket  = request.args.get('bucket')
    access  = request.args.get('access')
    mgdDB   = database.get_db_conn(config.mainDB)
    
    app.logger.debug("key = " + str(key) + ", bucket = " + str(bucket))

    if key == None and bucket == None :
        return None
    # endif


    cfs_rec = None
    if bucket != None:
        cfs_rec = mgdDB.db_blipcom_cfs.find_one({
            "$and" : [
                {"key"    : key    },
                {"bucket" : bucket }
            ]
        })
    else:
        cfs_rec = mgdDB.db_blipcom_cfs.find_one({
            "key" : key   
        })
    # end if
    download_fname = os.path.basename( key )
    content_type   = cfs_rec["content_type"] 
    def generate():
        mgdDB      = database.get_db_conn(config.mainDB)
        cfs_rec    = mgdDB.db_blipcom_cfs.find_one({
            "$and" : [{"key" : key }, {"bucket" : bucket }]
        })
        if cfs_rec  != None:
            handle_mgd_grid = gridfs.GridFS(mgdDB)
            file_mgd_grid   = handle_mgd_grid.get( cfs_rec["fk_file_id"] )
            raw             = file_mgd_grid.read(1024)
            file_name       = key
            while raw:
                yield raw
                raw = file_mgd_grid.read(1024)
            # end while
        # end if
    # end def
    app.logger.debug( content_type )
    file_response = Response(
        stream_with_context(generate()), mimetype=content_type
    )
    #
    # If access == SHOW or anything else for that matter 
    # we will not call this, if its empty we call this and 
    # we download the file as opposed to prop it on the browser
    # 
    if access == None:
        file_response.headers.set( 
            'Content-Disposition','attachment',filename=download_fname
        )
    # end if
    return file_response
# end def
#
#
