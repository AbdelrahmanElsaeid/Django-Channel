from django.db import models

from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    online = models.ManyToManyField(to=User, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images', default='images/d.jpg', blank=True, null=True)  


    def __str__(self):
        return self.name
    
    def get_messages(self):
        return self.message_room.all()
    
    def get_count_member(self):
        return self.online.count()



class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_user')
    room = models.ForeignKey(ChatRoom, related_name='message_room', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room.name + ' - ' + self.user.username + ' - ' + self.message 


   