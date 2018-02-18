function getQueryString (name) {
  let reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)')
  let r = window.location.search.substr(1).match(reg)
  if (r != null) return unescape(r[2])
  return null
}

let started = false

function toggleStar () {
  if (started) {
    $('.star').css({'display': 'inline-block'})
    $('.no-star').css({'display': 'none'})
  }
  else {
    $('.star').css({'display': 'none'})
    $('.no-star').css({'display': 'inline-block'})
  }
}

$('.star-button').click(() => {
  let imdbId = getQueryString('id')
  let result = store.get('stars') || []

  result = result.concat([{
    id: imdbId,
    title: $('.main-title').text().trim(),
    summary: $('.summary_text').text().trim()
  }])

  if (started)
    result = result.filter(item => item.id !== imdbId)

  // $.cookie('stars', JSON.stringify(result))
  store.set('stars', result)
  started = !started
  toggleStar()
})

let data = store.get('stars') || []

for (let item of data) {
  if (item.id === getQueryString('id')) {
    started = true
    break
  }
}
toggleStar()
