$(document).ready(function(){
    
    let start = false;
    let end = false;
    let click = true;

    $('.end').hide();
    $('.maze').hide();
    $('.find-route').hide();
    $('.reset').hide();
    $('.solution').hide();

    let start_node = null;
    let end_node = null;
    let maze_node  = [];
    let result = [];
    
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
        }else if(node!==start_node && node!==end_node && click){
            if(maze_node.includes(node)){
                $(this).removeClass('bg-dark');
                var index = maze_node.indexOf(node);
                if (index !== -1) {
                maze_node.splice(index, 1);
                }
                console.log(maze_node)
            }else{
                console.log($(this).attr('id'));
                $(this).addClass('bg-dark');
                $('.find-route').show();
                maze_node.push(node)
                console.log(maze_node)
            }
            
        }
    })


    // send maze layout
    $('.find-route').click(function(){
        click = false

        let uniqueMaze = [...new Set(maze_node)];

        let csrfToken = $("#token").attr('value');
        data = {'start_node': start_node, 'end_node': end_node, 'maze': uniqueMaze}
        
        fetch('/maze/compute_maze', { method: 'POST', headers: {'X-CSRFToken': csrfToken}, body: JSON.stringify(data)})
        .then((response) => {
            if (response.ok) {          
                return response.json();
            }
            throw new Error('Something went wrong');
            })
            .then((responseJson) => {
                if(responseJson['path']==='None'){
                    console.log('none')
                    $('.maze').hide();
                    $('.solution').show().html('No Solution Found!');
                    $('.find-route').hide();
                    $('.reset').show();
                }else{
                    $('.maze').hide();
                    $('.solution').show().html('Maze Solved!');
                    $('.find-route').hide();
                    $('.reset').show();
                    result = responseJson['path']
                    responseJson['path'].forEach(element => {
                        $(`#${element}`).addClass('bg-warning');
                    });
                    $(`#${start_node}`).addClass('bg-primary')
                }
            })
            .catch((error) => {
                    console.log(error)
        });
    })

    $('.reset').click(function(){
        maze_node.forEach(element => {
            $(`#${element}`).attr('class', 'box border border-dark rounded-0 col-1')
        })
        result.forEach(element => {
            $(`#${element}`).attr('class', 'box border border-dark rounded-0 col-1')
        })
        $(`#${start_node}`).attr('class', 'box border border-dark rounded-0 col-1')
        $(`#${end_node}`).attr('class', 'box border border-dark rounded-0 col-1')
        start = false
        end = false
        click = true
        start_node = null
        end_node = null
        maze_node = []
        result = []
        $('.reset').hide();
        $('.find-route').hide();
        $('.solution').hide();
        $('.start').show();

        fetch('/maze/reset_maze')
        .then((response) => {
            if (response.ok) {          
                return response.json();
            }
            throw new Error('Something went wrong');
            })
            .then((responseJson) => {
                console.log(responseJson)
            })
    })
        
})