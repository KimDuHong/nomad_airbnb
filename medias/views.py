from rest_framework.views import APIView
from .models import Photo
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class PhotoDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if photo.room.owner != request.user:
            raise PermissionDenied
        elif photo.experience:
            if photo.experience.host != request.user:
                raise PermissionDenied
        photo.delete()
        return Response(status=201)
