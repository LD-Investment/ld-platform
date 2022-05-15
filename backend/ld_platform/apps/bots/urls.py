from django.urls import path

app_name = "bots"

urlpatterns = [
    # Indicator Bot - General
    path("indicator"),
    # Indicator Bot - News Tracker
    path("indicator/news-tracker"),
    path("indicator/news-tracker/subscribe"),
    path("indicator/news-tracker/control/fetch-news"),
    path("indicator/news-tracker/control/model"),
    path("indicator/news-tracker/control/model/<int:id>"),
    path("indicator/news-tracker/control/model/<int:id>/calculate"),
]
