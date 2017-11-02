$(document).ready(function(){

  $('#update-btn').on('click', function(event){

    event.preventDefault();
    var access_token = $('#access_token').val();
    //var csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    //$.ajaxSetup({
      //beforeSend: function(xhr, settings){
        //xhr.setRequestHeader('X-CSRFToken', csrf_token);
      //}
    //})
    //console.log('csrftoken:', csrf_token);
    alert('update requested');
    $.ajax({
      type: 'GET',
      url: '/update/',
      data: {
        'access_token': access_token
      },
      success: function(data, status, xhr){
        alert(data['msg']);
      },
      error: function(xhr, status, error){
        console.error(error);
      }
    })

  })

})
