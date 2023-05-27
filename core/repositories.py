from typing import List

from django.db.models import Sum

from reports.models import ReportModel, SourceModel
from .entities import Report, Source


class ReportRepository:

    def create_report(self, report: Report) -> Report:
        report_created = ReportModel.objects.create(name=report.name, date=report.date)
        report._id = report_created.id
        return report

    def get_all_reports(self) -> List[Report]:
        report_models = ReportModel.objects.all()
        reports = []
        for report_model in report_models:
            report = Report(name=report_model.name, date=report_model.date, _id=report_model.id)
            reports.append(report)
        return reports

    def get_report_with_amortized_emissions(self, report_id, year=None):
        report = ReportModel.objects.filter(id=report_id).prefetch_related('sources').first()
        message = {}
        sources = []
        if report:
            sources = report.sources.all()
            if not sources:
                message['sources'] = 'No sources found for this report'
                return report, message, sources
            if year:
                try:
                    year = int(year)
                except ValueError:
                    raise ValueError("Invalid year")

                for source in sources:
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
            total_emission_report = sources.aggregate(total_emissions=Sum('total_emission'))['total_emissions']
            message['total_emission_report'] = total_emission_report
            return report, message, sources

        return None

    def get_reports_by_year(self, year: str) -> List[Report]:
        report_models = ReportModel.objects.filter(date__year=year)
        reports = []
        for report_model in report_models:
            report = Report(name=report_model.name, date=report_model.date, _id=report_model.id)
            reports.append(report)
        return reports

    def get_reports_by_date_range(self, start_date: str, end_date: str) -> List[Report]:
        report_models = ReportModel.objects.filter(date__year__range=[start_date, end_date])
        reports = []
        for report_model in report_models:
            report = Report(name=report_model.name, date=report_model.date, _id=report_model.id)
            reports.append(report)
        return reports

    def get_report_by_id(self, report_id: int) -> Report:
        try:
            report_model = ReportModel.objects.get(id=report_id)
            if report_model:
                report = Report(name=report_model.name, date=report_model.date, _id=report_model.id)
                return report
        except ReportModel.DoesNotExist:
            return None

    def update_report(self, report_id, report: Report) -> Report:
        report_model = ReportModel.objects.get(pk=report_id)
        if not report_model:
            return False
        report_model.name = report.name
        report_model.date = report.date
        report_model.save()
        return report

    def delete_report(self, report_id: int) -> bool:
        report = ReportModel.objects.filter(pk=report_id)
        if report:
            report.delete()
            return True
        return False


class SourceRepository:
    def create_source(self, source: Source) -> Source:

        return SourceModel.objects.create(
            report=source.report,
            description=source.description,
            value=source.value,
            emission_factor=source.emission_factor,
            total_emission=source.total_emission,
            lifetime=source.lifetime,
            acquisition_year=source.acquisition_year
        )

    def get_source_by_id(self, source_id: int):
        try:
            return SourceModel.objects.get(id=source_id)
        except SourceModel.DoesNotExist:
            return None

    def get_all_sources(self) -> List[Source]:
        source_models = SourceModel.objects.select_related('report').all()
        sources = []
        for source_model in source_models:
            source = Source(
                report=source_model.report,
                description=source_model.description,
                value=source_model.value,
                emission_factor=source_model.emission_factor,
                total_emission=source_model.total_emission,
                lifetime=source_model.lifetime,
                acquisition_year=source_model.acquisition_year,
                _id=source_model.id
            )
            sources.append(source)
        return sources

    def update_source(self, source_id, source: Source) -> Source:
        try:
            source_model = SourceModel.objects.get(pk=source_id)
            if not source_model:
                return False
            source_model.description = source.description
            source_model.value = source.value
            source_model.emission_factor = source.emission_factor
            source_model.total_emission = source.total_emission
            source_model.lifetime = source.lifetime
            source_model.acquisition_year = source.acquisition_year
            source_model.save()
            return source
        except SourceModel.DoesNotExist:
            return None

    def delete_source(self, source_id: int) -> bool:
        try:
            SourceModel.objects.filter(pk=source_id).delete()
            return True
        except Exception as e:
            print("Error deleting")
            return False
