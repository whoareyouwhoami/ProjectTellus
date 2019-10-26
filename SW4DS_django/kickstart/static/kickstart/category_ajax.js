$("#id_main_category").change(function() {
  var url = $("#kickForm").attr("data-cat-url");
  var mcatid = $(this).val();

  $.ajax({
    url: url,
    data: {
      'main_category': mcatid
    },
    success: function(data) {
      $("#id_category").html(data);
    }
  });
});