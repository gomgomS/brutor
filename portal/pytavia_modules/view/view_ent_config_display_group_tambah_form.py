import sys
import traceback
import pymongo

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

class view_ent_config_display_group_tambah_form :

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, params):
        pass
    # end def

    def _find_tipe_grouping(self) :
        tipe_list = [
            { "name" : "Carousel Banner"        , "value" : "carousel_banner"       , "desc" : "[800x460] Tampilan Banner (Gambar & Title)" },
            { "name" : "Carousel Banner Small"  , "value" : "carousel_banner_small" , "desc" : "[400x240] Tampilan Banner SMALL (Gambar & Title)"},           
            { "name" : "Carousel Detail"        , "value" : "carousel_detail"       , "desc" : "[800x460] Tampilan Banner (Gambar, Title, Deskripsi)"},
            { "name" : "Carousel Portrait"      , "value" : "carousel_portrait"     , "desc" : "[90x200] Tampilan Portrait" },
            { "name" : "Grid"                   , "value" : "grid"                  , "desc" : "[90x90]Tampilan Grid" },
            { "name" : "Carousel Bottom Banner" , "value" : "carousel_bottom_banner", "desc" : "Tampilan Bottom Banner" },


        ]
        return tipe_list
    # end def

    def _find_one_tipe_grouping(self, value) :
        tipe_list = self._find_tipe_grouping()
        result = { "name" : "", "value" : "", "desc" : "" }
        for each_tipe in tipe_list :
            if value == each_tipe["value"] :
                result = each_tipe
                break
        # endfor
        return result
    # end def

    def _find_display_group(self, params) :
        fk_menu_id  = params["fk_menu_id"]
        config_list = []
        config_view = self.mgdDB.db_ent_config_display_group.find({
            "fk_ent_menu_id" : fk_menu_id,
            "is_deleted" : False 
        }).sort("urutan", pymongo.ASCENDING)
        #config_list = list( config_view )
        for each_item in config_view :
            tipe_grouping = self._find_one_tipe_grouping(each_item["type"])
            each_item["tipe_grouping"] = tipe_grouping
            config_list.append( each_item )
        return config_list
    # end def

    def _find_one_menu(self, params) :
        fk_menu_id = params["fk_menu_id"]
        menu_rec = self.mgdDB.db_ent_config_menu.find_one({ "pkey" : fk_menu_id })
        return menu_rec
    # end def


    def html(self, params):
        response = helper.response_msg(
            "FIND_ENTERTAINMENT_CONFIG_DISPLAY_GROUP_FORM_SUCCESS", "FIND ENTERTAINMENT DISPLAY GROUP FORM SUCCESS", {} , "0000"
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

            # FIND CONFIG 
            config_list = self._find_display_group(params)
            menu_rec    = self._find_one_menu(params)
            tipe_list   = self._find_tipe_grouping()

            html = render_template(
                "entertainment/config_display_group_tambah_form.html",
                menu_list_html          = menu_list_html,
                core_display            = core_display,
                core_header             = core_header, 
                core_footer             = core_footer, 
                core_script             = core_script,  
                core_css                = core_css,
                core_dialog_message     = core_dialog_message,
                username                = params["username"      ],
                role_position           = params["role_position" ],
                tipe_list               = tipe_list,
                config_list             = config_list,
                menu_rec                = menu_rec
            )

            response.put( "data", {
                    "html" : html
                }
            )


        except:
            trace_back_msg = traceback.format_exc() 
            print(trace_back_msg)
            self.webapp.logger.debug(trace_back_msg)
            response.put( "status"      , "FIND_ENTERTAINMENT_CONFIG_DISPLAY_GROUP_FORM_FAILED" )
            response.put( "desc"        , "FIND ENTERTAINMENT CONFIG DISPLAY GROUP FORM FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try

        return response
    # end def
    
# end class

