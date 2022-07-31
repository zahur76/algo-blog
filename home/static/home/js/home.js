$(document).ready(function(){


    function stationColour(station){
        if(station[0][0]==['Northern Line']){
            return `<span class="text-dark">${station[0][0]}</span>`
        }else if(station[0][0]==['Victoria Line']){
            return `<span class="text-info">${station[0][0]}</span>`
        }else if(station[0][0]==['Central Line']){
            return `<span class="text-danger">${station[0][0]}</span>`
        }else if(station[0][0]==['Bakerloo Line']){
            return `<span class="text-brown">${station[0][0]}</span>`
        }else{
            return `<span class="text-warning">${station[0][0]}</span>`
        }        
    }

    // function to check transit change

    function transit(stops, element){

        if(element <= stops.length-1){
            let stationList = [];
            let nextStation = Object.values(stops[element])[0];
            let actualStation = Object.values(stops[element-1])[0];
            for(let i=0; i<=nextStation.length; i++){
                for(let j=0; j<=actualStation.length; j++){
                    if(nextStation[i]==actualStation[j]){
                        stationList.push(nextStation[i])
                    }
                }
            }
            let station = stationColour([stationList[0]])
            return stationList[0]

        }else{
            return 'Destination!'
        }
        
    };
    // function to iterate through stations
    
    function stops(stops) {

        let stations = ''; 
        let count = 0
        stops.forEach(element => {
            count += 1
            if(Object.values(element)[0].length > 1 ){
                stations += `<div class="stops col-12 text-center"><span class="border border-dark p-2">${Object.keys(element)}</span><div class="col-12 fw-bold stations p-3">${transit(stops, count)}</div>`                
            }else{
                stations += `<div class="stops col-12 text-center"><span class="border border-dark p-2">${Object.keys(element)}</span><div class="col-12 fw-bold stations p-3">${stationColour(Object.values(element))}</div>` 
            }           
        })
        return stations
    }

    $('.submit-stations').click(function(e){
        e.preventDefault();

        let departure = $('#departure').val();
        let arrival = $('#arrival').val();
        let csrfToken = $('#token').val();

    
        if(!arrival && departure){
            $('#arrival').css('border', '2px solid red');
            setInterval(() => {
                $('#arrival').css('border', '1px solid #ced4da');
                $('#departure').css('border', '1px solid #ced4da');
            }, 1500);
        }else if(!departure && arrival){
            $('#departure').css('border', '2px solid red');
            setInterval(() => {
                $('#arrival').css('border', '1px solid #ced4da');
                $('#departure').css('border', '1px solid #ced4da');
            }, 1500);
        }else if(!departure && !arrival){
            $('#arrival').css('border', '2px solid red');
            $('#departure').css('border', '2px solid red');
            setInterval(() => {
                $('#arrival').css('border', '1px solid #ced4da');
                $('#departure').css('border', '1px solid #ced4da');
            }, 1500);
        }else{
            console.log('ok')
            data = {'departure': departure, 'arrival': arrival}

            fetch('/compute_paths', { method: 'POST', headers: {'X-CSRFToken': csrfToken}, body: JSON.stringify(data)})
            .then((response) => {
                if (response.ok) {          
                    return response.json();2
                }
                throw new Error('Something went wrong');
                })
                .then((responseJson) => {
                    console.log(responseJson)
                    let i=0;
                    responseJson['path'].forEach(element => {
                        console.log(element)
                        i++;
                        $('.path-results').append(
                            `<div class="col-12 m-2">
                                <a class="btn btn-success" data-bs-toggle="collapse" href="#collapseExample${i}" role="button" aria-expanded="false" aria-controls="collapseExample">path ${i} - ${element.length-1} stops</a>
                                    <div class="collapse" id="collapseExample${i}">
                                    <div class="card card-body border-0">${stops(element)}</div>
                                </div>
                            </div>`)
                    });
                })
                .catch((error) => {
                        console.log(error)
            });
        }   

    })
});