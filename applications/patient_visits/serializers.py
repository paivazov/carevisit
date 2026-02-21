from __future__ import annotations

from rest_framework import serializers

from applications.patient_visits.models import DutyResult, Visit


class DutyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DutyResult
        fields = ('id', 'duty', 'status')
        read_only_fields = ('id',)


class VisitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ('id', 'number', 'caregiver', 'patient', 'start_date_time', 'end_date_time', 'status', 'description')


class VisitDetailSerializer(serializers.ModelSerializer):
    duty_results = DutyResultSerializer(many=True, read_only=True)

    class Meta:
        model = Visit
        fields = (
            'id',
            'number',
            'caregiver',
            'patient',
            'start_date_time',
            'end_date_time',
            'status',
            'duty_results',
            'description'
        )


class VisitCreateUpdateSerializer(serializers.ModelSerializer):
    duty_results = DutyResultSerializer(many=True, required=False)

    class Meta:
        model = Visit
        fields = (
            'number',
            'caregiver',
            'patient',
            'start_date_time',
            'end_date_time',
            'status',
            'description',
            'duty_results'
        )
        read_only_fields = ('number',)

    def validate(self, attrs: dict) -> dict:
        start = attrs.get('start_date_time')
        end = attrs.get('end_date_time')
        if all((start, end, start >= end)):
            raise serializers.ValidationError({'end_date_time': 'end_date_time must be later than start_date_time.'})
        return attrs

    @staticmethod
    def validate_duty_results(value: list) -> list:
        if len(value) > 5:
            raise serializers.ValidationError('A visit cannot have more than 5 duties.')
        return value

    def create(self, validated_data: dict) -> Visit:
        duty_results_data = validated_data.pop('duty_results', [])
        visit = Visit.objects.create(**validated_data)
        self._add_duty_results(visit, duty_results_data)
        return visit

    def update(self, instance: Visit, validated_data: dict) -> Visit:
        duty_results = validated_data.pop('duty_results', None)
        if duty_results is not None:
            instance.duty_results.all().delete()
            self._add_duty_results(instance, duty_results)
        return super().update(instance, validated_data)

    @staticmethod
    def _add_duty_results(instance: Visit, duty_results: list) -> None:
        to_create = [DutyResult(visit=instance, **result) for result in duty_results]
        DutyResult.objects.bulk_create(to_create)


class CaregiverStatsSerializer(serializers.Serializer):
    unfinished_visits_count = serializers.IntegerField()
    unfinished_duties_count = serializers.IntegerField()
