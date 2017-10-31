$(document).ready(function(){

  $('#update-btn').on('click', function(event){

    event.preventDefault()
    var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
    var access_token = $('#access_token').val()
    $.ajaxSetup({
      beforeSend: function(xhr, settings){
        xhr.setRequestHeader('X-CSRFToken', csrf_token)
      }
    })
    $.ajax({
      type: 'POST',
      url: '/update/',
      data: {
        'access_token': access_token
      },
      success: function(data, status, xhr){
        alert(data['msg'])
      },
      error: function(xhr, status, error){
        console.error(error)
      }
    })

  })

})
