from rest_framework import generics
from .models import Link, LinkSerializer


class LinkCreateView(generics.CreateAPIView):
    serializer_class=LinkSerializer

class LinkRetrieve(generics.RetrieveAPIView):
    serializer_class=LinkSerializer
    queryset=Link.objects.all()