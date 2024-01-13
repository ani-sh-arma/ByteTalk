from django.shortcuts import render, redirect, HttpResponse , get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Messages
import json


def index(request):

    if request.user.is_authenticated:
        return redirect('home')

    return render(request , 'home/index.html')



def register(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:

            new_user = User.objects.create_user(username, email, password)
            # new_user = UserCreationForm(request.POST)
            new_user.first_name = fname
            new_user.last_name = lname

            new_user.save()
            return redirect("login")
            # Redirect or perform other actions for successful registration
        except IntegrityError:
            # Handle the case when a user with the same username already exists
            error_message = (
                "Username already exists. Please choose a different username."
            )
            return render(
                request,
                "home/register.html",
                {"error_message": error_message},
            )

    else:
        return render(
            request, "home/register.html"
        )
    

def home(request):
    user = User.objects.all()

    if request.user.is_anonymous:
        return redirect('login')

    return render(request, "home/home.html" , {"users": user })


def chat(request, id):

    if request.user.is_anonymous:
        return redirect('login')


    user = User.objects.all()
    other_sender = get_object_or_404(User, id=id)

    sent_messages = Messages.objects.filter(sender = request.user, receiver = id)
    received_messages = Messages.objects.filter(sender = other_sender , receiver = request.user.id)

    messages = sent_messages.union(received_messages)

    return render(request, "home/home.html" , {"users": user, 'messages': messages , 'chat_to': other_sender})



def send_message(request):
    print("send_message")

    if request.method == 'POST':

        print("post method")
        data = json.loads(request.body)

        receiverId = data['receiverId']
        receiver = User.objects.get(id = receiverId)
        message = data['message']
        sender = request.user
        print(sender , receiverId, message)


        Messages.objects.create(sender = sender, receiver = receiver, message = message)

        return JsonResponse({'status': 'Message sent'})
    
    else:
        print("else block")
        return JsonResponse({'status': 'Error'})
    

from django.http import JsonResponse

def get_latest_messages(request, id):
    
    try:
        # Your logic to fetch the latest messages
        other_sender = get_object_or_404(User, id=id)

        sent_messages = Messages.objects.filter(sender=request.user, receiver=id)
        received_messages = Messages.objects.filter(sender=other_sender, receiver=request.user.id)

        messages = sent_messages.union(received_messages)

        # Convert User objects to their usernames
        messages_list = [{'sender': message.sender.username, 'message': message.message} for message in messages]

        return JsonResponse({'messages': messages_list})

    except Exception as e:
        # Log the exception for further investigation
        print(f"Exception in get_latest_messages: {e}")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


    