$(document).ready(
	function()
	{
		$("#activate_button_id").click(
			function(){}
		)
	}
);

view_receipt = function(receiptPath)
{  
    //console.log(receiptPath);
    if(receiptPath){
        imgModal = "<img src='/user/get-receipt/transaction?"+receiptPath+"' class='img-responsive image-modal-transaction-report-view-receipt' />" ;        
        document.getElementById("modalBodyreceipt").innerHTML = imgModal ;
   }   
  
}
active_add_username = function(user_id, username , activate)
{        
	$("#act_merchantusername_id" ).val( username );
	$("#activate_value_id"       ).val( activate );
	$("#activate_pkey_id"	     ).val( user_id  );
}

lock_add_username = function(user_id , username, lock_status)
{
        $("#lock_merchantusername_id ").val( username    );
        $("#lock_value_id"            ).val( lock_status );
        $("#lock_pkey_id"             ).val( user_id     );
}

force_logout_username = function(user_id , username, lock_status)
{
        $("#logout_merchantusername_id " ).val( username    );
        $("#logout_value_id"             ).val( lock_status );
        $("#logout_pkey_id"              ).val( user_id     );
}

edit_add_username = function(user_id, username, full_name,  role)
{
        $("#edit_username_id" ).val( username    );
        $("#edit_fullname_id" ).val( full_name   );
        $("#edit_role_id"     ).val( role        );
        $("#edit_pkey_id"     ).val( user_id     );
}