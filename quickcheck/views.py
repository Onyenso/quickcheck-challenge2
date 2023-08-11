from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from quickcheck.serializers import (
    StorySerializer,
    JobSerializer,
    CommentSerializer,
    PollSerializer,
    PollOptSerializer,
    AllItemsSerializer
)
from quickcheck.permissions import IsOwnerOrReadOnly
from quickcheck.models import Story, Job, Comment, Poll, PollOpt, Base
from quickcheck.sync import sync_data
from config.pagination import CustomPagination


class AllItemsViewSet(viewsets.ModelViewSet):
    queryset = Base.objects.all()
    serializer_class = AllItemsSerializer
    template_name = "quickcheck/index.html"
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["type"]
    search_fields = ["job__title", "job__text", "story__title", "poll__title", "poll__text"]
    pagination_class = CustomPagination
    http_method_names = ["get"] # this view is read-only

    def list(self, request, *args, **kwargs):
        # apply filters
        self.queryset = self.filter_queryset(self.get_queryset())

        if request.accepted_renderer.format == 'json':
            # apply pagination and return JSON response
            page = self.paginate_queryset(self.queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            # apply pagination and return HTML response
            paginator = Paginator(self.queryset.filter(type__in=["story", "job", "poll"]), self.pagination_class.page_size)
            page_number = request.GET.get('page')
            try:
                data = paginator.page(page_number)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)

            # Calculate a range of page numbers for dynamic pagination links
            max_pages_to_display = 5
            current_page = data.number
            start_page = max(current_page - max_pages_to_display // 2, 1)
            end_page = min(start_page + max_pages_to_display, paginator.num_pages)

            return render(request, self.template_name, {'data': data, 'start_page': start_page, 'end_page': end_page})
    
    def retrieve(self, request, *args, **kwargs):
        # retrieve method to return only HTML response
        item = self.get_object()
        return render(request, "quickcheck/item.html", {'item': item})


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class PollOptViewSet(viewsets.ModelViewSet):
    queryset = PollOpt.objects.all()
    serializer_class = PollOptSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# scheduler = BackgroundScheduler()
# scheduler.add_job(func=sync_data, trigger="interval", seconds=5)
# scheduler.start()
# atexit.register(lambda: scheduler.shutdown())
