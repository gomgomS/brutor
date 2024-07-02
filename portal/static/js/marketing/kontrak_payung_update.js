$(document).ready(function () {
  const data = ["fromTime", "toTime"];

  data.forEach((el, i) => {
    $(`#${el}`).datepicker({ dateFormat: 'dd-mm-yy' });
    $(`.calendarIcon${i}`).click(function () {
      $(`#${el}`).focus();
    });
  });

});
