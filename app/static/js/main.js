$(document).ready(function(){
  //CSRF setup from Flask-WTF docs
  var csrftoken = $('meta[name=csrf-token]').attr('content'); 

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
      }
    }
  });


  $('.fa-circle').click(function(evt){
    var id = $(this).attr('data-task-id')
        that = $(this);
    $.ajax({
      type: 'post',
      url: '/tasks/complete/' + id,
      contentType: 'application/json;charset=UTF-8',
      success: function(result) {
        that.removeClass('fa-circle').addClass('fa-check-circle');
        that.parent().parent().addClass('task-complete');
      }
    });
  });
});