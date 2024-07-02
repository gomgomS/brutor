/*
    For Bank Users
*/


flag_active_user = function( user_id, username , flag_activate, title_activate )
{

	$("#activate_modal_title").text(title_activate + " User");
	$("#activate_pkey_id").val(user_id);
	$("#activate_username_id").val(username);
	$("#activate_value_id").val(flag_activate);
	
}

del_user = function( user_id )
{
	$("#del_pkey_id").val(user_id);
}

//edit_user = function( user_id, name, username, role_value )
edituser = function( user_id, name, username, role_value )
{
	document.getElementById("form_add_user").style.display = "none";
	document.getElementById("form_edit_user").style.display = "block";				
	//$("#edit_fullname").focus();
    document.getElementById("edit_fullname").focus();
	//$("#edit_pkey_id").val(user_id);
	document.getElementById("edit_pkey_id").value = user_id;
	$("#edit_fullname").val(name);
	$("#edit_username").val(username);
	$("#edit_password").val("");
	$("#edit_role").select(role_value);
}
reset_field = function()
{
	$("#add_fullname").focus();	
	$("#add_fullname").val("");
	$("#add_username").val("");
	$("#add_password").val("");
	$("#add_role").select("");
}
cancel_edit = function()
{
	document.getElementById("form_add_user").style.display = "block";
	document.getElementById("form_edit_user").style.display = "none";
	$("#add_fullname").focus();
	$("#edit_pkey_id").val("");
	
}


/*
    For Sales Users
*/

// for Sales Person
active_sales_person = function(user_id, username , flag_activate, title_activate)
{
	$("#activate_modal_title").text(title_activate + " User");
	$("#activate_pkey_id").val(user_id);
	$("#activate_username_id").val(username);
	$("#activate_value_id").val(flag_activate);
}

delete_sales_user = function( user_id )
{
    $("#fk_sales_user_id").val(user_id);
}
