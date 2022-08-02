$(document).ready(function(){

    $('.reset-stations').hide();

    $('.reset-stations').click(function(){
        $("#arrival select").val('Destination Station');
        $("#departure select").val('Departure Station');

        $('.submit-stations').show();
        $('.reset-stations').hide();

        $('.path-results').html('');
    })

    function stationColour(station){
        if(station[0][0]==['Northern Line']){
            return `<span class="border-start border-5 border-dark text-dark ps-2">${station[0][0]}</span>`
        }else if(station[0][0]==['Victoria Line']){
            return `<span class="border-start border-5 border-info text-info ps-2">${station[0][0]}</span>`
        }else if(station[0][0]==['Central Line']){
            return `<span class="border-start border-5 border-danger text-danger ps-2">${station[0][0]}</span>`
        }else if(station[0][0]==['Bakerloo Line']){
            return `<span class="border-brown text-brown ps-2">${station[0][0]}</span>`
        }else{
            return `<span class="border-start border-5 border-warning text-warning ps-2">${station[0][0]}</span>`
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
            if(stationList[0]=='Northern Line'){
                return `<span class="border-start border-5 border-dark text-dark ps-2">${stationList[0]}</span>`
            }else if(stationList[0]=='Victoria Line'){
                return `<span class="border-start border-5 border-info text-info ps-2">${stationList[0]}</span>`
            }else if(stationList[0]=='Central Line'){
                return `<span class="border-start border-5 border-danger text-danger ps-2">${stationList[0]}</span>`
            }else if(stationList[0]=='Bakerloo Line'){
                return `<span class="border-brown text-brown ps-2">${stationList[0]}</span>`
            }else{
                return `<span class="border-start border-5 border-warning text-warning ps-2">${stationList[0]}</span>`
            }

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
                stations += `<div class="stops col-12 text-center"><span class="border border-dark rounded-2 bg-secondary text-light p-2">${Object.keys(element)} <i class="fas fa-subway"></i></span><div class="col-12 fw-bold stations p-3">${transit(stops, count)}</div>`                
            }else{
                stations += `<div class="stops col-12 text-center"><span class="border border-dark rounded-2 bg-secondary text-light p-2">${Object.keys(element)} <i class="fas fa-subway"></i></span><div class="col-12 fw-bold stations p-3">${stationColour(Object.values(element))}</div>` 
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
        }else if(departure==arrival){
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
                    $('.submit-stations').hide();
                    $('.reset-stations').show();
                    let i=0;
                    responseJson['path'].forEach(element => {
                        i++;
                        $('.path-results').append(
                            `<div class="col-12 m-2">
                                <a class="btn btn-success" data-bs-toggle="collapse" href="#collapseExample${i}" role="button" aria-expanded="false" aria-controls="collapseExample">path ${i} - ${element.length-1} stops <i class="ps-1 pb-1 my-auto fas fa-sort-down"></i></a>
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