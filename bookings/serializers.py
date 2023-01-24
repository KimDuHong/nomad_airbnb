from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "kind",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )


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
        if value["check_in"] >= value["check_out"]:
            raise serializers.ValidationError("체크아웃이 체크인보다 빠릅니다.")
        if Booking.objects.filter(
            check_in__lte=value["check_out"],
            check_out__gte=value["check_in"],
        ).exists():
            raise serializers.ValidationError("Reservation Allready.")
        return value
