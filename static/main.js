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

  $('#user-list-btn').on('click', function(event){
    event.preventDefault()
    console.log('user-list-btn clicked')
    var user_list = $('#user-list').val()
    alert('this list will be merged with existing one')
    $.ajax({
      type: 'GET',
      url: '/user_list_update/',
      data: {
        'user_list': user_list,
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
