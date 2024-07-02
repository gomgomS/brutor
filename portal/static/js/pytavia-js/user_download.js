$(document).ready(function() {
    $('#table-list-download').DataTable( {
        dom: 'Bfrtip',
        buttons: [
			'copy', 'csv', 'excel','pdf'
		]
    } );
} );