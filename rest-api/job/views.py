from rest_framework import viewsets, permissions, filters
from .models import Job
from .serializers import JobSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  
    filter_backends = [filters.SearchFilter]   
    search_fields = ['name']  


