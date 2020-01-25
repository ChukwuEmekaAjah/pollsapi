from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Poll
# Create your views here.

def polls_list(request):
	MAX_OBJECTS = 20
	polls = Poll.objects.all()[:MAX_OBJECTS]
	data = {"results":list(polls.values("question","create_by__id", "pub_date"))}
	return JsonResponse(data)

def polls_detail(request, pk):
	poll = get_object_or_404(Poll, pk=pk)
	print(poll)
	data = {"results": {
		"question":poll.question,
		"pub_date":poll.pub_date,
		"created_by":poll.create_by.username
	}}
	return JsonResponse(data)

