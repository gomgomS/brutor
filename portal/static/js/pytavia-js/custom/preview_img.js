// Get the modal
    var modal = document.getElementById("modal-applicant-detail");

    // Get the image and insert it inside the modal - use its "alt" text as a caption
    var modalImg          = document.getElementById("modal_preview_img");
    var captionText       = document.getElementById("img_caption");

    var img_selfie        = document.getElementById("img_selfie");
    img_selfie.onclick    = function(){
       
        modalImg.src          = this.src;
        modalImg.style.width  = "100%";
        captionText.innerHTML = this.alt;
    }

    var img_ktp               = document.getElementById("img_ktp");
    img_ktp.onclick           = function(){
        //modal.style.display   = "block";
        modalImg.src          = this.src;
        modalImg.style.width  = "100%";
        captionText.innerHTML = this.alt;
    }

    var img_signature         = document.getElementById("img_signature");
    img_signature.onclick     = function(){        
        modalImg.src          = this.src;
        modalImg.style.width  = "100%";
        captionText.innerHTML = this.alt;
    }

    var img_npwp              = document.getElementById("img_npwp");
    img_npwp.onclick          = function(){        
        modalImg.src          = this.src;
        modalImg.style.width  = "100%";
        captionText.innerHTML = this.alt;
    }

    var img_income            = document.getElementById("img_income");
    img_income.onclick        = function(){        
        modalImg.src          = this.src;
        modalImg.style.width  = "100%";
        captionText.innerHTML = this.alt;
    }

    