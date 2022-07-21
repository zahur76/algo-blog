$(document).ready(function(){ 
    
    let start = false
    let end = false

    $('.end').hide();
    $('.maze').hide();
    $('.find-route').hide();

    let start_node = null;
    let end_node = null;
    let maze_node  = [];

    $('.box').click(function(){
        let node = $(this).attr('id');
        if(!start){
            $(this).toggleClass('bg-primary');
            start = true;
            $('.start').hide();
            $('.end').show();
            start_node = $(this).attr("id")
        }else if(!end && node!=start_node){
            $(this).toggleClass('bg-danger');
            end = true;
            $('.end').hide();
            $('.maze').show();
            end_node = $(this).attr("id")
        }else if(node!==start_node && node!==end_node){
            console.log($(this).attr('id'));
            $(this).toggleClass('bg-warning');
            $('.find-route').show();
            maze_node.push(node)

            console.log(maze_node)
        }
    })


    // send maze layout
    $('.find-route').click(function(){       
        let csrfToken = $("#token").attr('value');
        data = {'start_node': start_node, 'end_node': end_node, 'maze': maze_node}
        
        fetch('/maze/compute_maze', { method: 'POST', headers: {'X-CSRFToken': csrfToken}, body: JSON.stringify(data)})
        .then((response) => {
            if (response.ok) {          
                return response.json();
            }
            throw new Error('Something went wrong');
            })
            .then((responseJson) => {
                console.log(responseJson)

            })
            .catch((error) => {
                    console.log(error)
        });
    })
        
})