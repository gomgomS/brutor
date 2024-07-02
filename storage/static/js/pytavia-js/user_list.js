$(document).ready(function() {
    $('#table-employee-management').DataTable( {
        dom: 'Bfrtip',
        buttons: [
			'copy', 'csv', 'excel','pdf'
		]
    } );
} );
