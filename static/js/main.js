'use strict'
let init = true

// State Machine
const stateMachine = {
  title: '',
  genres: '',
  years: '',
  rating: '',
  sort: 'rating'
}

// Filters Data
const dataList = {
  genres: ['All', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'],
  years: ['All', '2016', '2015', '2014', '2013-2012', '2011-2010', '1990', '1980', 'Earlier'],
  rating: ['All', '5.0-4.0', '4.0-3.0', '3.0-2.0', '2.0-1.0', '1.0']
}

// Dynamic generating DOM element for filters
const filterFactory = (type, mark, index) =>
  `<div class="filter animation" data-index="${index}" data-type="${type}" onclick="onFilterClick(this)">
    ${mark}
   </div>`

const movieFactory = (title, genres, rating, years, imdbId, description) =>
  `<div class="item">
    <img src="/getMovieCover?id=${imdbId}" alt="" onclick="onMovieClick(this)" data-imdb-id="${imdbId}">
    <div class="content">
      <div class="row">
        <div class="title" onclick="onMovieClick(this)" data-imdb-id="${imdbId}">${title}</div>
        <div class="rating">${parseInt(rating).toFixed(1)}</div>
      </div>
      <div class="row">
        <div class="description">${description}</div>
      </div>
      <div class="row">
        <div class="years">${years}</div>
        <div class="genres">${genres}</div>
      </div>
    </div>
  </div>`

const recommendFactory = (title, rate, imdbId) =>
  `<div class="item" onclick="onMovieClick(this)" data-imdb-id="${imdbId}">
    <div class="top">
        <img src="/getMovieCover?id=${imdbId}" alt="">
    </div>
    <div class="bottom">
        <p>${title}</p>
        <p>${parseInt(rate).toFixed(1)}</p>
     </div>
   </div>`

function requestAndRender (url, factory, slot) {
  return new Promise((resolve, reject) => {
    $.ajax({
      url: SERVER_URL + url,
      data: stateMachine,
    }).done((res) => {
      $('.match-slot').html(`${res.length} results matched!`)
      let list = res.reduce((template, item) => template + factory(item[0], item[1], item[2], item[3], item[4], item[5]), '')
      $(slot).html(list)
      resolve(true)
    }).fail(() => {
      reject(false)
    })
  })
}

function animationProcessor () {
  if (!init) return
  init = false
  $('.animation-header-slot').toggleClass('search-animation-header')
  $('.animation-title-slot').toggleClass('search-animation-title')
  $('.animation-disappear-slot').toggleClass('disappear')
  $('.animation-panel-slot').toggleClass('search-animation-panel')
  $('.animation-no-height-slot').toggleClass('no-height')
}

// Execute when page loaded
$(document).ready(() => {
  Object
    .keys(dataList)                           // ['genres', 'years', 'rating']
    .forEach(type => {                        // type = ...
      let currentList = dataList[type]        // dataList.genres / xx.y; type -> array
      $(`.${type}-slot`)                      // div.genres-slot
        .html(currentList                     // .html() -> insert currentList
          .reduce((template, item, index) =>  // [...].reduce((sum, item, index) => {} , '')
            template + filterFactory(type, currentList[index], index), '')) // template + filterFactory
    })

  // TODO: Give recommend data
  $.ajax({
    url: SERVER_URL + '/getBannerMovie',
    success: (res) => {
      $('.recommend-slot').html(res.map(item =>
        recommendFactory(item[1], parseInt(item[5]), item[7])))
    }
  })
})

// Filter Click Event
function onFilterClick (target) {
  // Get element attributes
  // Highlight attribute toggle
  let type = $(target).attr('data-type')
  $(`.filter[data-type=${type}][data-index=${dataList[type].indexOf(stateMachine[type])}]`).toggleClass('highlight')
  let index = $(target).attr('data-index')
  stateMachine[type] = dataList[type][index]
  $(target).toggleClass('highlight')

  // Start requesting
  requestAndRender('/getMovieList', movieFactory, '.movie-slot')
    .then(animationProcessor)

  console.log(`Event triggered on type: ${type}, at ${index}`)
}

// Search button event
$('.search-button').click(() => {
  stateMachine.title = $('.search-input').val()
  requestAndRender('/getMovieList', movieFactory, '.movie-slot')
    .then(animationProcessor)
})

$('.sort-option').click((e) => {
  $(`.sort-option[data-sort=${stateMachine.sort}]`).toggleClass('highlight')
  stateMachine.sort = $(e.target).attr('data-sort')
  $(e.target).toggleClass('highlight')
  requestAndRender('/getMovieList', movieFactory, '.movie-slot')
})
