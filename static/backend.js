
const seats_requested= localStorage.getItem('selectedSeats')? JSON.parse(localStorage.getItem('selectedSeats')) : null
const movie_title=movieSelect.options[movieSelect.selectedIndex].id

const seat_list=seats_requested.map(seat=> seat+1 )

fetch('check_seats/',{
    method:'POST',
    headers:{
        'Content-Type': 'application/json'
    },
    body:JSON.stringify({
        'seat_numbers':seat_list,
        'movie_title':movie_title
    })
}).then(e=>{
    console.log(e)
})