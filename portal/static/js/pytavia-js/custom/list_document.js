var g_remove_link = ""

$(document).ready(
	function()
	{
		$("#delete-confirm-button").click(
			function()
			{
				delete_document_upload();
			}
		)
	}
);

//
// Delete the document upload
//
delete_document_upload = function()
{
	window.location = g_remove_link;
};

//
// Set the document to delete
//
set_delete_document_upload = function(pkey)
{
	g_remove_link = "/process/admin/document/remove?pkey=" + pkey;
}
