'use strict'

const stateMachine1 = {
  username: '',
  password: ''
}

const signInHTML = 'Username:<br>' +
  '<input id="swal-input1" class="swal2-input">' +
  'Password:<br>' +
  '<input id="swal-input2" class="swal2-input" type="password">'

$('.sign-in').click(() => {
  swal({
    title: 'Login',
    html: signInHTML,
    confirmButtonColor: '#992e28',
    focusConfirm: false,
    preConfirm: function () {
      return new Promise(function (resolve) {
        resolve({
          username: $('#swal-input1').val(),
          password: $('#swal-input2').val()
        })
      })
    }
  }).then(result => {
    console.log(result)
    $.ajax(
      {
        url: SERVER_URL + '/login',
        method: 'POST',
        data: result,
        success: function (res) {
          console.log(res)
          if (res.result[0]) {
            $.cookie('session', res.result[1])
            swal({
              title: 'success!',
              confirmButtonColor: '#992e28'
            }).then(() => {
              history.go(0)
            })
          }
          else {
            swal({title: 'Error!'})
          }
        }
      }
    )
  })
})

const registerHTML = 'Username:<br>' +
  '<input id="swal-input1" class="swal2-input">' +
  'Password:<br>' +
  '<input id="swal-input2" class="swal2-input" type="password">' +
  'Confirm Password:<br>' +
  '<input id="swal-input3" class="swal2-input" type="password">'

$('.register').click(() => {
  swal({
    title: 'Register',
    html: registerHTML,
    method: 'POST',
    confirmButtonColor: '#992e28',
    focusConfirm: false,
    preConfirm: function () {
      return new Promise(function (resolve) {
        resolve({
          username: $('#swal-input1').val(),
          password: $('#swal-input2').val()
        })
      })
    }
  }).then(result => {
    $.ajax(
      {
        url: SERVER_URL + '/register',
        method: 'POST',
        data: result,
        success: (res) => {
          if (res[0]) {
            $.cookie('session', res[1])
            swal({
              title: 'success!',
              confirmButtonColor: '#992e28'
            }).then(() => {
              history.go(0)
            })
          }
          else {
            swal({title: 'Error!'})
          }
        }
      }
    )
  })
})

$('.user-name').click(() => {
  swal({
    title: 'Logout?',
    text: 'You are logging out.',
    type: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#992e28',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'logout'
  }).then((result) => {
    if (result) {
      swal(
        'Logged out!',
        'Your have logged out.',
        'success'
      ).then(() => {
        $.cookie('session', null)
        history.go(0)
      })
    }
  })
})
