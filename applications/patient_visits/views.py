from __future__ import annotations # todo: rm when not needed

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.patient_visits.filters import VisitFilter
from applications.patient_visits.models import DutyResult, Visit
from applications.patient_visits.serializers import (
    CaregiverStatsSerializer,
    VisitCreateUpdateSerializer,
    VisitDetailSerializer,
    VisitListSerializer,
)


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.without_deleted().prefetch_related('duties')
    filterset_class = VisitFilter
    ordering_fields = ['start_date_time', 'end_date_time', 'status', 'number']
    ordering = ['-start_date_time']

    def get_serializer_class(self):
        if self.action == 'list':
            return VisitListSerializer
        if self.action == 'caregiver_stats':
            return CaregiverStatsSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return VisitCreateUpdateSerializer
        return VisitDetailSerializer

    def destroy(self, request, *args, **kwargs):
        visit = self.get_object()
        if visit.status == Visit.Status.COMPLETED:
            visit.is_deleted = True
            visit.save(update_fields=['is_deleted'])
        else:
            visit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='caregiver-stats')
    def caregiver_stats(self, request):
        caregiver = request.user
        unfinished_statuses = [Visit.Status.SCHEDULED, Visit.Status.IN_PROGRESS]

        unfinished_visits_count = Visit.objects.filter(
            caregiver=caregiver,
            status__in=unfinished_statuses,
        ).count()

        unfinished_duties_count = DutyResult.objects.filter(
            visit__caregiver=caregiver,
            status=DutyResult.Status.NOT_DONE,
            visit__status__in=unfinished_statuses,
        ).count()

        serializer = self.get_serializer({
            'unfinished_visits_count': unfinished_visits_count,
            'unfinished_duties_count': unfinished_duties_count,
        })
        return Response(serializer.data)
