from django.shortcuts import render, redirect
from django.views import View
from core.services import ReportService
from core.entities import Report


class HomeView(View):

        def get(self, request):
            return render(request, "home.html")
class ReportListView(View):

    def get(self, request):
        report_service = ReportService()
        reports = report_service.get_all_reports()
        return render(request, "reports/report_list.html", {"reports": reports})


class ReportDetailView(View):
    def get(self, request, report_id):
        report_service = ReportService()
        report = report_service.get_report_by_id(report_id)
        return render(request, "reports/report_detail.html", {"report": report})


class ReportCreateView(View):

    def get(self, request):
        return render(request, "reports/report_create.html")

    def post(self, request):
        report_entity = Report(name=request.POST["report-name"], date=request.POST["report-date"])
        report_service = ReportService()
        created_report = report_service.create_report(report_entity)
        return redirect('report-detail', report_id=created_report.id)


