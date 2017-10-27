$(document).ready(function(){
  $('#update-btn').on('click', function(){
    $.ajax({
      type: 'GET',
      url: '/update'
    })
  })
})
