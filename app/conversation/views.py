import os
import calendar
import datetime
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post, DayReport
from .serializers import PostSerializer, DayReportSerializer

from .functions.keyword_extraction import *
from .functions.emotion_classification import *
from constant.conversation import *

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_post(request):
    try:
        serializer = PostSerializer()
        post = serializer.create(request.user.family_id)

        response_data = {"id": post.id}
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        response_data = {'error': str(e)}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_post(request, pk):
    try:
        postSerializer = PostSerializer()
        post = Post.objects.get(pk=pk)

        keyword = [("안녕"),  ("반가워"), ("오랜만이네")]
        emotion = [[0.1, 0.2, 0.3, 0.4]]
        # keyword = keyword_extraction()
        # print(keyword)
        # emotion = emotion_classification(AUDIO_INPUT_WAV_PATH)
        # print(emotion)
        # os.remove(TEXT_PATH)
        # os.remove(AUDIO_INPUT_WAV_PATH)
        # os.remove(AUDIO_INPUT_WEBM_PATH)
        # os.remove(AUDIO_OUTPUT_PATH)
        data = {
            "content": "content",
            "emotion": emotion,
            "keyword": keyword
        }
        # print(data)
        
        postSerializer.update(post=post, data=data)
        reportSerializer = DayReportSerializer()
        report = reportSerializer.get_or_create(family=request.user.family_id, date=post.date)
        report = reportSerializer.update(report=report, data=data, post=post)
        response_data = {"message": UPDATE_POST_MESSAGE}
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        response_data = {'error': str(e)}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_posts(request, date):
    try:
        queryset = Post.objects.filter(
            Q(family_id=request.user.family_id) &
            Q(date=date)
        )
        serializer = PostSerializer(queryset, many=True)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        response_data = {'error': str(e)}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_report(request, date):
    try:
        queryset = DayReport.objects.get(
            Q(family_id=request.user.family_id) &
            Q(date=date)
        )
        serializer = DayReportSerializer(queryset)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        response_data = {'error': str(e)}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_reports(request, date):
    try:
        queryset = DayReport.objects.filter(
            Q(family_id=request.user.family_id) &
            Q(date__year=date.year) &
            Q(date__month=date.month)
        )
        serializer = DayReportSerializer(queryset, many=True)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        response_data = {'error': str(e)}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
def createResponseData(option, date, values):
    data = {}
    data["date"] = date
    if option == "variance":
        data["variance"] = values
    elif option == "count" or option == "mean":
        for i in range(len(values)):
            key = f"emotion_{i}_{option}"
            value = values[i]
            data[key] = value
    return data
    
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_week_counts(request, start):
    try:
        response_data = []
        for i in range(7):
            date = start + datetime.timedelta(days=i)
            try:
                report = DayReport.objects.get(family_id=request.user.family_id, date=date)
                data = createResponseData("count", date, [report.emotion_0_count, report.emotion_1_count, report.emotion_2_count, report.emotion_3_count])
            except DayReport.DoesNotExist:
                data = createResponseData("count", date, [0, 0, 0, 0])
            response_data.append(data)
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        response_data = {'error': str(e)}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_week_means(request, start):
    try:
        response_data = []
        for i in range(7):
            date = start + datetime.timedelta(days=i)
            try:
                report = DayReport.objects.get(family_id=request.user.family_id, date=date)
                data = createResponseData("mean", date, [report.emotion_0_mean, report.emotion_1_mean, report.emotion_2_mean, report.emotion_3_mean])
            except DayReport.DoesNotExist:
                data = createResponseData("mean", date, [0, 0, 0, 0])
            response_data.append(data)
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        response_data = {'error': str(e)}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_week_variances(request, start):
    try:
        response_data = []
        for i in range(7):
            date = start + datetime.timedelta(days=i)
            posts = Post.objects.filter(
                Q(family_id=request.user.family_id) &
                Q(date=date)
            )
            try:
                report = DayReport.objects.get(family_id=request.user.family_id, date=date)
                deviation = [0, 0, 0, 0]
                for post in posts:
                    deviation[0] += (post.emotion_0 - report.emotion_0_mean) ** 2
                    deviation[1] += (post.emotion_1 - report.emotion_1_mean) ** 2
                    deviation[2] += (post.emotion_2 - report.emotion_2_mean) ** 2
                    deviation[3] += (post.emotion_3 - report.emotion_3_mean) ** 2
                variance = sum(deviation) / report.post_count / 4
                data = createResponseData("variance", date, variance)
            except DayReport.DoesNotExist:
                data = createResponseData("variance", date, 0)
            response_data.append(data)
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        response_data = {'error': str(e)}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_dummy_data(request, date):
    try:
        _, days = calendar.monthrange(date.year, date.month)
        postSerializer = PostSerializer()
        reportSerializer = DayReportSerializer()
        for day in range(1, days + 1):
            temp_date = f"{date.year}-{date.month}-{day}"
            report = reportSerializer.get_or_create(family=request.user.family_id, date=temp_date)
            for i in range(3):
                random_numbers = np.random.dirichlet(np.ones(4), size=1)
                data = {
                    "date": temp_date,
                    "emotion": random_numbers,
                    "keyword": "BTS 봉준호 손흥민",
                    "content": "content",
                }
                post = postSerializer.createDummy(request.user.family_id, data)
                report = reportSerializer.update(report=report, data=data, post=post)
        response_data = {"message": UPDATE_POST_MESSAGE}
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        response_data = {'error': str(e)}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]