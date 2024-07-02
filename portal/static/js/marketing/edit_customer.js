$(document).ready(function () {
  const editData = {
    editRegion: [
      { id: 1, text: "Ambon" },
      { id: 2, text: "Jambi" },
    ],
    editCity: [
      { id: 1, text: "Maluku" },
      { id: 2, text: "Jambi" },
    ],
  };

  for (const prop in editData) {
    $(`.${prop}`).select2({
      data: editData[prop],
      placeholder: "Please choose",
      width: "100%",
    });
  }
});
