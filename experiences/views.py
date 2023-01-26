from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Perk, Experience
from .serializers import (
    PerkSerializer,
    ExperienceSerializer,
    ExperienceDetailSerializer,
)
from categories.models import Category
from django.conf import settings
from bookings.models import Booking
from bookings.serializers import (
    PublicBookingSerializer,
    CreateRoomBookingSerializer,
    CreateExperienceBookingSerializer,
)
from django.utils import timezone


# Create your views here.


class Experiences(APIView):
    def get(self, request):
        all_experience = Experience.objects.all()
        serializer = ExperienceSerializer(all_experience, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Invalid category")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.ROOMS:
                        raise ParseError("The category kind should be 'experiences'")
                except Category.DoesNotExist:
                    raise ParseError("Category Not Found")
                experience = serializer.save(
                    host=request.user,
                    category=category,
                )
                perks = request.data.get("perks")

                if not isinstance(perks, list):
                    if perks:
                        raise ParseError("Perks_pk must be a list")
                    else:
                        raise ParseError("Perks are null")
                try:
                    for pk in perks:
                        perk = Perk.objects.get(pk=pk)
                        experience.perks.add(perk)
                except Perk.DoesNotExist:
                    raise ParseError("Perk Not Found")

                return Response(ExperienceSerializer(experience).data)
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):

    permission_classes = [IsAuthenticated]

    def is_negative(self, value):
        if value:  # check None value
            if value < 0:
                return True
        return False

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(experience)
        return Response(serializer.data)

    def put(self, request, pk):
        if request.data.get("host"):
            raise ParseError("CANNOT UPDATE HOST")
        expereince = self.get_object(pk)
        if request.user != expereince.host:
            raise PermissionDenied  # 권한
        serializer = ExperienceDetailSerializer(
            expereince,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            price = request.data.get("price")
            if self.is_negative(price):
                raise ParseError("negative price")

            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.ROOMS:
                        raise ParseError("Must Be Experience")
                    expereince.category = category
                except Category.DoesNotExist:
                    raise ParseError("Invalid Category pk")

            perk_pk = request.data.get("perks")
            if perk_pk:
                if not isinstance(perk_pk, list):
                    raise ParseError("perk_pk must be a list")
                expereince.perks.clear()
                perk_pk = list(set(perk_pk))
                for pk in perk_pk:
                    try:
                        perk = Perk.objects.get(pk=pk)
                        expereince.perks.add(perk)
                    except Perk.DoesNotExist:
                        raise ParseError("Invalid Amenity pk")

            update_experience = serializer.save()
            return Response(ExperienceDetailSerializer(update_experience).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        expereince = self.get_object(pk)
        if request.user != expereince.host:
            raise PermissionDenied
        expereince.delete()
        return Response(status=204)


class ExperiencePerk(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        experience = self.get_object(pk)
        serializer = PerkSerializer(
            experience.perks.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class ExperienceBooking(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            experience_time__gte=now,
        )
        serializer = PublicBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookingAll(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
        )
        serializer = PublicBookingSerializer(
            bookings[start:end],
            many=True,
        )
        return Response(serializer.data)


class ExperienceBookingDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_experience(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get_booking(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise NotFound

    def get(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)
        if booking.experience == self.get_experience(pk):
            return Response(PublicBookingSerializer(booking).data)
        else:
            raise ParseError("Wrong link")

    def put(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)

        if booking.user.pk != request.user.pk:
            raise PermissionDenied

        serializer = CreateExperienceBookingSerializer(
            booking,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            booking = serializer.save()
            serializer = PublicBookingSerializer(booking)

            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk, booking_pk):

        booking = self.get_booking(booking_pk)

        if booking.user.pk != request.user.pk:
            raise PermissionDenied

        booking.delete()

        return Response(status=204)


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
