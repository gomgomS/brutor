$(document).ready(function() {
    $('#table-list-advertising').DataTable( {
        dom: 'Bfrtip',
        buttons: [
			'copy', 'csv', 'excel','pdf'
		]
    } );
} );
