from django.shortcuts import render


# Create your views here
def maze(request):
    """ 
    A view to return the  Maze editor
    
    """


    return render(request, "maze/maze.html")
