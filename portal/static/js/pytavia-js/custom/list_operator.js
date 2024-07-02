$(document).ready(
	function()
	{
		$("#activate_button_id").click(
			function()
			{
			}
		)
	}
);

active_add_operator = function(user_id, username , activate)
{
	$("#activate_username").val( username );
	$("#activate_value_id").val( activate );
	$("#activate_pkey_id" ).val( user_id  );
}

lock_add_operator = function(user_id , username, lock_status)
{
        $("#lock_username").val( username    );
        $("#lock_value_id"   ).val( lock_status );
        $("#lock_pkey_id"    ).val( user_id     );
}

edit_add_operator = function(user_id,username,email,info,role)
{
        $("#username").val( username    );
        $("#email").val( email   );
        $("#info").val( info   );
        $("#role_id").val( role        );
        $("#pkey_id").val( user_id     );
}

view_note = function(note)
{
        $("#view_note").val( note    );
}

