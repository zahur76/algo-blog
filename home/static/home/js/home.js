$(document).ready(function(){

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
                })
                .catch((error) => {
                        console.log(error)
            });
        }   

    })
});