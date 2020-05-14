from django import forms
from forum.models import Topic, DiscussionThread, ThreadResponse, FORUM_TOPICS

class DiscussionThreadForm(forms.Form):
	topic = forms.ChoiceField(
		widget=forms.Select(
			attrs={
				"class":"form-control mb-2"
			}
		),
		choices=FORUM_TOPICS
	)
	title = forms.CharField(
		widget=forms.TextInput(
			attrs={
				"class":"form-control mb-2",
				"placeholder":"Title"
			}
		)
	)
	paragraph = forms.CharField(
		label = "",
		widget=forms.Textarea(
			attrs={
				"class":"form-control mb-2",
				"placeholder":"Type your post here..."
			}
		)
	)

	def save(self, user):
		newthread = DiscussionThread()
		# Create an entry for this topic if it does not exist.
		if (Topic.objects.filter(type=self.cleaned_data["topic"]).count() == 0):
			new_instance = Topic()
			new_instance.type = self.cleaned_data["topic"]
			new_instance.save()
		# Regardless, assign this topic to this thread.
		topic = Topic.objects.get(type=self.cleaned_data["topic"])
		newthread.posted_under = topic
		newthread.user = user
		newthread.title = self.cleaned_data["title"]
		newthread.paragraph = self.cleaned_data["paragraph"]
		newthread.save()

class ThreadResponseForm(forms.Form):
	content = forms.CharField(
		widget=forms.Textarea(
			attrs={
				"class":"form-control"
			}
		)
	)

	def save(self, user, thread):
		newresponse = ThreadResponse()
		newresponse.thread = thread
		newresponse.user = user
		newresponse.paragraph = self.cleaned_data["content"]
		newresponse.save()