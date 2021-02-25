
const seats_requested= localStorage.getItem('selectedSeats')? JSON.parse(localStorage.getItem('selectedSeats')) : []
// const movie_title=movieSelect.options[movieSelect.selectedIndex].id
const all_seats = document.querySelectorAll('.row .seat');

const seats_list=seats_requested.map(seat=> seat+1 )

async function contactAPI(url,body){
    const response=await fetch(url,{
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector("input[name='csrfmiddlewaretoken']").value
        },
        body:JSON.stringify(body)
    })

    return response.json()
}

function refreshSeat(){
    const movie_title=movieSelect.options[movieSelect.selectedIndex].id
    contactAPI('/occupied/',{movie_title}).then(data=>{
        const occupied_seat = data['occupied_seat'];
        const movie_title=data['movie']
        
        const seats_localStorage=localStorage.getItem('selectedSeats') ? JSON.parse(localStorage.getItem('selectedSeats')):null
        const movie_index=localStorage.getItem('selectedMovieIndex')

        all_seats.forEach(seat=>{
            seat.classList.remove('occupied')
        })
        
        const LS_movie=movieSelect.options[movie_index].textContent
        if(LS_movie===movie_title){
            if (occupied_seat !== null && occupied_seat.length > 0) {
                all_seats.forEach((seat, index) => {
                if (occupied_seat.indexOf(index) > -1) {
                    seat.classList.add('occupied');
                    seat.classList.remove('selected');
                }
                    });
                }
    
            if(seats_localStorage != null){
                seats_localStorage.forEach((e,index)=>{
                    if(occupied_seat.includes(e)){
                        seats_localStorage.splice(index,1)
                        localStorage.setItem('selectedSeats',seats_localStorage)
                        console.log(seats_localStorage)
                    }
                })
            }
        }
        updateSelectedCount()
    })
}

refreshSeat()

cta_btn.addEventListener("click",e=>{
    const movie_title=movieSelect.options[movieSelect.selectedIndex].id
    const seats_list=JSON.parse(localStorage.getItem('selectedSeats'))

    if(seats_list!==null && seats_list.length>0){
        data={movie_title,seats_list}
        contactAPI('/payment/',data).then(res=>{
           if(res['payment_url']){
               console.log('working')
            //    window.open(res['payment_url'],'_blank')
            // window.location.replace(res['payment_url'])
            window.location.href=res['payment_url']
           }
           if(res['error']){
               console('error')
           }
        }).catch(e=>{
            console.log(e)
        })
    }
})

