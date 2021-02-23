
const seats_requested= localStorage.getItem('selectedSeats')? JSON.parse(localStorage.getItem('selectedSeats')) : null
const movie_title=movieSelect.options[movieSelect.selectedIndex].id

const seats_list=seats_requested.map(seat=> seat+1 )

async function contactAPI(url,body){
    const response=await fetch(url,{
        method:'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body:JSON.stringify(body)
    })

    return response.json()
}

contactAPI('/check_seats/',{seats_list,movie_title}).then(e=>{
    console.log(e)
})
