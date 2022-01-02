from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .serializers import UserProfileSerializer

User = get_user_model()


class UserProfileViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """This endpoint is used to check whether requester is authenticated with its
    httpOnly JWT cookie"""

    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj
