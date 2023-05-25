from typing import List
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
            report = Report(name=report_model.name, date=report_model.date, _id=report_model.id)
            return report
        except ReportModel.DoesNotExist:
            return {}


    def update_report(self, report_id, report: Report) -> Report:
        try:
            report_model = ReportModel.objects.get(pk=report_id)
            report_model.name = report.name
            report_model.date = report.date
            report_model.save()
            return report
        except ReportModel.DoesNotExist:
            return None


    def delete_report(self, report_id: int) -> bool:
        try:
            ReportModel.objects.filter(pk=report_id).delete()
            return True
        except Exception as e:
            print("Error deleting")
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
            return []


    def get_all_sources(self) -> List[Source]:
        source_models = SourceModel.objects.all()
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
