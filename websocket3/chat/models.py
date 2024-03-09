from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Chat(models.Model):
	# hold the reference to the user who authored the message
	#ForeignKey is a field type in Django used to define many-to-one relationships https://docs.djangoproject.com/en/5.0/topics/db/examples/many_to_one/
	#User => model with which the foreign key relationship is established
	#related_name='author_message => defines the reverse relationship from the User model back to the Message mode
	#allows you to access messages authored by a specific user
	#specifies the behavior to adopt when the referenced object is deleted
	#CASCADE => all associated messages will also be deleted
	#If you don't specify related_name in ForeignKey(), when you access related obj you have to use default relate name "_set"
	#Ex. You have Message instance called "message" you can access related User instance by "message.user_set"
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

class ChatRoom(models.Model):
	name = models.TextField()

	# author = models.ForeignKey(User, related_name='author_msg', on_delete=models.CASCADE)
	# content = models.TextField()
	# username = models.TextField(null=True)
	# timestamp = models.DateTimeField(auto_now_add=True) #auto add timestamp

	# def __str__(self):
	# 	return self.author.get_username

	#function to load only last 10 msg order in reverse order(most recent time first)
	# def last_10_messages(self):
	# 	return Message.objects.order_by('-timestamp').all[:10]
