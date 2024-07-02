var cms_scoring_list = [];
var final_cms_scoring_list = [];
var g_cms_scoring = {};
var rule_id   = $("#rule-id").val();
var fields    = $("#fields").val();
var attrib_name  = $("#group-id").val();

 $('#add_rules').on("click", function(e) {
	var category    = $("#category").val();
	var fields      = $("#fields").val();
	var operator_a  = $("#operator_a").val();
    var operator_b  = $("#operator_b").val();
    var input_value = $("#input_value").val();
    var field_type  = $("#field_type").val();

	g_cms_scoring = {
		"rule_id"  	    : rule_id,
		"attrib_name"  	: attrib_name,
        "field_type"    : field_type,
        "input_value"   : input_value,
        "category"  	: category,
		"attribute" 	: fields,
		"operator_a"  	: operator_a,
		"operator_b"    : operator_b,
	}
    console.log(g_cms_scoring);
	fn_add_rules(g_cms_scoring);

 })


$('#category').on("change", function(e) {
    var selected_category = $(this).val();
    fn_get_attributes({
        "category" : selected_category
    });
});

$('#field_type').on("change", function(e) {
    var selected_cattribute_type = $(this).val();
    if (selected_cattribute_type == "_custom_field_")
    {
        $("#category_section").css("display","none");
        $("#attribute_section").css("display","none");
        $("#value_section").css("display","block");
        $("#fields").val("");
        $("#category").val("");
    }
    else
    {
        $("#category_section").css("display","block");
        $("#attribute_section").css("display","block");
        $("#value_section").css("display","none");
        $("#input_value").val("");
        
    }
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
          "__value__",item.value
          ).replace(
		  "__operator_a__",item.math_operator_a
		  ).replace(
		  "__operator_b__",item.math_operator_b
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
    console.log(rule_id,"liat konsol");
 	if (rule_id != "")
 	{

 		$("#group-title").text(attrib_name);
		fn_get_all_rules();
 	}
 });

 $('.btn-add-arthmetic').on("click", function(e) {
     $("#group-title").text(attrib_name);
     // $(".scoring-rules-row").css("display","block");
 });

  $('#g_name').keyup(function() {
      var v = $(this).val();
      attrib_name = v.toUpperCase().split(' ').join('_');
      $("#group-name").val(attrib_name);
      $("#group-title").text(attrib_name);
  });

 fn_get_all_rules = function()
 {
	 http_params = {
         "rule_id":rule_id
     }
     AJAX_SERVER_call(
             fn_get_all_rules_CALLBACK,
             "GET",
             "/api/get/scoring/arithmetic/rules/data",
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
        console.log(msg_data);
        for (var i = 0; message_data.length > i; i++)
        {
            var scoring_data = message_data[i];
            $(".final-display-bottom").css("display","block");
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
             "/api/scoring/arithmetic/ordering/rules/update",
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
             "/api/scoring/arithmetic/rule/add",
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
        fn_get_all_rules();
	}
}

fn_remove_rule = function(rule_key)
{
    http_params = {"rule_key": rule_key}
    AJAX_SERVER_call_POST(
            fn_remove_rule_CALLBACK,
            "POST",
            "/api/scoring/arithmetic/rules/remove",
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
