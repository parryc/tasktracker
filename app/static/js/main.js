$(document).ready(function(){
  //CSRF setup from Flask-WTF docs
  var csrftoken = $('meta[name=csrf-token]').attr('content'); 
  var completeTask = function(){
    var id = $(this).attr('data-task-id')
        that = $(this);
    $.ajax({
      type: 'post',
      url: '/tasks/complete/' + id,
      contentType: 'application/json;charset=UTF-8',
      success: function(result) {
        that.removeClass('task-hover');
        that.parent().parent().addClass('task-complete');
        that.unbind('mouseenter mouseleave')
      }
    });
  }

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
      }
    }
  });

  $('.fa-circle').hover(function(){
    $(this).removeClass('fa-circle').addClass('fa-check-circle').addClass('task-hover')
    $(this).click(completeTask);
  },
  function(){
    if(!$(this).hasClass('fa-check-circle'))
      $(this).removeClass('fa-check-circle').removeClass('task-hover').addClass('fa-circle')
  });
});