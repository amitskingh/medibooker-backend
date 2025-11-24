from rest_framework import serializers
from django.utils import timezone
from datetime import datetime
from .models import Slot


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ["id", "doctor", "date", "start_time", "end_time", "is_booked"]
        read_only_fields = ["doctor", "is_booked"]

    def validate(self, attrs):
        slot_date = attrs["date"]
        start = attrs["start_time"]
        end = attrs["end_time"]

        # 1. Start < End check
        if start >= end:
            raise serializers.ValidationError(
                {"time": "End time must be greater than start time."}
            )

        # 2. Combine date + time as aware datetime
        slot_start_dt = datetime.combine(slot_date, start)
        slot_start_dt = timezone.make_aware(slot_start_dt)

        now = timezone.localtime()

        # 3. Prevent creating past slots
        if slot_start_dt <= now:
            raise serializers.ValidationError(
                {"date": "Cannot create a slot in the past."}
            )

        return attrs
