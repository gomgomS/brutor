$(document).ready(function () {
  const options = document.getElementById("addVesselOptions");
  const file = document.getElementById("inpFile");
  const tugImg = document.getElementById("imgTugboat");
  options.addEventListener("click", (e) => {
    const target = e.target.classList;
    if (target.contains("add-vessel-option")) {
      const allOptions = document.querySelectorAll(".add-vessel-option");
      allOptions.forEach((el) => {
        el.classList.add("add-vessel-option--unactive");
      });
      target.remove("add-vessel-option--unactive");

      const bodies = document.querySelectorAll(".add-vessel-body");
      bodies.forEach((el) => {
        el.classList.remove("add-vessel-body--active");
      });

      const targetData = e.target.dataset.option;
      const targetBody = document.querySelectorAll(`.${targetData}`);
      targetBody.forEach((el) => {
        el.classList.add("add-vessel-body--active");
      });
    }
  });
  file.addEventListener("change", function () {
    const selectedFiles = this.files[0];
    if (selectedFiles) {
      const reader = new FileReader();
      reader.addEventListener("load", function () {
        tugImg.setAttribute("src", this.result);
      });
      reader.readAsDataURL(selectedFiles);
    }
  });
});
