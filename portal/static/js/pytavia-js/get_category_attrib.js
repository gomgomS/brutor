var selected_category = $("#category_select").val();
var edited_attrib_id  = $("#edited_attrib_id").val();

$(document).ready(function(){
    fn_scoring_category_attrib({"db_coll":selected_category})

    $("#table-achievement-status-list").DataTable();
    $('#category_select').on("change", function(e) {
         selected_category = $(this).val();
        if (selected_category != "__")
        {
            fn_scoring_category_attrib({
                "db_coll" : selected_category
            });
        }
        else {
             $("#filed_select").html("<option value='__'>Select Field</option>")
        }
    });
});




fn_scoring_category_attrib = function(http_params)
{
    AJAX_SERVER_call_POST(
            fn_scoring_category_attrib_CALLBACK,
            "POST",
            "/api/scoring/get/category/attrib",
            http_params,
            true
    );
}

fn_scoring_category_attrib_CALLBACK = function(msg_data)
{
   var message_action = msg_data.message_action;
   var message_data	  = msg_data.message_data;
   $("#filed_select_chosen").html("");
   if (message_action == "GET_SCORING_CATEGORY_ATTRIB_SUCCESS")
   {
       console.log(msg_data);
       $("#filed_select").html("<option value='__'>Select Field</option>")
        for (var i=0; i < message_data.length; i++)
        {
            var attr_item    = message_data[i];
            var attr_option  = '<option value="'+attr_item+'">'+attr_item+'</option>';
            if (edited_attrib_id == attr_item)
            {
                attr_option  = '<option value="'+attr_item+'" selected="selected">'+attr_item+'</option>';
            }
            var tmpl_fields_attr = $("#filed_select").append(attr_option);
        }
   }
}

AJAX_SERVER_call_POST = function(callback_func, method, url, data, bool){
  var csrf_token = $("#csrf_token").val() ;
 _g_jqxhr = $.ajax({
             url      : url,
             method   : method,
             data     : JSON.stringify(data),
             dataType : "json",
             contentType: "application/json; charset=utf-8",
             dataType: 'json',
             beforeSend: function(xhr, settings) {
                 if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                     xhr.setRequestHeader("X-CSRFToken", csrf_token);
                 }
             },
             success: function(response,request){
                 console.log("success ++++++++ ")
                 callback_func(response);
             },
             error: function(response){
                 console.log("error ++++++++ ")
                 callback_func(response);
             }

             });
     }
