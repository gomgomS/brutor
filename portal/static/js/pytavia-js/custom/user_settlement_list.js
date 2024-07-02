var g_curr_tid   = null;
var g_curr_batch = null

$(document).ready(
	function() 
	{

	}
);

set_settlement = function( trx_tid , batch )
{
	g_curr_tid   = trx_tid;
	g_curr_batch = batch;
};

exec_settlement = function()
{
	var date 	= $("#id_date"	     ).val()
	var merchant_id = $("#id_merchant_id").val()
	var terminal_id = $("#id_terminal_id").val()
	var batch_no_id = $("#id_batch_no_id").val()
	var search_id   = $("#id_search_id"  ).val()
	window.location = "/process/settlement/update?" + 
		"trx_tid="      + g_curr_tid   + 
		"&batch_no="    + g_curr_batch +
		"&date="        + date	       + 
		"&merchant_id=" + merchant_id  +
		"&terminal_id=" + terminal_id  +
		"&batch_no_id=" + batch_no_id  +
		"&search=" 	+ search_id    
};
