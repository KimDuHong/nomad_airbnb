from django.utils import timezone
from rest_framework import serializers
from .models import Booking
import datetime


class PublicBookingSerializer(serializers.ModelSerializer):
    is_past = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = (
            "pk",
            "kind",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
            "is_past",
        )

    def get_is_past(self, obj):
        now = timezone.localtime(timezone.now()).date()
        compare_time = (obj.experience_time + timezone.timedelta(hours=9)).date()
        if now > compare_time:
            return True
        else:
            return False


# check_in and check_out want to requried fields
class CreateRoomBookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    # is_valid() 실행시 같이 실행하는 메소드, 특정 필드 체크용
    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if value < now:
            raise serializers.ValidationError("체크인 시간 에러")
        else:
            return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if value < now:
            raise serializers.ValidationError("체크아웃 시간 에러")
        else:
            return value

    # 특정 필드가 아닌 validator 자체에서 띄우는 에러
    def validate(self, value):
        room = self.context.get("room")
        if room:
            if value["check_in"] >= value["check_out"]:
                raise serializers.ValidationError("체크아웃이 체크인보다 빠릅니다.")
            if Booking.objects.filter(
                room=room,
                check_in__lte=value["check_out"],
                check_out__gte=value["check_in"],
            ).exists():
                raise serializers.ValidationError("Reservation Allready.")
            return value
        else:
            raise serializers.ValidationError("Error")


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    experience_time = serializers.DateTimeField()

    class Meta:
        model = Booking
        fields = ("experience_time", "guests")

    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now())
        if value < now:
            raise serializers.ValidationError("이미 지났습니다.")
        else:
            return value
