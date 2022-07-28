from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages

from .models import SiteHits

from algo_blog.settings import DEFAULT_FROM_EMAIL


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
    return render(request, "home/part_two.html")
