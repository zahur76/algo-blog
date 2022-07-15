from django.shortcuts import render, reverse, redirect
from django.core.mail import send_mail
from django.contrib import messages


# Create your views here
def index(request):
    """A view to return the index page"""

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
            email,
            ["zahurmeerun@hotmail.com"]
        )
    messages.success(request, "Thanks for your Feedback!")
    return redirect(reverse("home"))