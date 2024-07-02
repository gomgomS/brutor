    fn_validate = function()
    {
       var documentId = $("#advDocument").val().replace(/\s/g, "");
       var notesId    = $("#Notes").val().replace(/\s/g, "");
       var selectId 	= $("#SelectId").val();

       if (documentId.length == 0){
         $("#err_file").show();
         return false
       }
       if (selectId == "NONE"){
         $("#err_status").show();
         return false
       }
       if (notesId.length == 0){
         $("#err_notes").show();
         return false
       }
    }

    fn_validates = function()
   {
     var notesId  = $("#Notes").val().replace(/\s/g, "");
     var selectId = $("#SelectId").val();

     if (selectId == "NONE"){
       $("#err_status").show();
       return false
     }
   }

    // Get the modal
    var modal = document.getElementById("imgModal");

    // Get the image and insert it inside the modal - use its "alt" text as a caption
    var modalImg          = document.getElementById("img01");
    var captionText       = document.getElementById("caption");
    var img_national      = document.getElementById("img_national_id");
    img_national.onclick  = function(){
    modal.style.display   = "block";
    modalImg.src          = this.src;
    captionText.innerHTML = this.alt;
    }

    var img_selfie        = document.getElementById("img_selfie");
    img_selfie.onclick    = function(){
    modal.style.display   = "block";
    modalImg.src          = this.src;
    captionText.innerHTML = this.alt;
    }

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];
    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
    modal.style.display = "none";
    }
