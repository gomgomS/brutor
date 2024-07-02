$(document).ready(function () {
    ownershipStatus = $('#ownershipStatus').val()
    console.log(ownershipStatus)
    if( ownershipStatus == 'OWN'){
        $("#psnSheetOwned").prop("checked", true);
    }
    else{
        $("#psnSheetTc").prop("checked", true);
    }
});


