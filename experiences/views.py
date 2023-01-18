from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Experience, Perk
from .serializers import PerkSerializer

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
    def get_object(self, pk):
        try:
            perk = Perk.objects.get(pk=pk)
            return perk
        except Perk.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk, data=request.data)
        if serializer.is_valid():
            update_perk = serializer.save()
            return Response(PerkSerializer(update_perk).data)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=204)
