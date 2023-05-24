from typing import List

from .repositories import ReportRepository, SourceRepository
from .entities import Report, Source


class ReportService:
    def __init__(self, report_repository: ReportRepository = ReportRepository()):
        self.report_repository = report_repository

    def create_report(self, report: Report) -> Report:
        return self.report_repository.create_report(report)

    def get_reports_by_year(self, year: str) -> List[Report]:
        return self.report_repository.get_reports_by_year(year)

    def get_reports_by_date_range(self, start_date: str, end_date: str) -> List[Report]:
        return self.report_repository.get_reports_by_date_range(start_date, end_date)

    def get_all_reports(self) -> list[Report]:
        return self.report_repository.get_all_reports()

    def get_report_by_id(self, report_id: int) -> Report:
        return self.report_repository.get_report_by_id(report_id)

    def update_report(self, report_id: int, report: Report) -> Report:
        return self.report_repository.update_report(report_id, report=report)

    def delete_report(self, report_id: int) -> bool:
        return self.report_repository.delete_report(report_id)


class SourceService:
    def __init__(self, source_repository: SourceRepository = SourceRepository()):
        self.source_repository = source_repository

    def create_source(self, source: Source) -> Source:
        return self.source_repository.create_source(source)

    def get_source_by_id(self, source_id: int) -> Source:
        return self.source_repository.get_source_by_id(source_id)

    def get_all_sources(self) -> List[Source]:
        return self.source_repository.get_all_sources()

    def update_source(self, source_id, source: Source) -> Source:
        return self.source_repository.update_source(source_id, source=source)

    def delete_source(self, source_id: int) -> bool:
        return self.source_repository.delete_source(source_id)