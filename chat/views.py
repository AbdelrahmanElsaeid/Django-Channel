from django.shortcuts import render
from .models import ChatRoom, Messages


# Create your views here.




def index(request):
    rooms = ChatRoom.objects.all()
    return render(request, 'index.html', {"rooms": rooms})



def room(request, room_name):
    room, _ = ChatRoom.objects.get_or_create(name=room_name)
    room.online.add(request.user)
    room.save()

    rooms = ChatRoom.objects.filter(online=request.user)

    # Get all messages for this chatroom

    messages = room.get_messages()     

    context = {
        "room_name": room_name,
        "room": room,
        "rooms":rooms,
        "messages": messages,
        }

    return render(request, "room.html", context) 