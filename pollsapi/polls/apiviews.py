from rest_framework import generics, status
from rest_framework.response import Response 
from django.shortcuts import get_object_or_404 
from rest_framework.views import APIView 
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied 

from .models import Poll, Choice, Vote
from .serializers import PollSerializer, UserSerializer, ChoiceSerializer, VoteSerializer 

class PollList (generics.ListCreateAPIView):
	queryset = Poll.objects.all()
	serializer_class = PollSerializer

class PollDetail(generics.RetrieveDestroyAPIView):
	def get_queryset(self):
		queryset = Poll.objects.filter(id=self.kwargs['pk'])
		return queryset
	serializer_class = PollSerializer

	def destroy(self, request, *args, **kwargs):
		poll = Poll.objects.get(pk=self.kwargs["pk"])
		if not poll.create_by == request.user:
			raise PermissionDenied("You can not delete this poll")
		return super().destroy(request, *args, **kwargs)


class ChoiceList(generics.ListCreateAPIView):
	def get_queryset(self):
		queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
		return queryset
	serializer_class = ChoiceSerializer

	def post(self, request, *args, **kwargs):
		poll = Poll.objects.get(pk=self.kwargs["pk"])
		if not request.user == poll.create_by:
			raise PermissionDenied("You can not create a choice for this poll")
		return super().post(request, *args, **kwargs)

class CreateVote(generics.ListCreateAPIView):
	serializer_class = VoteSerializer
	def get_queryset(self):
		queryset = Vote.objects.filter(poll_id=self.kwargs['pk'], choice_id=self.kwargs['choice_pk'])
		return queryset
	def post(self, request, pk, choice_pk):
		voted_by = request.data.get("voted_by")
		data = {"choice":choice_pk, "poll":pk, 'voted_by':voted_by}
		serializer = VoteSerializer(data=data)
		if serializer.is_valid():
			vote = serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(generics.CreateAPIView):
	authentication_classes = ()
	permission_classes = ()
	serializer_class = UserSerializer

class LoginView(APIView):
	permission_classes = ()
	def post(self, request):
		username = request.data.get("username")
		password = request.data.get("password")
		user = authenticate(username=username, password=password)
		if user:
			return Response({"token":user.auth_token.key})
		else:
			return Response({"error":"Wrong credentials"}, status.HTTP_400_BAD_REQUEST)

