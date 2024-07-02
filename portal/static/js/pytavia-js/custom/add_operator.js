$(document).ready(function()
{
	$("#genpass").click(function(evt)
		{
			GEN_PASS_OPS();		
		}
	)
	$("#email_ops_username_id").focusout(
		function()
		{
			CHECK_USERNAME_PROC();
		}
	);
});

GEN_PASS_OPS = function() 
{	
	AJAX_SERVER_call(
		GEN_PASS_OPS_CALLBACK,
		"GET",
		"/user/gen_password",
		true
	);
}

GEN_PASS_OPS_CALLBACK = function(msg_data)
{
	var message_data =  msg_data.message_data;	
	if(message_data.password)
	{
		$("#password").val(message_data.password);
	}
}

CHECK_USERNAME_PROC = function()
{
	var username = $("#email_ops_username_id").val();
        AJAX_SERVER_call(
        	CHECK_USERNAME_PROC_CALLBACK,
                "GET",
                "/auth/username/check",
		{ username : username },
                true
        );
}

CHECK_USERNAME_PROC_CALLBACK = function(msg_data)
{
	console.log( msg_data );
	var message_action = msg_data.message_action;
	if ( message_action == "USERNAME_AVAILABILITY_SUCCESS" )
	{
		$("#submit_button_id").removeAttr("disabled","disabled");
	}
	else
	{
		var desc = msg_data.message_desc;
		$("#submit_button_id").attr("disabled","disabled");
		alert( desc );
	}
};

AJAX_SERVER_call = function(callback_func, method, wservice, uri, bool)
{
        _g_jqxhr = $.ajax(
        {
                url      : wservice ,
                method   : method   ,
                data     : uri      ,
                dataType : "json"
        }).done(
                function(msg_json)
                {
                        callback_func(msg_json);
                }
        ).fail(
                function(msg_json)
                {
                        callback_func(msg_json);
                }
        ).always(
                function()
                {
                }
        );
}
