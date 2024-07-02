var cms_scoring_list = [];
var final_cms_scoring_list = [];
var g_cms_scoring = {};
var bool_ops;
var groups    = $("#group-name").val();
var group_key = $("#group-key").val();

 $('#add_rules').on("click", function(e) {
	var category   = $("#category").val();
	var fields     = $("#fields").val();
	var operator   = $("#operator").val();
	var vals       = $("#vals").val();
	var data_type  = $("#data_type").val();
	bool_ops   	   = $("#bool_ops").val();

	g_cms_scoring = {
		"group_key"  	: group_key,
		"category"  	: category,
		"attribute" 	: fields,
		"group_name"	: groups,
		"operator"  	: operator,
		"value"     	: vals,
		"data_type" 	: data_type,
		"logic_operator": bool_ops,
	}
	fn_add_rules(g_cms_scoring);

 })

  fn_generate_table = function(bools_ops)
  {
	  $("#table_list").html("");
	  var row_tmpl = $("#row_table_list").html();
  console.log(bools_ops);
  if (bools_ops == "done")
   {
	var input_score	    = "<label>Score: </label><input type='text' id='rules_score'/>";
	var submit_btn_html = "<button type='button' id='submit_group'>Submit</button>";
	var wraping_submit_scoring = input_score + " " + submit_btn_html;
	$("#submit_scoring").html(wraping_submit_scoring)
	fn_ready_to_send();

   }
	  for (var i = 0; i < cms_scoring_list.length;i++)
	  {
		  item = cms_scoring_list[i];
		  console.log(item,"s_data");

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
		  )
		  var display_tmpl = $("#table_list").append(row)

	  }
  }

fn_ready_to_send = function()
{
	$('#submit_group').on("click", function(e) {
	console.log(cms_scoring_list);
	$("#view_cms_scoring").html(JSON.stringify(cms_scoring_list));
	fn_jaitan();
	});

}

fn_jaitan = function()
{
	var string_bucket = "";
	var anu = "";
	var anunya = "";
	var points = $("#rules_score").val();
		for (var i = 0; i < cms_scoring_list.length; i++)
		{
			item = cms_scoring_list[i];
			string_bucket = item.category +" "+ item.fields +" "+ item.operator +" "+ item.vals +" "+ item.bool_ops + " "
			anu += string_bucket;
		}
		anunya = groups +" "+ anu +" "+ points
		console.log(anunya);

		final_data = {
			"groups" : groups,
			"points" : points,
			"rules_list" : cms_scoring_list,
			"rules_str" : anunya
		}
		final_cms_scoring_list.push(final_data)
		console.log(final_cms_scoring_list);
}

$('.btn-add-group').on("click", function(e) {
	groups = $("#add-group").val();
	console.log(groups);
	$("#group-title").text(groups);
	$(".scoring-rules-row").css("display","block");
 })

 $(document).ready(function(){
	 console.log(groups,"liat konsol");
 	if (groups != "")
 	{
 		$("#group-title").text(groups);
		fn_get_all_rules();
 		console.log(groups);
 	}
 });

 fn_get_all_rules = function(http_params)
 {
	 http_params = {"group_key":group_key}
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
        console.log(msg_data,"hello world");
        for (var i = 0; message_data.length > i; i++)
        {
            var scoring_data = message_data[i];
            console.log(scoring_data,"g_cms_scoring");
            cms_scoring_list.push(scoring_data);
        }
        fn_generate_table(bool_ops);
        console.log(cms_scoring_list,"cms_scoring_list");
     }
 }

 // AJAX CALL - POST
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
	console.log(msg_data);
    cms_scoring_list = [];
	var message_action = msg_data.message_action;
	if (message_action == "ADD_SCORING_RULE_SUCCESS")
	{
        console.log(g_cms_scoring,"g_cms_scoring");
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
