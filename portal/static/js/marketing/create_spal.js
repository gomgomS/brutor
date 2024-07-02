$(document).ready(function () {
  const data = ["laycan", "laycanTo"];

  data.forEach((el, i) => {
    $(`#${el}`).datepicker({ dateFormat: 'dd-mm-yy' });

    $(`.calendarIcon${i}`).click(function () {
      $(`#${el}`).focus();
    });
  });

});
