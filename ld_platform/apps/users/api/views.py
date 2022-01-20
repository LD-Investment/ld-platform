from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from ld_platform.apps.bots.models import SubscribedBot

from .serializers import UserProfileSerializer, UserSubscribedBotSerializer

User = get_user_model()


class UserProfileViewSet(RetrieveAPIView):
    """This endpoint is used to check whether requester is authenticated with its
    httpOnly JWT cookie"""

    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


class UserSubscribedBotViewSet(ListAPIView):
    serializer_class = UserSubscribedBotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SubscribedBot.objects.filter(user=user)
