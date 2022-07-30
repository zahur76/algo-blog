from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json


all_routes = []
# Create your views here

def maze(request):
    """ 
    A view to return the  Maze editor
    
    """

    return render(request, "maze/maze.html")


@require_http_methods(["POST"])
def compute_maze(request):

    def find_connections(graph, vertex, visited):
        stack = [] 
        for node in graph[vertex]:
            if node not in visited:
                stack.append(visited + [node]) 

        if stack:
            for route in stack:
                find_connections(graph, route[-1], route)
        else:
            all_routes.append(visited)
        return all_routes


    def find_routes(graph, vertex, end, visited=[]):    
    
        visited.append(vertex)    
            
        paths = find_connections(graph, vertex, visited)

        my_paths = []
        for route in paths:
            if end in route:
                my_paths.append(route[:route.index(end)+1])
        path_length = []
        for path in my_paths:
            path_length.append(len(path))
        index_minimum = path_length.index(min(path_length))

        return my_paths[index_minimum]       

    data = json.loads(request.body)

    print(data)

    maze_dictionary = {}

    new_list = []

    for ele in data['maze']:
        new_list.append(int(ele))   

    for i in range(1, 101):
        if i not in new_list:
            if i == 1:
                maze_dictionary["1"] = [str(i+1), str(i+10)]
            elif i == 10:
                maze_dictionary["10"] = [str(i-1), str(i+10)]
            elif i == 91:
                maze_dictionary["91"] = [str(i+1) , str(i-10)]
            elif i == 100:
                maze_dictionary["100"] = [str(i-1), str(i-10)]
            elif i in [2, 3, 4, 5, 6, 7, 8, 9]:
                maze_dictionary[str(i)] = [str(i-1), str(i+1), str(i+10)]
            elif i in [92, 93, 94, 95, 96, 97, 98, 99]:
                maze_dictionary[str(i)] = [str(i-1), str(i+1), str(i-10)]
            elif i in [11, 21, 31, 41, 51, 61, 71, 81]:
                maze_dictionary[str(i)] = [str(i+1), str(i-10), str(i+10)]
            elif i in [20, 30, 40, 50, 60, 70, 80, 90]:
                maze_dictionary[str(i)] = [str(i-1), str(i-10), str(i+10)]
            else:
                maze_dictionary[str(i)] = [str(i-1), str(i+1), str(i-10), str(i+10)]
            
    for key, value in maze_dictionary.items():
        for node in new_list:
            if str(node) in value:
                value.remove(str(node))
    
    print(maze_dictionary)

    try:
        result = find_routes(maze_dictionary, data['start_node'], data['end_node'])
    except:
        result = None

    if result:
        return JsonResponse({'path': result[1:]})
    return JsonResponse({'path': 'None'})

def reset_maze(request):
    global all_routes
    all_routes = []
    return JsonResponse({'status': 'ok'})