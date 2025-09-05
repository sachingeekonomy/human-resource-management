# core/urls.py

from django.urls import path
from .views import (
    HomePageView, 
    SignUpView, 
    CustomLoginView, 
    DashboardRedirectView,
    AdminDashboardView,
    EmployeeDashboardView,
    AboutUsView,
    ContactUsView,
    NotApprovedView,
    AdminEmployeeListView,
    AdminAddEmployeeView,
    AdminEmployeeUpdateView,
    approve_employee,
    reject_employee,
    AdminEmployeeDeleteView,
    AdminDepartmentListView,
    AdminAddDepartmentView,
    AdminDepartmentUpdateView,
    AdminDepartmentDeleteView,
    LeaveApplyView,
    LeaveHistoryView,
    AdminLeaveManageView,
    approve_leave,
    reject_leave,
    AdminPayrollListView,
    CreatePayrollView,
    process_payroll,
    EmployeePayslipListView,
    payslip_pdf_view,
    clock_in,
    clock_out,
    EmployeeAttendanceView,
    AdminManageAttendanceView,
    AdminAddAttendanceView,
    AdminAnnouncementListView,
    AdminAddAnnouncementView,
    AdminAnnouncementUpdateView,
    AdminAnnouncementDeleteView,
    EmployeeAnnouncementListView,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Static and Authentication URLs
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutUsView.as_view(), name='about'),
    path('contact/', ContactUsView.as_view(), name='contact'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # Dashboard URLs
    path('dashboard/', DashboardRedirectView.as_view(), name='dashboard_redirect'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/employee/', EmployeeDashboardView.as_view(), name='employee_dashboard'),
    path('not-approved/', NotApprovedView.as_view(), name='not_approved'),

    # Admin Employee Management URLs
    path('dashboard/admin/employees/', AdminEmployeeListView.as_view(), name='admin_view_employees'),
    path('dashboard/admin/employees/add/', AdminAddEmployeeView.as_view(), name='admin_add_employee'),
    path('dashboard/admin/employees/edit/<int:pk>/', AdminEmployeeUpdateView.as_view(), name='admin_edit_employee'),
    path('dashboard/admin/employees/delete/<int:pk>/', AdminEmployeeDeleteView.as_view(), name='admin_delete_employee'),
    path('dashboard/admin/employees/approve/<int:pk>/', approve_employee, name='admin_approve_employee'),
    path('dashboard/admin/employees/reject/<int:pk>/', reject_employee, name='admin_reject_employee'),
    
     # Admin Department Management URLs
    path('dashboard/admin/departments/', AdminDepartmentListView.as_view(), name='admin_view_departments'),
    path('dashboard/admin/departments/add/', AdminAddDepartmentView.as_view(), name='admin_add_department'),
    path('dashboard/admin/departments/edit/<int:pk>/', AdminDepartmentUpdateView.as_view(), name='admin_edit_department'),
    path('dashboard/admin/departments/delete/<int:pk>/', AdminDepartmentDeleteView.as_view(), name='admin_delete_department'),

    # Employee Leave Management URLs
    path('dashboard/employee/leave/apply/', LeaveApplyView.as_view(), name='leave_apply'),
    path('dashboard/employee/leave/history/', LeaveHistoryView.as_view(), name='leave_history'),

    # Admin Leave Management URLs
    path('dashboard/admin/leaves/', AdminLeaveManageView.as_view(), name='admin_manage_leaves'),
    path('dashboard/admin/leaves/approve/<int:pk>/', approve_leave, name='admin_approve_leave'),
    path('dashboard/admin/leaves/reject/<int:pk>/', reject_leave, name='admin_reject_leave'),

    # Payroll Management URLs
    path('dashboard/admin/payroll/', AdminPayrollListView.as_view(), name='admin_manage_payroll'),
    path('dashboard/admin/payroll/create/', CreatePayrollView.as_view(), name='admin_create_payroll'),
    path('dashboard/admin/payroll/process/<int:pk>/', process_payroll, name='admin_process_payroll'),
    path('dashboard/employee/payslips/', EmployeePayslipListView.as_view(), name='employee_payslips'),
    path('dashboard/employee/payslip/<int:pk>/pdf/', payslip_pdf_view, name='payslip_pdf'),

    # Attendance Management URLs
    path('dashboard/employee/attendance/', EmployeeAttendanceView.as_view(), name='employee_attendance'),
    path('dashboard/employee/clock-in/', clock_in, name='clock_in'),
    path('dashboard/employee/clock-out/', clock_out, name='clock_out'),
    path('dashboard/admin/attendance/', AdminManageAttendanceView.as_view(), name='admin_manage_attendance'),
    path('dashboard/admin/attendance/add/', AdminAddAttendanceView.as_view(), name='admin_add_attendance'),

    # Announcement Management URLs
    path('dashboard/admin/announcements/', AdminAnnouncementListView.as_view(), name='admin_view_announcements'),
    path('dashboard/admin/announcements/add/', AdminAddAnnouncementView.as_view(), name='admin_add_announcement'),
    path('dashboard/admin/announcements/edit/<int:pk>/', AdminAnnouncementUpdateView.as_view(), name='admin_edit_announcement'),
    path('dashboard/admin/announcements/delete/<int:pk>/', AdminAnnouncementDeleteView.as_view(), name='admin_delete_announcement'),
    path('dashboard/employee/announcements/', EmployeeAnnouncementListView.as_view(), name='employee_view_announcements'),

]
