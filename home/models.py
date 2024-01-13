from django.db import models
from django.contrib.auth.models import User

class Messages(models.Model):
    sender = models.ForeignKey(User , on_delete = models.CASCADE , related_name='sender')
    receiver = models.ForeignKey(User , on_delete=models.CASCADE , related_name='receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} || {self.receiver} || {self.message}"
    


# try to implement the add friend functionality
# make user's able to search for other users with ajax so no page reload
# make another page for chat section where user's will be chatting