$(document).ready(function() {
    $('#table-employee-management').DataTable( {
        dom: 'Bfrtip',
        buttons: [
			'copy', 'csv', 'excel','pdf'
		]
    } );
} );

// date
$('.tgl_awal').datepicker({
	format: 'mm/dd/yyyy',
	startDate: '-3d'
});	
$('.tgl_akhir').datepicker({
	format: 'mm/dd/yyyy',
	startDate: '-3d'
});		
// end date
$('#modal-mpos-bca').on('shown.bs.modal', function () {
  $('#myInput').focus()
})

$('#modal-mpos-bca-edit').on('shown.bs.modal', function () {
  $('#myInput').focus()
})

$('#modal-mpos-bca-inactive').on('shown.bs.modal', function () {
  $('#myInput').focus()
})

$('#modal-mpos-bca-active').on('shown.bs.modal', function () {
  $('#myInput').focus()
})

$('#modal-mpos-bca-lock').on('shown.bs.modal', function () {
  $('#myInput').focus()
})

$('#modal-mpos-bca-unlock').on('shown.bs.modal', function () {
  $('#myInput').focus()
})

$('#modal-mpos-bca-force-logout').on('shown.bs.modal', function () {
  $('#myInput').focus()
})
