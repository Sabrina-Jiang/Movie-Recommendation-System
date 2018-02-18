$('.user-icon').on('click', () => {
  renderStars()
  $('.float-list').toggleClass('no-height')
  setTimeout(() => {
    $('.float-list').toggleClass('disappear')
  }, 10)
})

$('.close').click(() => {
  $('.float-list').toggleClass('disappear')
  setTimeout(() => {
    $('.float-list').toggleClass('no-height')
  }, 300)
})

$('.clear').click(() => {
  store.set('stars', [])
  renderStars()
})

function renderStars () {
  let data = store.get('stars') || []
  $('.float-container').html(data
    .map(item =>
      `<div class="float-item">
        <div class="item-img">
            <a href="/details?id=${item.id}" target="_blank">
                <img src="/getMovieCover?id=${item.id}" alt="">
            </a>
        </div>
        <div class="intro">
            <div class="item-title">
                <a href="/details?id=${item.id}" target="_blank">${item.title}</a>
            </div>
            <div class="item-summary">${item.summary}</div>
        </div>
    </div>`
    ))
  if (data.length === 0) {
    $('.float-container').html(`<p class="nothing">Nothing started!</p>`)
  }
}

renderStars()
