var cms_scoring_list = [];
var final_cms_scoring_list = [];
var g_cms_scoring = {};
var bool_ops;
var groups    = $("#group-name").val();
var rule_id   = $("#rule-id").val();

 $('#add_rules').on("click", function(e) {
	var category   = $("#category").val();
	var fields     = $("#fields").val();
	var operator   = $("#operator").val();
	var vals       = $("#vals").val();
	var data_type  = $("#data_type").val();
	bool_ops   	   = $("#bool_ops").val();

	g_cms_scoring = {
		"rule_id"  	    : rule_id,
		"category"  	: category,
		"attribute" 	: fields,
		"group_name"	: groups,
		"operator"  	: operator,
		"value"     	: vals,
		"data_type" 	: data_type,
		"logic_operator": bool_ops,
	}
    var field_list = Object.values(g_cms_scoring);
    for ( var i = 0; i < field_list.length; i++)
    {
        var field_item = field_list[i];
        if (field_item == "__" || field_item == "")
        {
            $("#dialog_message").modal("toggle");
            var error_dialog ="Field " +Object.keys(g_cms_scoring)[i]+ " belum diisi"
            $("#msg_desc").text(error_dialog);
            return $("#msg_desc").text(error_dialog);
        }
    }

    if (data_type == "number")
    {
        if (operator != "in")
        {
            vals = parseFloat(vals);
            if (number_validation(vals) != true)
            {
                $("#dialog_message").modal("toggle");
                var error_dialog = "Type data yang Anda masukkan tidak sesuai!"
                $("#msg_desc").text(error_dialog);
                return $("#msg_desc").text(error_dialog);
            }
        }
    }

	fn_add_rules(g_cms_scoring);

 })

 number_validation = function(n)
 {
    if (Number.isInteger(n) == true)
    {
        return true
    }
    if (isFloat_number(n) == true)
    {
        return true
    }
 }

function isFloat_number(v) {
    var num = /^[-+]?[0-9]+\.[0-9]+$/;
    return num.test(v);
}

$('#category').on("change", function(e) {
    var selected_category = $(this).val();
    fn_get_attributes({
        "category" : selected_category
    });
});

  fn_generate_table = function()
  {
	  $("#table_list").html("");
	  var row_tmpl = $("#row_table_list").html();
	  for (var i = 0; i < cms_scoring_list.length;i++)
	  {
		  item = cms_scoring_list[i];
          var rule_key = "'"+'del_'+item.pkey+"'";
          var order   = '<input type="number" value="'+item.order+'" data-key="'+item.pkey+'" class="order_id form-control" style="width:60px;"/>';
          var remove_btn = '<button type="button" class="btn btn-danger" style="width:80px;" onclick="fn_remove_rule('+rule_key+')"><i class="fa fa-trash position-left"></i>Delete</button>';
		  row = row_tmpl.replace(
		  "__category__",item.category
		  ).replace(
		  "__fields__",item.attribute
		  ).replace(
		  "__operator__",item.operator
		  ).replace(
		  "__vals__",item.value
		  ).replace(
	  	  "__data_type__",item.data_type
	  	  ).replace(
		  "__bool_ops__",item.logic_operator
		  ).replace(
		  "__rmv_btn__",remove_btn
		  ).replace(
		  "__order__",order
		  )
		  var display_tmpl = $("#table_list").append(row)

	  }
  }

$('.btn-update-list').on("click", function(e) {
    var ordering_list = [];
    $.each($(".order_id"), function() {
        var order_key   = $(this).attr("data-key");
        var order_value = $(this).val();
        ordering_data = {
            "order_key" : order_key,
            "order_val" : order_value
        }
        ordering_list.push(ordering_data);
    });
    fn_ordering_rules_update(ordering_list);
});


 $(document).ready(function(){
    console.log(groups,"liat konsol");
 	if (groups != "")
 	{
        $("#logic_operator").val(bool_ops);
 		$("#group-title").text(groups);
        $(".scoring-rules-row").css("display","block");
		fn_get_all_rules();
 	}
 });

 fn_get_all_rules = function()
 {
	 http_params = {
         "rule_id":rule_id
     }
     AJAX_SERVER_call(
             fn_get_all_rules_CALLBACK,
             "GET",
             "/api/get/scoring/rules/data",
             http_params,
             true
     );
 }

 fn_get_all_rules_CALLBACK = function(msg_data)
 {
     var message_action = msg_data.message_action;
     var message_data   = msg_data.message_data;
     if (message_action == "GET_SCORING_RULE_SUCCESS")
     {
        for (var i = 0; message_data.length > i; i++)
        {
            var scoring_data = message_data[i];
            if(scoring_data.logic_operator == "done")
            {
                $(".final-display-bottom").css("display","block");
            }
            cms_scoring_list.push(scoring_data);
        }
        fn_generate_table();
     }
 }

 // AJAX CALL
 fn_ordering_rules_update = function(ordering_list)
 {
     var http_params = { "ordering_list" : ordering_list }
     AJAX_SERVER_call_POST(
             fn_ordering_rules_update_CALLBACK,
             "POST",
             "/api/scoring/ordering/rules/update",
             http_params,
             true
     );
 }

fn_ordering_rules_update_CALLBACK = function(msg_data)
{
    var message_action = msg_data.message_action;
    var message_data   = msg_data.message_data;
    if (message_action == "UPDATE_SCORING_RULE_LIST_SUCCESS")
    {
        cms_scoring_list = [];
        fn_get_all_rules();
    }
}


 fn_get_attributes = function(http_params)
 {
     AJAX_SERVER_call_POST(
             fn_get_attributes_CALLBACK,
             "POST",
             "/api/scoring/get/attributes",
             http_params,
             true
     );
 }

fn_get_attributes_CALLBACK = function(msg_data)
{
    var message_action = msg_data.message_action;
    var message_data   = msg_data.message_data;
    if (message_action == "GET_SCORING_ATTR_SUCCESS")
    {
        $("#fields").html("<option value='__'>Attribute</option>")
        for (var i=0; i < message_data.length; i++)
        {
            var attr_item    = message_data[i];
            var attr_option  = '<option value="'+attr_item.value+'">'+attr_item.name+'</option>';
            var tmpl_fields_attr = $("#fields").append(attr_option);
        }
    }
}

 fn_add_rules = function(http_params)
 {
     AJAX_SERVER_call_POST(
             fn_add_rules_CALLBACK,
             "POST",
             "/api/scoring/rules/add",
             http_params,
             true
     );
 }

fn_add_rules_CALLBACK = function(msg_data)
{
	var message_action = msg_data.message_action;
	if (message_action == "ADD_SCORING_RULE_SUCCESS")
	{
        cms_scoring_list = [];
        return fn_get_all_rules();
	}
    if (message_action == "ERROR_DATA_TYPE")
    {
        $("#dialog_message").modal("toggle");
        var error_dialog = "Type data yang Anda masukkan tidak sesuai!"
        return $("#msg_desc").text(error_dialog);
    }
}

fn_remove_rule = function(rule_key)
{
    http_params = {"rule_key": rule_key}
    AJAX_SERVER_call_POST(
            fn_remove_rule_CALLBACK,
            "POST",
            "/api/scoring/rules/remove",
            http_params,
            true
    );
}

fn_remove_rule_CALLBACK = function(msg_data)
{
   var message_action = msg_data.message_action;
   if (message_action == "REMOVE_SCORING_RULE_SUCCESS")
   {
       cms_scoring_list = [];
       fn_get_all_rules();
   }
}


fn_update_ordering_rules = function(http_params)
{
    AJAX_SERVER_call_POST(
            fn_update_ordering_rules_CALLBACK,
            "POST",
            "/api/scoring/rules/add",
            http_params,
            true
    );
}

fn_update_ordering_rules_CALLBACK = function(msg_data)
{
   cms_scoring_list = [];
   var message_action = msg_data.message_action;
   if (message_action == "ADD_SCORING_RULE_SUCCESS")
   {
       fn_get_all_rules();
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

 AJAX_SERVER_call=function(callback_func,method,wservice,uri,bool)
	{_g_jqxhr=$.ajax({url:wservice,method:method,data:uri,dataType:"json"}).done(function(msg_json)
	{callback_func(msg_json);}).fail(function(msg_json)
	{callback_func(msg_json);}).always(function()
	{});};
