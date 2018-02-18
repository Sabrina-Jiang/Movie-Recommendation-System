'use strict'
// const SERVER_URL = 'https://cs542-yliu25.c9users.io'
const SERVER_URL = 'http://localhost:8080'

function onMovieClick(target) {
  let imdbId = $(target).attr('data-imdb-id')
  window.open(`/details?id=${imdbId}`)
}

$(document).ready(() => {
  $.ajax({
    url: '/profile',
    success: (res) => {
      if (res[0]) {
        let username = res[1][1]
        $('.user-name').html(username)
        $('.login-state').toggleClass('no-height')
      } else {
        $('.action-button').toggleClass('no-height')
      }
    }
  })
})
