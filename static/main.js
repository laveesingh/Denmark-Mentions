$(document).ready(function(){

  $('#update-btn').on('click', function(event){

    event.preventDefault();
    var access_token = $('#access_token').val();
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
