$(document).ready(function() {
		$('#table-employee-management').DataTable( {
			dom: 'Bfrtip',
			buttons: [
				'copy', 'csv', 'excel','pdf'
			]
		} );

            //act_terminal()
});


act_terminal = function(pkey,status_val,status)
{
        //alert("test")
	$("#pkey").val( pkey );
	$("#status").val( status_val );
}
