from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers

# A model to keep track of a user's total score.
# A player's total score is how many games they've won.
class PlayerScore(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	score = models.IntegerField(default=0)

class LeaderboardSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = PlayerScore
		fields = '__all__'