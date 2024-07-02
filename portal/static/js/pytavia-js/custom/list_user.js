$(document).ready(function(){
    $("#genpass").click(function(evt){
        GEN_PASS_OPS();		
    })
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
            $("#reset_password").val(message_data.password);
	}
}

show_user_detail = function( fk_user_id )
{
    AJAX_SERVER_call(
        show_user_detail_CALLBACK,
        "GET",
        "/api/user/get-item",
        { fk_user_id : fk_user_id },
        true
    );
};

show_user_detail_CALLBACK = function(msg_data)
{
    console.log( msg_data );

    var message_action = msg_data.message_action
    if ( message_action == "GET_USER_DETAIL_SUCCESS")
    {
		var user_detail = msg_data.message_data.user_detail;
		$("#fullname_id"   ).val( user_detail.fullname    ); //fullname
		$("#username_id"   ).val( user_detail.email       ); //username
		$("#group_id"	   ).val( user_detail.group       ); //role
		$("#status_id"	   ).val( user_detail.status      ); //status
    }
    
};

///////////////////////////////////////////////////////////////

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
///////////////////////////////////////////////////////////

view_note = function(inactive_note, lock_note)
{
    $("#lock_note").val(lock_note);
    $("#inactive_note").val(inactive_note);
}

active_add_username = function(user_id, username , activate)
{
	$("#activate_pkey_id").val(user_id);
	$("#activate_value_id").val(activate);
	$("#activate_username_id").val(username);
}

lock_add_username = function(user_id , username, lock_status)
{
        $("#lock_pkey_id").val(user_id);
        $("#lock_value_id").val(lock_status);
        $("#lock_username_id").val(username);
}

edit_add_username = function(user_id, username, full_name,  role)
{
        /* for edit tab */
        $("#edit_role_id").val(role);
        $("#edit_pkey_id").val(user_id);
        $("#edit_username_id").val(username);
        $("#edit_fullname_id").val(full_name);
        $("#select_role_update_id").val(role);

        /* for reset tab */        
        $("#reset_role_id").val(role);
        $("#reset_user_id").val(user_id);
        $("#reset_username").val(username);
}

delete_user = function(user_id)
{       
       $("#del_pkey_id").val(user_id);
}
