import sys
import traceback

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

class view_konten_tambah_form:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def

    def _find_posisi_banner(self, params):

        posisi_banner_list = []
        posisi_banner_view = self.mgdDB.db_config.find({ "is_deleted" : False, "config_type" : "POSISI_DI_APLIKASI" })
        for posisi_banner_item in posisi_banner_view:
            posisi_banner_list.append(posisi_banner_item)


        response = {
            "posisi_banner_list"   : posisi_banner_list
        }

        return response
    # end def

    def _find_jenis_tampilan(self, params):
        jenis_tampilan_list = []
        jenis_tampilan_view = self.mgdDB.db_config.find({ "is_deleted" : False, "config_type" : "JENIS_TAMPILAN" })
        for jenis_tampilan_item in jenis_tampilan_view:
            jenis_tampilan_list.append(jenis_tampilan_item)

        response = {
            "jenis_tampilan_list"   : jenis_tampilan_list
        }
        return response
    # end def


    def _find_perusahaan(self, params):
        perusahaan_list = []
        perusahaan_view = self.mgdDB.db_brutor_partner.find(
            {   
                "fk_tipe_perusahaan_value" : { "$ne" : "TENANTS" },
                "is_deleted" : False
            }
        )
        for perusahaan_item in perusahaan_view:
            perusahaan_list.append(perusahaan_item)

        response = {
            "perusahaan_list"   : perusahaan_list
        }
        return response
    # end def

    
    def html(self, params):
        response = helper.response_msg(
            "FIND_KONTEN_TAMBAH_FORM_SUCCESS", "FIND KONTEN TAMBAH FORM SUCCESS", {} , "0000"
        )
        try:
            menu_list_html         = view_core_menu.view_core_menu().html(params)
            core_display           = view_core_display.view_core_display().html(params)
            params["core_display"] = core_display         
            core_header            = view_core_header.view_core_header().html(params)
            core_footer            = view_core_footer.view_core_footer().html(params)
            core_script            = view_core_script.view_core_script().html(params)
            core_css               = view_core_css.view_core_css().html(params)
            core_dialog_message    = view_core_dialog_message.view_core_dialog_message().html(params)


            # FIND POSISI BANNER
            posisi_banner_resp             = self._find_posisi_banner( params )
            posisi_banner_list             = posisi_banner_resp["posisi_banner_list"] 

            # FIND PERUSAHAAN
            perusahaan_resp             = self._find_perusahaan( params )
            perusahaan_list             = perusahaan_resp["perusahaan_list"         ] 

            # FIND JENIS TAMPILAN
            jenis_tampilan_resp             = self._find_jenis_tampilan( params )
            jenis_tampilan_list             = jenis_tampilan_resp["jenis_tampilan_list" ] 


            html = render_template(
                "pengelolaan_konten/konten_tambah_form.html",
                menu_list_html          = menu_list_html,
                core_display            = core_display,
                core_header             = core_header, 
                core_footer             = core_footer, 
                core_script             = core_script,  
                core_css                = core_css,
                core_dialog_message     = core_dialog_message,
                username                = params["username"      ],
                role_position           = params["role_position" ],
                redirect                = params["redirect"      ],
                posisi_banner_list      = posisi_banner_list,
                perusahaan_list         = perusahaan_list,
                jenis_tampilan_list     = jenis_tampilan_list
            )

            response.put( "data", {
                    "html" : html
                }
            )


        except:
            trace_back_msg = traceback.format_exc() 
            print(trace_back_msg)
            self.webapp.logger.debug(trace_back_msg)
            response.put( "status"      , "FIND_KONTEN_TAMBAH_FORM_FAILED" )
            response.put( "desc"        , "FIND KONTEN TAMBAH FORM FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try

        return response
    # end def
    
# end class

