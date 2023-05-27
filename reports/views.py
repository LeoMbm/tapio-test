from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.services import ReportService, SourceService
from core.entities import Report, Source
from reports.serializers import ReportSerializer, SourceSerializer, SourceDetailsSerializer


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

    def get(self, request, *args, **kwargs):
        report_service = ReportService()
        year_query = request.query_params.get('year')
        message = {}
        if year_query:
            try:
                year_query = int(year_query)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid year'})
            reports = report_service.get_reports_by_year(str(year_query))
            message['details'] = f'Reports from {year_query}'
        elif request.query_params.get('from_year') and request.query_params.get('to_year'):
            reports = report_service.get_reports_by_date_range(request.query_params['from_year'],
                                                               request.query_params['to_year'])
            message['details'] = f'Reports from {request.query_params["from_year"]} to {request.query_params["to_year"]}'
        else:
            reports = report_service.get_all_reports()
        serializer = self.serializer_class(reports, many=True)
        message['data'] = serializer.data
        return Response(message, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        message = {}
        if serializer.is_valid():
            report_service = ReportService()
            report_to_create = Report(name=serializer.validated_data['name'], date=serializer.validated_data['date'])
            created_report = report_service.create_report(report_to_create)
            message['id'] = created_report.id
            message['message'] = 'Report created successfully'
            message['data'] = serializer.data
            return Response(message, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportDetailDeleteUpdateView(APIView):
    serializer_class = ReportSerializer

    def get(self, request, pk):
        """
        Get report with amortized emissions or by id if year is not provided
        :param request:
        :param pk:
        :return:
        """
        report_service = ReportService()
        year = request.query_params.get('year')
        result = report_service.get_report_with_amortized_emissions(pk, year)
        if result is not None:
            report, message, sources = result
            if report is None:
                return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Report not found'})
            serializer = self.serializer_class(report)
            message['data'] = serializer.data
            if sources:
                sources_serializer = SourceDetailsSerializer(sources, many=True)
                message['data']['sources'] = sources_serializer.data
            return Response(message, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Report not found'})


    def delete(self, request, pk):
        report_service = ReportService()
        if report_service.delete_report(pk):
            return Response(status=status.HTTP_204_NO_CONTENT, data={'message': 'Report deleted'})
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Report not found'})

    def put(self, request, pk):
        report_service = ReportService()
        report = report_service.get_report_by_id(pk)
        name = request.data.get('name', report.name)
        date = request.data.get('date', report.date)
        report_to_update = Report(name=name, date=date)
        serializer = self.serializer_class(report, data=request.data, partial=True)
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
        if sources is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'No source has been created yet'})
        serializer = self.serializer_class(sources, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            source_service = SourceService()
            report_service = ReportService()
            report_id = None
            if request.data.get('report'):
                report_id = request.data['report']
                report = report_service.get_report_by_id(report_id)
                if not report:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid report ID'})
            source_to_create = Source(**serializer.validated_data)
            total_emission = source_to_create.value * source_to_create.emission_factor
            source_to_create.total_emission = total_emission
            created_source = source_service.create_source(source_to_create)
            serializer.data[
                'total_emission'] = total_emission
            data = {'data': serializer.data, 'emission_with_calcul': total_emission,
                    "emission_without_calcul": total_emission, "formula": "value * emission_factor",
                    'id': created_source.id}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SourceDetailDeleteUpdate(APIView):
    serializer_class = SourceSerializer

    def get(self, request, pk):
        source_service = SourceService()
        source = source_service.get_source_by_id(pk)
        message = {}
        if source is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Source not found'})
        year = request.query_params.get('year')
        if year:
            try:
                year = int(year)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid year'})
            if year >= source.acquisition_year:
                years_passed = year - source.acquisition_year
                lifetime = source.lifetime
                message['years_passed'] = years_passed
                message['remaining_time'] = lifetime - years_passed
                if years_passed >= lifetime:
                    source.total_emission = 0.0
                    message['amortized_emission'] = 0.0
                    message['gameover'] = 'Source lifetime is over'
                else:
                    amortized_emission = source.total_emission * (1 - years_passed / lifetime)
                    source.total_emission = round(amortized_emission, 2)
                    message['amortized_emission'] = amortized_emission
        serializer = self.serializer_class(source)
        message['data'] = serializer.data
        return Response(message, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        source_service = SourceService()
        if source_service.delete_source(pk):
            return Response(status=status.HTTP_204_NO_CONTENT, data={'message': 'Source deleted'})
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Source not found'})

    def put(self, request, pk):
        source_service = SourceService()
        source = source_service.get_source_by_id(pk)
        message = {}
        if source is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Source not found'})
        original_total_emission = source.total_emission
        if 'modifications' in request.data and request.data['modifications']:
            modifications = request.data['modifications']
            for modification in modifications:
                if 'ratio' in modification:
                    ratio = float(modification['ratio'])
                    source.value = source.value * ratio
                    message['plan_modification'] = {
                        'message': 'Value updated',
                        'new_value': source.value,
                        'ratio': ratio,
                        'formula': 'value * ratio'
                    }
                if 'emission_factor' in modification:
                    source.emission_factor = float(modification['emission_factor'])
                    source.total_emission = source.value * source.emission_factor
                    message['emission_factor_modification'] = {
                        'message': 'Emission factor updated',
                        'new_emission_factor': source.emission_factor,
                        'new_total_emission': source.total_emission,
                        'formula': 'value * emission_factor'
                    }
                message['list_of_modifications'] = modifications

        lifetime = source.lifetime
        years_elapsed = datetime.now().year - source.acquisition_year
        if years_elapsed >= lifetime:
            source.total_emission = 0.0
            message['total_emission'] = source.total_emission
            message['lifetime'] = 'Lifetime exceeded'
        else:
            average_annual_emission = source.total_emission / lifetime
            amortized_emission = average_annual_emission * years_elapsed
            source.total_emission -= amortized_emission
            message['average_annual_emission'] = average_annual_emission
            message['amortized_emission'] = source.total_emission
            message['total_emission'] = source.total_emission
            message['lifetime'] = 'Lifetime not exceeded'
        serializer = self.serializer_class(source, data=request.data, partial=True)
        if serializer.is_valid():
            updated_source = source_service.update_source(pk, source)
            serializer.data['id'] = updated_source.id
            message['data'] = serializer.data
            delta_total_emission = source.total_emission - original_total_emission
            message['delta_total_emission'] = delta_total_emission
            message['total_emission'] = source.total_emission
            return Response(message, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

