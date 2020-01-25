from django.urls import path
from .views import polls_list, polls_detail
from .apiviews import PollList, LoginView, UserCreate, PollDetail, ChoiceList, CreateVote

urlpatterns = [
	path("polls/", polls_list, name="polls_list"),
	path("polls/<int:pk>/", polls_detail, name="polls_detail"),
	path("api/polls/", PollList.as_view(), name="list_of_polls"),
	path("api/polls/<int:pk>/",PollDetail.as_view(), name="poll_detail"),
	path("api/polls/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
	path("api/polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),
	path("api/users/", UserCreate.as_view(), name="user_create"),
	path("api/login/", LoginView.as_view(), name="login"),
] 