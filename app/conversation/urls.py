from django.urls import path, register_converter
from converters import (DateConverter, YearMonthConverter)
from .views import *

register_converter(DateConverter, "date")
register_converter(YearMonthConverter, "year-month")

urlpatterns = [
    path('posts/create', create_post, name="create-post"),
    path('posts/create/', create_post, name="create-post"),
    path('posts/update/<int:pk>', update_post, name="update-post"),
    path('posts/update/<int:pk>/', update_post, name="update-post"),
    path("posts/<date:date>", get_posts, name="get-posts"),
    path("posts/<date:date>/", get_posts, name="get-posts"),

    path("day/<date:date>", get_report, name="get-day"),
    path("day/<date:date>/", get_report, name="get-day"),
    path("day/<year-month:date>", get_reports, name="get-days"),
    path("day/<year-month:date>/", get_reports, name="get-days"),

    path("week/count/<date:start>", get_week_counts, name="get-week-count"),
    path("week/count/<date:start>/", get_week_counts, name="get-week-count"),
    path("week/mean/<date:start>", get_week_means, name="get-week-mean"),
    path("week/mean/<date:start>/", get_week_means, name="get-week-mean"),
    path("week/var/<date:start>", get_week_variances, name="get-week-variance"),
    path("week/var/<date:start>/", get_week_variances, name="get-week-variance"),

    path("dummy/<year-month:date>", create_dummy_data, name="create-dummy"),
]