from django.db import models
from django.contrib.auth.models import User
from core.models import UserSerializer
from rest_framework import serializers

# RPS Forum models

# Each topic that a thread can be posted under
'''
# As this is a Rock-Paper-Scissors discussion board, topics will be:
	- General
	- Strategy
	- Site suggestions
	- Other/Off-Topic (for memes and whatever else people want to post)
'''
FORUM_TOPICS = [
	('gen', 'General'),
	('strat', 'Strategy'),
	('sitesug', 'Site Suggestions'),
	('other', 'Other/Off-Topic')
]

FORUM_TOPIC_DESCRIPTION = [
	"A place to talk about all things Rock Paper Scissors.",
	"Discuss strategy: how to guarantee wins, or other approaches.",
	"Suggest features for this website.",
	"For things that either loosely relate to Rock Paper Scissors, or not at all."
]

FORUM_URL = [
	"general",
	"strategy",
	"site-suggestions",
	"other"
]

class Topic(models.Model):
	type = models.CharField(max_length=10, blank=True, null=True)

# Each board has a multitude of threads
class DiscussionThread(models.Model):
	# A thread has:
	# - a title
	title = models.CharField(
		max_length=500,
		default='New thread',
		blank=False
	)
	# - a topic it's listed under
	posted_under = models.ForeignKey(Topic, on_delete=models.CASCADE)
	# - a user who posted it
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	# - and some content (text)
	paragraph = models.CharField(
		max_length=10000,
		blank=False
	)

# Each thread has a multitude of responses
class ThreadResponse(models.Model):
	# This is the thread this reponse is attached to
	thread = models.ForeignKey(DiscussionThread, on_delete=models.CASCADE)
	# A user has posted this response
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	# And the response has some words in it
	# TODO: Users can edit their responses, but I'll need to indicate they've done so.
	paragraph = models.CharField(
		max_length=10000,
		blank=False
	)

class BoardCategorySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Topic
		fields = '__all__'

class ThreadSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		user = UserSerializer()
		model = DiscussionThread
		fields = '__all__'

class ThreadResponseSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		user = UserSerializer()
		model = ThreadResponse
		fields = '__all__'