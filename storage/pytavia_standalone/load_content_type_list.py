import sys
import traceback

sys.path.append("../"                )
sys.path.append("../pytavia_core"    )
sys.path.append("../pytavia_modules" )
sys.path.append("../pytavia_settings")
sys.path.append("../pytavia_stdlib"  )
sys.path.append("../pytavia_storage" )

from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config

class load_content_type_list:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self):
        pass
    # end def

    def proc_content_type(self, params):
        call_id  = idgen._get_api_call_id()
        response = {
            "message_id"     : call_id,
            "message_action" : "LOAD_CONTENT_TYPE_SUCCESS",
            "message_code"   : "0",
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            mime_types = dict(
                txt='text/plain',
                htm='text/html',
                html='text/html',
                php='text/html',
                css='text/css',
                js='application/javascript',
                json='application/json',
                xml='application/xml',
                swf='application/x-shockwave-flash',
                flv='video/x-flv',

                # images
                png='image/png',
                jpe='image/jpeg',
                jpeg='image/jpeg',
                jpg='image/jpeg',
                gif='image/gif',
                bmp='image/bmp',
                ico='image/vnd.microsoft.icon',
                tiff='image/tiff',
                tif='image/tiff',
                svg='image/svg+xml',
                svgz='image/svg+xml',

                # archives
                zip='application/zip',
                rar='application/x-rar-compressed',
                exe='application/x-msdownload',
                msi='application/x-msdownload',
                cab='application/vnd.ms-cab-compressed',

                # audio/video
                mp3='audio/mpeg',
                ogg='audio/ogg',
                qt='video/quicktime',
                mov='video/quicktime',

                # adobe
                pdf='application/pdf',
                psd='image/vnd.adobe.photoshop',
                ai='application/postscript',
                eps='application/postscript',
                ps='application/postscript',

                # ms office
                doc='application/msword',
                docx='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                dotx='application/application/vnd.openxmlformats-officedocument.wordprocessingml.template',
                rtf='application/rtf',
                xls='application/vnd.ms-excel',
                xltx='application/vnd.openxmlformats-officedocument.spreadsheetml.template',
                xlsx='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                ppt='application/vnd.ms-powerpoint',
                pptx='application/vnd.openxmlformats-officedocument.presentationml.presentation',
                sldx='application/vnd.openxmlformats-officedocument.presentationml.slide',
                csv='text/csv',

                # open office
                odt='application/vnd.oasis.opendocument.text',
                ods='application/vnd.oasis.opendocument.spreadsheet',
            )
            for key  in  mime_types :
                key = key
                value = mime_types[key]                
                conType = database.get_record("db_content_type")
                conType["key"] = key
                conType["content_type"] = value
                conType_rec =  self.mgdDB.db_content_type.find_one({
                    "$and" : [
                            {"key" : key},
                            {"value" : value}
                    ]
                })                
                if conType_rec == None :
                    #print(conType) 
                    self.mgdDB.db_content_type.insert( conType )
                #end if 
            #end for 
        except:
            print (traceback.format_exc())
            response["message_action"] = "LOAD_CONTENT_TYPE_FAILED"
            response["message_action"] = "LOAD_CONTENT_TYPE_FAILED: " + str(sys.exc_info())
        # end try
        return response
    # end def


contentType = load_content_type_list()
contentType.proc_content_type({})

