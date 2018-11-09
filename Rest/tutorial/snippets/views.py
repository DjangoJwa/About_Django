from snippets.models import Snippets
from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User

class SnippetList(generics.ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    """
    queryset = Snippets.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a code snippet.
    """
    queryset = Snippets.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class UserList(generics.ListAPIView):
    queryset = Snippets.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = Snippets.objects.all()
    serializer_class = UserSerializer