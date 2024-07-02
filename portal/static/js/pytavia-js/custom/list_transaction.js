$(document).ready(
	function()
	{
	}
);

view_receipt = function(receiptPath){  
    //console.log(receiptPath);
    if(receiptPath){
        imgModal = "<img src='/user/get-receipt/transaction?"+receiptPath+"' class='img-responsive image-modal-transaction-report-view-receipt' />" ;        
        document.getElementById("modalBodyreceipt").innerHTML = imgModal ;
   }   
  
}

show_transaction_detail = function( private_key )
{
    AJAX_SERVER_call(
        show_transaction_detail_CALLBACK,
        "GET",
        "/api/transaction/get-item",
        { trans_id : private_key },
        true
    );
};

show_transaction_detail_CALLBACK = function(msg_data)
{
    var message_action = msg_data.message_action
    if ( message_action == "GET_TRANS_ITEM_SUCCESS")
    {
        var trans_rec = msg_data.message_data.trans_rec;
	$("#date_transaction_id" ).val(trans_rec.str_date_transaction_icmp);
	$("#invoice_no_id"	 ).val(trans_rec.ref_no        );
	$("#terminal_id"  	 ).val(trans_rec.trx_tid       );
	$("#amount1_id"   	 ).val(trans_rec.amount1       );
	$("#merchant_id"	 ).val(trans_rec.mid	       );
	$("#batch_no_id"	 ).val(trans_rec.batch	       );
	$("#card_number_id"	 ).val(trans_rec.card_number   );
	$("#card_type_id"	 ).val(trans_rec.card_type     );
	$("#merchant_type_id"	 ).val(trans_rec.merchant_type );
	$("#transaction_type_id" ).val(trans_rec.trans_type    );
	$("#serial_number_id"    ).val(trans_rec.serial_number );
	$("#approval_code_id"    ).val(trans_rec.approval_code );
	$("#settlement_status_id").val(trans_rec.settle_status );
	$("#email_id"   	 ).val(trans_rec.email         );
    }
}

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
