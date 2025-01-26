from django.db.models import Q, Case, When, Value
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Candidate
from .serializer import CandidateSerializer

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request, version=None):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({"results": []}, status=status.HTTP_400_BAD_REQUEST)

        query_words = query.lower().split()
        
        search_query = Q()
        for word in query_words:
            search_query |= Q(name__icontains=word)

        queryset = self.queryset.filter(search_query)

        relevancy_annotation = 0
        for word in query_words:
            relevancy_annotation += Case(
                When(Q(name__icontains=word), then=Value(1)),
                default=Value(0),
                output_field=models.IntegerField()
            )
        
        queryset = queryset.annotate(relevancy_score=relevancy_annotation).order_by('-relevancy_score')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
