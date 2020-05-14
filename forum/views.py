from django.shortcuts import render, redirect
from forum.models import Topic, DiscussionThread, ThreadResponse, FORUM_TOPICS, FORUM_TOPIC_DESCRIPTION, FORUM_URL
from forum.forms import DiscussionThreadForm, ThreadResponseForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# User forum boards
# Each board contains a separate topic.
@login_required(login_url="/login")
def forum_boards_list(request):
	forum_topics = []
	idx = 0
	for topic in FORUM_TOPICS:
		forum_topics.append( (topic[1], FORUM_TOPIC_DESCRIPTION[idx], FORUM_URL[idx]) )
		idx += 1
	data = {
		"title":"Forum",
		"forum_topics":forum_topics
	}
	#DiscussionThread.objects.all().delete()
	print(DiscussionThread.objects.all().values())
	return render(request, "forum/forum.html", data)
	
@login_required(login_url="/login")
def forum_newpost(request, topic):
	if (topic == "general"):
		form_topic = "gen"
	if (topic == "strategy"):
		form_topic = "strat"
	if (topic == "site-suggestions"):
		form_topic = "sitesug"
	if (topic == "other"):
		form_topic = "other"

	errors = ""

	if request.method == "POST":
		post_data = request.POST
		form = DiscussionThreadForm(request.POST)
		if form.is_valid():
			form.save(request.user)
			redirstring = "/forum/board/{}".format(topic)
			return redirect(redirstring)
		else:
			errors = form.errors

	form = DiscussionThreadForm(initial={"topic":form_topic})
	
	data = {
		"title":"New Thread",
		"post_topic":topic,
		"form":form,
		"errors":errors
	}
	return render(request, "forum/newthread.html", data)


@login_required(login_url="/login")
def forum_board(request, board):
	# Generate a table entry for this topic if it does not already exist.
	topic_field_str = ""

	if board == "general":
		topic_field_str = "gen"
	elif board == "strategy":
		topic_field_str = "strat"
	elif board == "site-suggestions":
		topic_field_str = "sitesug"
	elif board == "other":
		topic_field_str = "other"
	
	topic = Topic.objects.filter(type=topic_field_str)
	print(topic.count())

	if (topic.count() == 0):
		topic = Topic(type = topic_field_str)
		topic.save()
	
	topic = Topic.objects.get(type=topic_field_str)
	
	threads = DiscussionThread.objects.filter(posted_under=topic)

	if board == "general":
		data = {
			"title":"Forum - General",
			"forum_topic":FORUM_TOPICS[0][1],
			"topic_description":FORUM_TOPIC_DESCRIPTION[0],
			"new_thread_topic":"general",
			"forum_board":"general"
		}
	elif board == "strategy":
		data = {
			"title":"Forum - Strategy",
			"forum_topic":FORUM_TOPICS[1][1],
			"topic_description":FORUM_TOPIC_DESCRIPTION[1],
			"new_thread_topic":"strategy",
			"forum_board":"strategy"
		}
	elif board == "site-suggestions":
		data = {
			"title":"Forum - Site Suggestions",
			"forum_topic":FORUM_TOPICS[2][1],
			"topic_description":FORUM_TOPIC_DESCRIPTION[2],
			"new_thread_topic":"site-suggestions",
			"forum_board":"site-suggestions"
		}
	elif board == "other":
		data = {
			"title":"Forum - Other",
			"forum_topic":FORUM_TOPICS[3][1],
			"topic_description":FORUM_TOPIC_DESCRIPTION[3],
			"new_thread_topic":"other",
			"forum_board":"other"
		}
	thread_data = []

	# <QuerySet [{'id': 1, 'title': 'fasdfdfasadsf', 'posted_under_id': 1, 'user_id': 2, 'paragraph': 'dfasasdfasdfasdfasdf'}]>
	for thread in threads:
		# Go through thread data, and create tuple(s) accordingly
		thread_data.append(
			(thread.title, User.objects.get(id = thread.user_id), thread.id)
		)

	data["threads"] = thread_data
	
	return render(request, "forum/forumboard.html", data)

def view_thread(request, board, thread_id):
	# Get the table entry for this topic, since it likely already exists.
	topic_field_str = ""

	if board == "general":
		topic_field_str = "gen"
	elif board == "strategy":
		topic_field_str = "strat"
	elif board == "site-suggestions":
		topic_field_str = "sitesug"
	elif board == "other":
		topic_field_str = "other"
	
	topic = Topic.objects.get(type=topic_field_str)
	
	thread = DiscussionThread.objects.all().filter(posted_under=topic, id = thread_id)
	
	# There should only be one thread with this id posted under this topic. Every thread has a unique id.
	if (thread.count() == 1):
		errors = ""
		# If the user has sent a post request, we now have to apply that reply to this thread.
		if request.method == "POST":
			response_form = ThreadResponseForm(request.POST)
			if response_form.is_valid():
				response_form.save(request.user, DiscussionThread.objects.get(id=thread_id))
				redirect_url = "/forum/board/{0}/{1}".format(board, thread_id)
				return redirect(redirect_url)
			else:
				errors = form.errors
		# Get thread data
		thread_data = DiscussionThread.objects.get(posted_under=topic, id = thread_id)
		thread_title = thread_data.title
		thread_posted_by = User.objects.get(id = thread_data.user_id)
		thread_content = thread_data.paragraph
		# Also all relevant reply data
		thread_responses = ThreadResponse.objects.all().filter(thread = thread_id)
		if (thread_responses.count() > 0):
			thread_responses_data = ThreadResponse.objects.filter(thread = thread_id)
			responses = []
			for response in thread_responses_data:
				responses.append(
					(
						response.user,
						response.paragraph
					)
				)
		else:
			responses = None

		thread_response_form = ThreadResponseForm()

		data = {
			"title":"View thread: {}".format(thread_title),
			"thread_title":thread_title,
			"thread_posted_by":thread_posted_by,
			"thread_content":thread_content,
			"board":board,
			"thread_id":thread_id,
			"thread_response_form":thread_response_form,
			"thread_responses":responses,
			"current_user":User.objects.get(id = request.user.id),
			"errors":errors
		}
		return render(request, "forum/viewthread.html", data)
	else:
		return redirect("/404")