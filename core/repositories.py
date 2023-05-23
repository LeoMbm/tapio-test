from reports.models import ReportModel
from .entities import Report, Source


class ReportRepository:
    def create_report(self, report: Report) -> Report:
        return ReportModel.objects.create(name=report.name, date=report.date)

    def get_report_by_id(self, report_id: int) -> Report:
        try:
            return ReportModel.objects.get(id=report_id)
        except ReportModel.DoesNotExist:
            return []

    def update_report(self, report: Report) -> Report:
        pass

    def delete_report(self, report_id: int) -> bool:
        try:
            ReportModel.objects.filter(report_id=report_id).delete()
            return True
        except Exception as e:
            print("Error deleting")
            return False
class SourceRepository:
    def create_source(self, source: Source) -> Source:
        pass

    def get_source_by_id(self, source_id: int):
        pass