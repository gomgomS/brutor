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

from view import view_core_menu
from view import view_core_display
from view import view_core_header
from view import view_core_footer
from view import view_core_script
from view import view_core_css
from view import view_core_dialog_message

from collections import deque

class view_config_document_type:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self):
        pass
    # end def

    def show_menu_list(self, params):
        args            = params['args']
        value           = args["value"] if "value" in args else None
        data_list       = self.mgdDB.db_config_document_type.find({"fk_user_id" : params['fk_user_id']})
        doc_edit        = None
        form            = {}
        form['name']    = "Document_type"
        form['mode']    = "insert"
        if not value is None:
            doc_edit    = self.mgdDB.db_config_document_type.find_one({"value" : value})
            form["mode"]= "edit"
        response = {
            "config_data_list" : data_list,
            "edit_item_rec"    : doc_edit,
            "form"             : form,
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
        show_menu_data          = self.show_menu_list( params )
        config_data_list        = show_menu_data["config_data_list"] 
        edit_item_rec           = show_menu_data["edit_item_rec"  ]
        form                    = show_menu_data["form"           ]
        return render_template(
            "configuration/document_type.html",
            menu_list_html      = menu_list,
            config_data_list    = config_data_list,
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
# end class
