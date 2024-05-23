from django.urls import path, register_converter
from converters import (DateConverter, YearMonthConverter)
from .views import (
    create_post,
    update_post,
    get_posts,
    get_report,
    get_reports,
    get_week_report,
    PostViewSet
    )

register_converter(DateConverter, "date")
register_converter(YearMonthConverter, "year-month")
post_detail = PostViewSet.as_view({
    "get": "retrieve",
    "delete": "destroy"
})

urlpatterns = [
    path('posts/create', create_post, name="create-post"),
    path('posts/update/<int:pk>', update_post, name="update-post"),
    path("posts/<date:date>", get_posts, name="get-posts"),
    path("posts/<int:pk>", post_detail, name="post-detail"),
    path("reports/<date:date>", get_report, name="get-report"),
    path("reports/<year-month:date>", get_reports, name="get-reports"),
    path("reports/week/<date:start>", get_week_report, name="get-week-report"),
]