from django.shortcuts import render
from rest_framework.views import APIView
from .models import Experience, Perk
from .serializers import PerkSerializer
from rest_framework.response import Response

# Create your views here.


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)


class PerkDetail(APIView):
    def get_object(self, request):
        pass

    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
