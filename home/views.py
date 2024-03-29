from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages

from .models import SiteHits
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from algo_blog.settings import DEFAULT_FROM_EMAIL
import json

all_routes = []

graph = {
    "Morden": {"Line": ["Northern Line"], "Connections":["South Wimbledon"]},
    "South Wimbledon": {"Line": ["Northern Line"], "Connections":["Morden", "Colliers Wood"]},
    "Colliers Wood": {"Line": ["Northern Line"], "Connections":["South Wimbledon", "Tooting Broadway"]},
    "Tooting Broadway": {"Line": ["Northern Line"], "Connections":["Colliers Wood", "Tooting Bec"]},
    "Tooting Bec": {"Line": ["Northern Line"], "Connections":["Tooting Broadway", "Balham"]},
    "Balham": {"Line": ["Northern Line"], "Connections":["Tooting Bec", "Clapham South"]},
    "Clapham South": {"Line": ["Northern Line"], "Connections":["Balham", "Clapham Common"]},
    "Clapham Common": {"Line": ["Northern Line"], "Connections":["Clapham South", "Clapham North"]},
    "Clapham North": {"Line": ["Northern Line"], "Connections":["Clapham Common", "Stockwell"]},
    "Stockwell": {"Line": ["Northern Line", "Victoria Line"], "Connections":["Oval", "Clapham North", "Vauxhall", "Brixton"]},
    "Oval": {"Line": ["Northern Line"], "Connections":["Stockwell", "Kennington"]},
    "Kennington": {"Line": ["Northern Line"], "Connections":["Nine Elms", "Waterloo", "Elephant And Castle"]},
    "Nine Elms": {"Line": ["Northern Line"], "Connections":["Battersea Power Station"]},
    "Waterloo": {"Line": ["Northern Line", "Bakerloo Line"], "Connections":["Kennington", "Embankment", "Lambeth North"]},
    "Battersea Power Station": {"Line": ["Northern Line"], "Connections":["Nine Elms"]},
    "Embankment": {"Line": ["Northern Line", "Circle Line", "Bakerloo Line"], "Connections":["Waterloo", "Charing Cross", "Westminister", "Temple"]},
    "Charing Cross": {"Line": ["Northern Line", "Bakerloo Line"], "Connections":["Embankment", "Leceister Square", "Picadilly Circus"]},
    "Leceister Square": {"Line": ["Northern Line"], "Connections":["Charing Cross", "Totternham Court Road"]},
    "Totternham Court Road": {"Line": ["Northern Line", "Central Line"], "Connections":["Leceister Square", "Warren Street", "Oxford Circus", "Holborn"]},
    "Warren Street": {"Line": ["Northern Line", "Victoria Line"], "Connections":["Totternham Court Road", "Euston", "Oxford Circus"]},
    "Elephant And Castle": {"Line": ["Northern Line", "Bakerloo Line"], "Connections":["Kennington", "Borough", "Lambeth North"]},
    "Borough": {"Line": ["Northern Line"], "Connections":["Elephant And Castle", "London Bridge"]},
    "London Bridge": {"Line": ["Northern Line"], "Connections":["Borough", "Bank"]},
    "Bank": {"Line": ["Northern Line"], "Connections":["London Bridge", "Moorgate"]},
    "Moorgate": {"Line": ["Northern Line"], "Connections":["Bank", "Old Street"]},
    "Old Street": {"Line": ["Northern Line"], "Connections":["Bank", "Angel"]},
    "Angel": {"Line": ["Northern Line"], "Connections":["Old Street", "King's Cross"]},
    "King's Cross": {"Line": ["Northern Line", "Victoria Line", "Circle line"], "Connections":["Angel", "Euston", "Highbury And Islington", "Farringdon", "Euston Square"]},
    "Euston": {"Line": ["Northern Line", "Victoria Line"], "Connections":["King's Cross", "Warren Street","Mornington Crescent", "Euston Square"]},
    "Mornington Crescent": {"Line": ["Northern Line"], "Connections":["Euston", "Camden Town"]},
    "Camden Town": {"Line": ["Northern Line"], "Connections":["Mornington Crescent", "Chalk Farm", "Kentish Town"]},
    "Chalk Farm": {"Line": ["Northern Line"], "Connections":["Camden Town", "Belsize Park"]},
    "Belsize Park": {"Line": ["Northern Line"], "Connections":["Chalk Farm", "Hamstead"]},
    "Hamstead": {"Line": ["Northern Line"], "Connections":["Belsize Park", "Golders Green"]},
    "Golders Green": {"Line": ["Northern Line"], "Connections":["Hamstead", "Brent Cross"]},
    "Brent Cross": {"Line": ["Northern Line"], "Connections":["Golders Green", "Hendon Central"]},
    "Hendon Central": {"Line": ["Northern Line"], "Connections":["Brent Cross", "Collindale"]},
    "Collindale": {"Line": ["Northern Line"], "Connections":["Hendon Central", "Burnt Oak"]},
    "Burnt Oak": {"Line": ["Northern Line"], "Connections":["Collindale", "Edgware"]},
    "Edgware": {"Line": ["Northern Line"], "Connections":["Burnt Oak"]},
    "Kentish Town": {"Line": ["Northern Line"], "Connections":["Camden Town", "Tufnell Park"]},
    "Tufnell Park": {"Line": ["Northern Line"], "Connections":["Kentish Town", "Archway"]},
    "Archway": {"Line": ["Northern Line"], "Connections":["Tufnell Park", "Highgate"]},
    "Highgate": {"Line": ["Northern Line"], "Connections":["Archway", "East Finchley"]},
    "East Finchley": {"Line": ["Northern Line"], "Connections":["Highgate", "Finchley Central"]},
    "Finchley Central": {"Line": ["Northern Line"], "Connections":["East Finchley", "Mill Hill East", "West Finchley"]},
    "Mill Hill East": {"Line": ["Northern Line"], "Connections":["Finchley Central"]},
    "West Finchley": {"Line": ["Northern Line"], "Connections":["Finchley Central", "Woodside Park"]},
    "Woodside Park": {"Line": ["Northern Line"], "Connections":["West Finchley", "Totteridge And Whetstone"]},
    "Totteridge And Whetstone": {"Line": ["Northern Line"], "Connections":["Woodside Park", "High Barnet"]},
    "High Barnet": {"Line": ["Northern Line"], "Connections":["Totteridge And Whetstone"]},
    "West Ruislip": {"Line": ["Central Line"], "Connections":["Ruislip Gardens"]},
    "Ruislip Gardens": {"Line": ["Central Line"], "Connections":["West Ruislip", "South Ruislip"]},
    "South Ruislip": {"Line": ["Central Line"], "Connections":["Ruislip Gardens", "Northolt"]},
    "Northolt": {"Line": ["Central Line"], "Connections":["South Ruislip", "Greenford"]},
    "Greenford": {"Line": ["Central Line"], "Connections":["Northolt", "Pervale"]},
    "Pervale": {"Line": ["Central Line"], "Connections":["Greenford", "Hanger Lane"]},
    "Hanger Lane": {"Line": ["Central Line"], "Connections":["Pervale", "North Acton"]},
    "Ealing Broadway": {"Line": ["Central Line"], "Connections":["West Acton"]},
    "West Acton": {"Line": ["Central Line"], "Connections":["Ealing Broadway", "North Acton"]},
    "North Acton": {"Line": ["Central Line"], "Connections":["West Acton", "East Acton", "Hanger Lane"]},
    "East Acton": {"Line": ["Central Line"], "Connections":["North Acton", "White City"]},
    "White City": {"Line": ["Central Line"], "Connections":["East Acton", "Sherperd's Bush"]},
    "Sherperd's Bush": {"Line": ["Central Line"], "Connections":["White City", "Holland Park"]},
    "Holland Park": {"Line": ["Central Line"], "Connections":["Sherperd's Bush", "Notting Hill Gate"]},
    "Notting Hill Gate": {"Line": ["Central Line, Circle Line"], "Connections":["Holland Park", "Queensway", "Bayswater", "High Street kensington"]},
    "Queensway": {"Line": ["Central Line"], "Connections":["Notting Hill Gate", "Lancaster Gate"]},
    "Lancaster Gate": {"Line": ["Central Line"], "Connections":["Queensway", "Marble Arch"]},
    "Marble Arch": {"Line": ["Central Line"], "Connections":["Lancaster Gate", "Bond Street"]},
    "Bond Street": {"Line": ["Central Line"], "Connections":["Marble Arch", "Oxford Circus"]},
    "Oxford Circus": {"Line": ["Central Line", "Victoria Line", "Bakerloo Line"], "Connections":["Bond Street", "Totternham Court Road", "Green Park", "Warren Street", "Regent's Park", "Picadilly Circus"]},
    "Holborn": {"Line": ["Central Line"], "Connections":["Totternham Court Road", "Chancery Lane"]},
    "Chancery Lane": {"Line": ["Central Line"], "Connections":["Holborn", "St Paul's"]},
    "St Paul's": {"Line": ["Central Line"], "Connections":["Chancery Lane", "Bank"]},
    "Bank": {"Line": ["Central Line"], "Connections":["St Paul's", "Liverpool Street"]},
    "Liverpool Street": {"Line": ["Central Line", "Circle Line"], "Connections":["Bank", "Berthnal Green", "Aldgate", "Moorgate"]},
    "Berthnal Green": {"Line": ["Central Line"], "Connections":["Liverpool Street", "Mile End"]},
    "Mile End": {"Line": ["Central Line"], "Connections":["Berthnal Green", "Stratford"]},
    "Stratford": {"Line": ["Central Line"], "Connections":["Mile End", "Leyton"]},
    "Leyton": {"Line": ["Central Line"], "Connections":["Stratford", "Leytonstone"]},
    "Leytonstone": {"Line": ["Central Line"], "Connections":["Leyton", "Snaresbrook", "Wanstead"]},
    "Snaresbrook": {"Line": ["Central Line"], "Connections":["Leytonstone", "South Woodford"]},
    "South Woodford": {"Line": ["Central Line"], "Connections":["Snaresbrook", "Woodford"]},
    "Woodford": {"Line": ["Central Line"], "Connections":["South Woodford", "Roding Valley", "Buckhurst Hill"]},
    "Wanstead": {"Line": ["Central Line"], "Connections":["Leytonstone", "Redbridge"]},
    "Redbridge": {"Line": ["Central Line"], "Connections":["Wanstead", "Gants Hill"]},
    "Gants Hill": {"Line": ["Central Line"], "Connections":["Redbridge", "Newbury Park"]},
    "Newbury Park": {"Line": ["Central Line"], "Connections":["Gants Hill", "Barkingside"]},
    "Barkingside": {"Line": ["Central Line"], "Connections":["Newbury Park", "Fairlop"]},
    "Fairlop": {"Line": ["Central Line"], "Connections":["Barkingside", "Hainault"]},
    "Hainault": {"Line": ["Central Line"], "Connections":["Fairlop", "Grange Hill"]},
    "Grange Hill": {"Line": ["Central Line"], "Connections":["Hainault", "Chigwell"]},
    "Chigwell": {"Line": ["Central Line"], "Connections":["Grange Hill", "Roding Valley"]},
    "Roding Valley": {"Line": ["Central Line"], "Connections":["Chigwell", "Roding Valley"]},
    "Buckhurst Hill": {"Line": ["Central Line"], "Connections":["Roding Valley", "Woodford" , "Loughton"]},
    "Loughton": {"Line": ["Central Line"], "Connections":["Debdon" , "Buckhurst Hill"]},
    "Debdon": {"Line": ["Central Line"], "Connections":["Loughton" , "Theydon Bois"]},
    "Theydon Bois": {"Line": ["Central Line"], "Connections":["Debdon" , "Epping"]},
    "Epping": {"Line": ["Central Line"], "Connections":["Theydon Bois"]},
    "Brixton": {"Line": ["Victoria Line"], "Connections":["Stockwell"]},
    "Vauxhall": {"Line": ["Victoria Line"], "Connections":["Stockwell", "Pimlico"]},
    "Pimlico": {"Line": ["Victoria Line"], "Connections":["Vauxhall", "Victoria"]},
    "Victoria": {"Line": ["Victoria Line", "Circle Line"], "Connections":["Pimlico", "Green Park", "Sloune Sqaure", "St Jame's Park"]},
    "Green Park": {"Line": ["Victoria Line"], "Connections":["Victoria", "Oxford Circus"]},
    "Highbury And Islington": {"Line": ["Victoria Line"], "Connections":["King's Cross", "Finsbury Park"]},
    "Finsbury Park": {"Line": ["Victoria Line"], "Connections":["Highbury And Islington", "Seven Sister's"]},
    "Seven Sister's": {"Line": ["Victoria Line"], "Connections":["Finsbury Park", "Tottenham Hale"]},
    "Tottenham Hale": {"Line": ["Victoria Line"], "Connections":["Seven Sister's", "Blackhorse Road"]},
    "Blackhorse Road": {"Line": ["Victoria Line"], "Connections":["Tottenham Hale", "Walthamstow Central"]},
    "Walthamstow Central": {"Line": ["Victoria Line"], "Connections":["Blackhorse Road"]},
    "Edgware Road": {"Line": ["Circle Line", "Bakerloo Line"], "Connections":["Bayswater", "Baker Street", "Royal Oak", "Warwick Avenue" ,"Marylebone"]},
    "Bayswater": {"Line": ["Circle Line"], "Connections":["Edgware Road", "Notting Hill Gate"]},
    "High Street kensington": {"Line": ["Circle Line"], "Connections":["Gloucester Road", "Notting Hill Gate"]},
    "Gloucester Road": {"Line": ["Circle Line"], "Connections":["High Street kensington", "South kensington"]},
    "South kensington": {"Line": ["Circle Line"], "Connections":["Gloucester Road", "Sloune Sqaure"]},
    "Sloune Sqaure": {"Line": ["Circle Line"], "Connections":["South kensington", "Victoria"]},
    "St Jame's Park":  {"Line": ["Circle Line"], "Connections":["Westminister", "Victoria"]},
    "Westminister":  {"Line": ["Circle Line"], "Connections":["St Jame's Park", "Embankment"]},
    "Temple": {"Line": ["Circle Line"], "Connections":["Blackfriar's", "Embankment"]},
    "Blackfriar's": {"Line": ["Circle Line"], "Connections":["Temple", "Mansion House"]},
    "Mansion House": {"Line": ["Circle Line"], "Connections":["Blackfriar's", "Canon Street"]},
    "Canon Street": {"Line": ["Circle Line"], "Connections":["Mansion House", "Monument"]},
    "Monument": {"Line": ["Circle Line"], "Connections":["Canon Street", "Tower Hill"]},
    "Tower Hill": {"Line": ["Circle Line"], "Connections":["Monument", "Aldgate"]},
    "Aldgate": {"Line": ["Circle Line"], "Connections":["Liverpool Street", "Aldgate"]},
    "Moorgate": {"Line": ["Circle Line"], "Connections":["Liverpool Street", "Barbican"]},
    "Barbican": {"Line": ["Circle Line"], "Connections":["Moorgate", "Farringdon"]},
    "Farringdon": {"Line": ["Circle Line"], "Connections":["Barbican", "King's Cross"]},
    "Euston Square": {"Line": ["Circle Line"], "Connections":["Great Portland street", "King's Cross"]},
    "Great Portland street": {"Line": ["Circle Line"], "Connections":["Euston Square", "Baker Street"]},
    "Baker Street": {"Line": ["Circle Line", "Bakerloo Line"], "Connections":["Great Portland street", "Edgware Road", "Marylebone", "Regent's Park"]},
    "Royal Oak": {"Line": ["Circle Line"], "Connections":["WestBourne Park", "Edgware Road"]},
    "WestBourne Park": {"Line": ["Circle Line"], "Connections":["Royal Oak", "Ladbroke Grove"]},
    "Ladbroke Grove": {"Line": ["Circle Line"], "Connections":["WestBourne Park", "Latimer Road"]},
    "Latimer Road": {"Line": ["Circle Line"], "Connections":["Ladbroke Grove", "Wood Lane"]},
    "Wood Lane": {"Line": ["Circle Line"], "Connections":["Latimer Road", "Shepherd's Bush Market"]},
    "Shepherd's Bush Market": {"Line": ["Circle Line"], "Connections":["Wood Lane", "Goldhawk Road"]},
    "Goldhawk Road": {"Line": ["Circle Line"], "Connections":["Shepherd's Bush Market"]},
    "Harrow and Wealdstone": {"Line": ["Bakerloo Line"], "Connections":["Kenton"]},
    "Kenton": {"Line": ["Bakerloo Line"], "Connections":["Harrow and Wealdstone", "South Kenton"]},
    "South Kenton": {"Line": ["Bakerloo Line"], "Connections":["Kenton", "North Wembley"]},
    "North Wembley": {"Line": ["Bakerloo Line"], "Connections":["South Kenton", "Wembley Central"]},
    "Wembley Central": {"Line": ["Bakerloo Line"], "Connections":["North Wembley", "Stonebridge Park"]},
    "Stonebridge Park": {"Line": ["Bakerloo Line"], "Connections":["Wembley Central", "Harlesdon"]},
    "Harlesdon": {"Line": ["Bakerloo Line"], "Connections":["Stonebridge Park", "Willesdon Junction"]},
    "Willesdon Junction": {"Line": ["Bakerloo Line"], "Connections":["Harlesdon", "Kensal Green"]},
    "Kensal Green": {"Line": ["Bakerloo Line"], "Connections":["Willesdon Junction", "Queen's Park"]},
    "Queen's Park": {"Line": ["Bakerloo Line"], "Connections":["Kensal Green", "Kilburn Park"]},
    "Kilburn Park": {"Line": ["Bakerloo Line"], "Connections":["Queen's Park", "Maida Vale"]},
    "Maida Vale": {"Line": ["Bakerloo Line"], "Connections":["Kilburn Park", "Warwick Avenue"]},
    "Warwick Avenue": {"Line": ["Bakerloo Line"], "Connections":["Edgware Road", "Maida Vale"]},
    "Marylebone": {"Line": ["Bakerloo Line"], "Connections":["Edgware Road", "Baker Street"]},
    "Regent's Park": {"Line": ["Bakerloo Line"], "Connections":["Oxford Circus", "Baker Street"]},
    "Picadilly Circus": {"Line": ["Bakerloo Line"], "Connections":["Oxford Circus", "Charing Cross"]},
    "Lambeth North": {"Line": ["Bakerloo Line"], "Connections":["Waterloo", "Elephant And Castle"]},
}

# Create your views here
def index(request):
    """A view to return the index page"""

    visitor = get_object_or_404(SiteHits, visitors="visitor")

    visitor.count += 1

    visitor.save()

    return render(request, "home/index.html")


def send_comment(request):
    """ A send comment to mail """
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        comment = request.POST['comment']

        subject = "Comment Received from SimpleAlgo"
        body = f'Message from {username}\n{email}\n{comment}'

        send_mail(
            subject,
            body,
            DEFAULT_FROM_EMAIL,
            ["zahurmeerun@hotmail.com"]
        )
    messages.success(request, "Thanks for your Feedback!")
    return redirect(reverse("home"))

def part_two(request):

    stations = ['Morden', 'South Wimbledon', 'Colliers Wood', 'Tooting Broadway', 'Tooting Bec',
        'Balham', 'Clapham South', 'Clapham Common', 'Clapham North', 'Stockwell', 'Oval', 'Kennington',
        'Nine Elms', 'Waterloo', 'Battersea Power Station', 'Embankment', 'Charing Cross', 'Leceister Square', 
        'Totternham Court Road', 'Warren Street', 'Elephant And Castle', 'Borough', 'London Bridge', 'Bank', 
        'Moorgate', 'Old Street', 'Angel', "King's Cross", 'Euston', 'Mornington Crescent', 'Camden Town', 
        'Chalk Farm', 'Belsize Park', 'Hamstead', 'Golders Green', 'Brent Cross', 'Hendon Central', 'Collindale', 
        'Burnt Oak', 'Edgware', 'Kentish Town', 'Tufnell Park', 'Archway', 'Highgate', 'East Finchley', 'Finchley Central', 
        'Mill Hill East', 'West Finchley', 'Woodside Park', 'Totteridge And Whetstone', 'High Barnet', 'West Ruislip', 
        'Ruislip Gardens', 'South Ruislip', 'Northolt', 'Greenford', 'Pervale', 'Hanger Lane', 'Ealing Broadway', 'West Acton', 
        'North Acton', 'East Acton', 'White City', "Sherperd's Bush", 'Holland Park', 'Notting Hill Gate', 'Queensway', 
        'Lancaster Gate', 'Marble Arch', 'Bond Street', 'Oxford Circus', 'Holborn', 'Chancery Lane', "St Paul's", 'Liverpool Street', 
        'Berthnal Green', 'Mile End', 'Stratford', 'Leyton', 'Leytonstone', 'Snaresbrook', 'South Woodford', 'Woodford', 'Wanstead', 
        'Redbridge', 'Gants Hill', 'Newbury Park', 'Barkingside', 'Fairlop', 'Hainault', 'Grange Hill', 'Chigwell', 'Roding Valley', 
        'Buckhurst Hill', 'Loughton', 'Debdon', 'Theydon Bois', 'Epping', 'Brixton', 'Vauxhall', 'Pimlico', 'Victoria', 'Green Park', 
        'Eustons', 'Highbury And Islington', 'Finsbury Park', "Seven Sister's", 'Tottenham Hale', 'Blackhorse Road', 
        'Walthamstow Central', 'Edgware Road', 'Bayswater', 'High Street kensington', 'Gloucester Road', 'South kensington', 
        'Sloune Sqaure', "St Jame's Park", 'Westminister', 'Temple', "Blackfriar's", 'Mansion House', 'Canon Street', 'Monument', 
        'Tower Hill', 'Aldgate', 'Barbican', 'Farringdon', 'Euston Square', 'Great Portland street', 'Baker Street', 'Royal Oak', 
        'WestBourne Park', 'Ladbroke Grove', 'Latimer Road', 'Wood Lane', "Shepherd's Bush Market", 'Goldhawk Road', 'Harrow and Wealdstone', 
        'Kenton', 'South Kenton', 'North Wembley', 'Wembley Central', 'Stonebridge Park', 'Harlesdon', 'Willesdon Junction', 'Kensal Green', "Queen's Park", 
        'Kilburn Park', 'Maida Vale', 'Warwick Avenue', 'Marylebone', "Regent's Park", 'Picadilly Circus', 'Lambeth North']

    context = {
        'stations': stations,
    }
    return render(request, "home/part_two.html", context)


@require_http_methods(["POST"])
def compute_paths(request):

    all_routes = []

    data = json.loads(request.body)


    def find_connections(graph, vertex, visited):
        stack = []   
        for node in graph[vertex]['Connections']:
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
            if end in route and route[:route.index(end)+1] not in my_paths:
                my_paths.append(route[:route.index(end)+1])
        
        my_paths = sorted(my_paths, key = len)

        station_path = []

        for path in my_paths:
            new_list = [{station: graph[station]["Line"]} for station in path]
            station_path.append(new_list)
        
        return station_path[:3]
    

    try:
        result = find_routes(graph, data['departure'], data['arrival'])
    except:
        result = None

    return JsonResponse({'path': result})
