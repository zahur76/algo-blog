from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages

from .models import SiteHits
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from algo_blog.settings import DEFAULT_FROM_EMAIL
import json


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
        body = comment

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

    data = json.loads(request.body)

    print(data)
    return JsonResponse({'path': 'Working'})
