from django.shortcuts import render, redirect
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.services import ReportService, SourceService
from core.entities import Report, Source
from reports.serializers import ReportSerializer, SourceSerializer


class HomeView(APIView):
    def get(self, request):
        message = {
            'case': 'Tapio Backend Challenge',
            'text': "I hope you like it!",
            'details': 'i was trying to implement a clean architecture, i hope you can give me some feedback about it, thanks!'
        }
        return Response(status=status.HTTP_200_OK, data=message)


class ReportListCreateView(APIView):
    serializer_class = ReportSerializer

    def get(self, request):
        report_service = ReportService()
        reports = report_service.get_all_reports()
        serializer = self.serializer_class(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            report_service = ReportService()
            report_to_create = Report(name=serializer.validated_data['name'], date=serializer.validated_data['date'])
            created_report = report_service.create_report(report_to_create)
            serializer.data['id'] = created_report.id
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportDetailDeleteUpdateView(APIView):
    serializer_class = ReportSerializer
    def get(self, request, pk):
        report_service = ReportService()
        report = report_service.get_report_by_id(pk)
        if report is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Report not found'})
        serializer = self.serializer_class(report)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        report_service = ReportService()
        if report_service.delete_report(pk):
            return Response(status=status.HTTP_204_NO_CONTENT, data={'message': 'Report deleted'})
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Report not found'})

    def put(self, request, pk):
        report_service = ReportService()
        report_to_update = Report(name=request.data['name'], date=request.data['date'])
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            updated_report = report_service.update_report(pk, report_to_update)
            serializer.data['id'] = updated_report.id
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SourceListCreateView(APIView):

    serializer_class = SourceSerializer

    def get(self, request):
        source_service = SourceService()
        sources = source_service.get_all_sources()
        print(sources)
        if sources is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'No source has been created yet'})
        serializer = self.serializer_class(sources, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            source_service = SourceService()
            source_to_create = Source(**serializer.validated_data)
            total_emission = source_to_create.value * source_to_create.emission_factor
            source_to_create.total_emission = total_emission
            created_source = source_service.create_source(source_to_create)
            serializer.data['id'] = created_source.id
            serializer.data['total_emission'] = created_source.total_emission
            data = {
                'data': serializer.data,
                'emission_with_calcul':  total_emission,
                "emission_without_calcul": serializer.data['total_emission'],
                "formula": "value * emission_factor"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
