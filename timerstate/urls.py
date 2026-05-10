from django.urls import path
from .views import (

    TimerStateListView,
    TimerStateDetailView,
    TimerStateCreateView,
    TimerStateUpdateView,
    TimerStateDeleteView,
)

app_name = "timer"

urlpatterns = [

    path(
        "timer-states/",
        TimerStateListView.as_view(),
        name="timer_state_list"
    ),

    path(
        "timer-states/create/",
        TimerStateCreateView.as_view(),
        name="timer_state_create"
    ),

    path(
        "timer-states/<int:pk>/",
        TimerStateDetailView.as_view(),
        name="timer_state_detail"
    ),

    path(
        "timer-states/<int:pk>/update/",
        TimerStateUpdateView.as_view(),
        name="timer_state_update"
    ),

    path(
        "timer-states/<int:pk>/delete/",
        TimerStateDeleteView.as_view(),
        name="timer_state_delete"
    ),
]