# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.urls import reverse_lazy
from .forms import EmployeeSignUpForm, EmployeeUpdateForm, DepartmentForm, LeaveForm, PayrollForm, AttendanceForm, AnnouncementForm
from .models import Department, User, Leave, Payroll, Attendance, Announcement
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import date, datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Q

# --- Custom Mixins for Role-Based Access ---

class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is an admin or superuser."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not (request.user.is_superuser or request.user.role == 'ADMIN'):
            return redirect('employee_dashboard')
        return super().dispatch(request, *args, **kwargs)

class EmployeeRequiredMixin(AccessMixin):
    """Verify that the current user is an approved employee."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_superuser or request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        if not request.user.is_approved:
            return redirect('not_approved')
        return super().dispatch(request, *args, **kwargs)

class RedirectLoggedInUserMixin(AccessMixin):
    """Redirects logged-in users from public pages to their dashboard."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.role == 'ADMIN':
                return redirect('admin_dashboard')
            else:
                return redirect('employee_dashboard')
        return super().dispatch(request, *args, **kwargs)


class SignUpView(CreateView):
    """
    View for employee registration.
    Uses the EmployeeSignUpForm and redirects to the login page on success.
    """
    form_class = EmployeeSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    
    def form_valid(self, form):
        """Handle successful form submission."""
        print(f"DEBUG: Form is valid, saving user: {form.cleaned_data.get('username')}")
        response = super().form_valid(form)
        messages.success(
            self.request, 
            'Account created successfully! Please wait for admin approval before you can log in.'
        )
        return response
    
    def form_invalid(self, form):
        """Handle form validation errors."""
        print(f"DEBUG: Form is invalid. Errors: {form.errors}")
        # Add a general error message
        messages.error(
            self.request, 
            'Please correct the errors below and try again.'
        )
        return super().form_invalid(form)
    
    def post(self, request, *args, **kwargs):
        """Handle POST request with debug logging."""
        print(f"DEBUG: POST request received for signup")
        print(f"DEBUG: POST data: {request.POST}")
        return super().post(request, *args, **kwargs)

class CustomLoginView(LoginView):
    """
    Custom login view that checks for employee approval.
    """
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard_redirect')
    
    def form_valid(self, form):
        """Check if user is approved after successful authentication."""
        response = super().form_valid(form)
        user = form.get_user()
        
        # Check if user is approved
        if hasattr(user, 'is_approved') and not user.is_approved:
            # Log out the user and redirect to not_approved page
            from django.contrib.auth import logout
            logout(self.request)
            messages.error(
                self.request,
                'Your account is not approved yet. Please wait for admin approval.'
            )
            return redirect('login')
        
        return response
    
    def form_invalid(self, form):
        """Handle invalid login attempts."""
        # Add error message for invalid credentials
        messages.error(
            self.request,
            'Invalid username or password. Please check your credentials and try again.'
        )
        return super().form_invalid(form)

class DashboardRedirectView(LoginRequiredMixin, TemplateView):
    """
    Redirects users to their respective dashboards based on their role.
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        elif request.user.role == 'EMPLOYEE':
            if not request.user.is_approved:
                return redirect('not_approved')
            return redirect('employee_dashboard')
        return redirect('home') 

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    """
    Displays the admin dashboard with dynamic stats.
    """
    template_name = 'admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        current_month = today.month
        current_year = today.year

        # First row stats
        context['total_employees'] = User.objects.filter(role='EMPLOYEE', is_approved=True).count()
        context['on_leave_today'] = Leave.objects.filter(start_date__lte=today, end_date__gte=today, status='APPROVED').count()
        context['total_departments'] = Department.objects.count()
        context['pending_leave_approvals'] = Leave.objects.filter(status='PENDING').count()

        # Second row stats
        context['present_today'] = Attendance.objects.filter(date=today, clock_in__isnull=False).count()
        context['total_announcements'] = Announcement.objects.count()
        context['approved_leave_month'] = Leave.objects.filter(status='APPROVED', start_date__year=current_year, start_date__month=current_month).count()
        context['pending_payrolls'] = Payroll.objects.filter(status='PENDING').count()

        context['today'] = today
        return context

class EmployeeDashboardView(EmployeeRequiredMixin, TemplateView):
    """
    Displays the employee dashboard with dynamic, personalized stats.
    """
    template_name = 'employee_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.request.user
        today = date.today()
        current_month = today.month
        current_year = today.year

        context['pending_leaves'] = Leave.objects.filter(employee=employee, status='PENDING').count()
        context['approved_leaves_month'] = Leave.objects.filter(
            employee=employee, 
            status='APPROVED', 
            start_date__year=current_year, 
            start_date__month=current_month
        ).count()
        context['attendance_month'] = Attendance.objects.filter(
            employee=employee, 
            date__year=current_year, 
            date__month=current_month
        ).count()
        context['unread_announcements'] = Announcement.objects.count() # This is a placeholder, a read/unread system would be needed for accuracy
        context['today'] = today
        return context


# --- Static Pages ---
class HomePageView(RedirectLoggedInUserMixin, TemplateView):
    template_name = 'home.html'

class AboutUsView(RedirectLoggedInUserMixin, TemplateView):
    template_name = 'about.html'

class ContactUsView(RedirectLoggedInUserMixin, TemplateView):
    template_name = 'contact.html'

class NotApprovedView(TemplateView):
    template_name = 'not_approved.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Ensure only unapproved users can access this view."""
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_approved:
            return redirect('dashboard_redirect')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Add user information to context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

# --- Admin Employee Management ---
class AdminEmployeeListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'admin_view_employees.html'
    context_object_name = 'employees'
    paginate_by = 15
    ordering = ['-id']  # Newest first

    def get_queryset(self):
        return User.objects.filter(role='EMPLOYEE').order_by('-id')

class AdminAddEmployeeView(AdminRequiredMixin, CreateView):
    form_class = EmployeeSignUpForm
    template_name = 'admin_add_employee.html'
    success_url = reverse_lazy('admin_view_employees')

    def form_valid(self, form):
        """Handle successful form submission."""
        try:
            form.instance.is_approved = True
            response = super().form_valid(form)
            messages.success(
                self.request, 
                f'Employee "{form.instance.username}" has been added successfully!'
            )
            return response
        except Exception as e:
            print(f"DEBUG: Error saving employee: {e}")
            messages.error(
                self.request, 
                f'Error adding employee: {str(e)}'
            )
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        """Handle form validation errors."""
        print(f"DEBUG: Admin add employee form is invalid. Errors: {form.errors}")
        # Add a general error message
        messages.error(
            self.request, 
            'Please correct the errors below and try again.'
        )
        return super().form_invalid(form)
    
class AdminEmployeeUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = EmployeeUpdateForm
    template_name = 'admin_edit_employee.html'
    success_url = reverse_lazy('admin_view_employees')

@login_required
def approve_employee(request, pk):
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        return redirect('employee_dashboard')
    employee = get_object_or_404(User, pk=pk)
    employee.is_approved = True
    employee.save()
    return redirect('admin_view_employees')

@login_required
def reject_employee(request, pk):
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        return redirect('employee_dashboard')
    employee = get_object_or_404(User, pk=pk)
    employee.delete()
    return redirect('admin_view_employees')

class AdminEmployeeDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'admin_delete_employee.html'
    success_url = reverse_lazy('admin_view_employees')


# --- Admin Department Management ---
class AdminDepartmentListView(AdminRequiredMixin, ListView):
    model = Department
    template_name = 'admin_view_departments.html'
    context_object_name = 'departments'

class AdminAddDepartmentView(AdminRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'admin_add_department.html'
    success_url = reverse_lazy('admin_view_departments')

class AdminDepartmentUpdateView(AdminRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'admin_edit_department.html'
    success_url = reverse_lazy('admin_view_departments')

class AdminDepartmentDeleteView(AdminRequiredMixin, DeleteView):
    model = Department
    template_name = 'admin_delete_department.html'
    success_url = reverse_lazy('admin_view_departments')


# --- Employee Leave Management ---
class LeaveApplyView(EmployeeRequiredMixin, CreateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'leave_apply.html'
    success_url = reverse_lazy('leave_history')

    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)

class LeaveHistoryView(EmployeeRequiredMixin, ListView):
    model = Leave
    template_name = 'leave_history.html'
    context_object_name = 'leaves'

    def get_queryset(self):
        return Leave.objects.filter(employee=self.request.user)

# --- Admin Leave Management ---
class AdminLeaveManageView(AdminRequiredMixin, ListView):
    model = Leave
    template_name = 'admin_manage_leaves.html'
    context_object_name = 'leaves'
    paginate_by = 15
    ordering = ['-id']  # Newest first (by ID, which is auto-incrementing)
    
    def get_queryset(self):
        queryset = Leave.objects.select_related('employee').order_by('-id')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status and status in ['PENDING', 'APPROVED', 'REJECTED']:
            queryset = queryset.filter(status=status)
        
        # Filter by employee name
        employee_name = self.request.GET.get('employee')
        if employee_name:
            queryset = queryset.filter(
                models.Q(employee__first_name__icontains=employee_name) |
                models.Q(employee__last_name__icontains=employee_name) |
                models.Q(employee__username__icontains=employee_name)
            )
        
        # Filter by date range
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if start_date:
            try:
                from datetime import datetime
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(start_date__gte=start_date_obj)
            except ValueError:
                pass  # Invalid date format, ignore filter
        
        if end_date:
            try:
                from datetime import datetime
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(end_date__lte=end_date_obj)
            except ValueError:
                pass  # Invalid date format, ignore filter
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filter values to context for form persistence
        context['current_status'] = self.request.GET.get('status', '')
        context['current_employee'] = self.request.GET.get('employee', '')
        context['current_start_date'] = self.request.GET.get('start_date', '')
        context['current_end_date'] = self.request.GET.get('end_date', '')
        
        # Add status choices for filter dropdown
        context['status_choices'] = [
            ('', 'All Statuses'),
            ('PENDING', 'Pending'),
            ('APPROVED', 'Approved'),
            ('REJECTED', 'Rejected'),
        ]
        
        return context

@login_required
def approve_leave(request, pk):
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        return redirect('employee_dashboard')
    leave = get_object_or_404(Leave, pk=pk)
    leave.status = 'APPROVED'
    leave.save()
    return redirect('admin_manage_leaves')

@login_required
def reject_leave(request, pk):
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        return redirect('employee_dashboard')
    leave = get_object_or_404(Leave, pk=pk)
    leave.status = 'REJECTED'
    leave.save()
    return redirect('admin_manage_leaves')


# --- Payroll Management ---
class AdminPayrollListView(AdminRequiredMixin, ListView):
    model = Payroll
    template_name = 'admin_manage_payroll.html'
    context_object_name = 'payrolls'
    paginate_by = 15
    ordering = ['-id']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Debug: Print initial queryset count
        print(f"DEBUG: Initial queryset count: {queryset.count()}")
        print(f"DEBUG: GET parameters: {dict(self.request.GET)}")
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            print(f"DEBUG: Filtering by status: {status}")
            queryset = queryset.filter(status=status)
            print(f"DEBUG: After status filter count: {queryset.count()}")
        
        # Filter by employee name/username
        employee_search = self.request.GET.get('employee')
        if employee_search:
            print(f"DEBUG: Filtering by employee: {employee_search}")
            queryset = queryset.filter(
                Q(employee__first_name__icontains=employee_search) |
                Q(employee__last_name__icontains=employee_search) |
                Q(employee__username__icontains=employee_search)
            )
            print(f"DEBUG: After employee filter count: {queryset.count()}")
        
        # Filter by pay period start date
        start_date = self.request.GET.get('start_date')
        if start_date:
            print(f"DEBUG: Filtering by start_date: {start_date}")
            queryset = queryset.filter(pay_period_start__gte=start_date)
            print(f"DEBUG: After start_date filter count: {queryset.count()}")
        
        # Filter by pay period end date
        end_date = self.request.GET.get('end_date')
        if end_date:
            print(f"DEBUG: Filtering by end_date: {end_date}")
            queryset = queryset.filter(pay_period_end__lte=end_date)
            print(f"DEBUG: After end_date filter count: {queryset.count()}")
        
        print(f"DEBUG: Final queryset count: {queryset.count()}")
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filter choices
        context['status_choices'] = [
            ('', 'All Status'),
            ('PENDING', 'Pending'),
            ('PAID', 'Paid'),
        ]
        
        # Add current filter values
        context['current_status'] = self.request.GET.get('status', '')
        context['current_employee'] = self.request.GET.get('employee', '')
        context['current_start_date'] = self.request.GET.get('start_date', '')
        context['current_end_date'] = self.request.GET.get('end_date', '')
        
        return context

class CreatePayrollView(AdminRequiredMixin, CreateView):
    model = Payroll
    form_class = PayrollForm
    template_name = 'admin_create_payroll.html'
    success_url = reverse_lazy('admin_manage_payroll')
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['employee'].queryset = User.objects.filter(role='EMPLOYEE', is_approved=True)
        return form

@login_required
def process_payroll(request, pk):
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        return redirect('employee_dashboard')
    payroll = get_object_or_404(Payroll, pk=pk)
    payroll.status = 'PAID'
    payroll.save()
    return redirect('admin_manage_payroll')

class EmployeePayslipListView(EmployeeRequiredMixin, ListView):
    model = Payroll
    template_name = 'employee_payslips.html'
    context_object_name = 'payslips'

    def get_queryset(self):
        return Payroll.objects.filter(employee=self.request.user)
    
@login_required
def payslip_pdf_view(request, pk):
    if not request.user.role == 'EMPLOYEE':
        return redirect('admin_dashboard')
    payslip = get_object_or_404(Payroll, pk=pk, employee=request.user)
    template_path = 'payslip_pdf.html'
    context = {'payslip': payslip}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{payslip.employee.username}_{payslip.pay_period_start}.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# --- Attendance Management ---
@login_required
def clock_in(request):
    if not request.user.role == 'EMPLOYEE':
        return redirect('admin_dashboard')
    # Check if the employee has already clocked in today
    if Attendance.objects.filter(employee=request.user, date=date.today()).exists():
        messages.error(request, 'You have already clocked in today.')
        return redirect('employee_attendance')

    Attendance.objects.create(
        employee=request.user,
        date=date.today(),
        clock_in=datetime.now().time()
    )
    messages.success(request, 'Clocked in successfully.')
    return redirect('employee_attendance')

@login_required
def clock_out(request):
    if not request.user.role == 'EMPLOYEE':
        return redirect('admin_dashboard')
    try:
        attendance = Attendance.objects.get(employee=request.user, date=date.today())
        if attendance.clock_out:
            messages.error(request, 'You have already clocked out today.')
        else:
            attendance.clock_out = datetime.now().time()
            attendance.save()
            messages.success(request, 'Clocked out successfully.')
    except Attendance.DoesNotExist:
        messages.error(request, 'You have not clocked in today.')
    
    return redirect('employee_attendance')

class EmployeeAttendanceView(EmployeeRequiredMixin, ListView):
    model = Attendance
    template_name = 'employee_attendance.html'
    context_object_name = 'attendance_records'

    def get_queryset(self):
        return Attendance.objects.filter(employee=self.request.user)

class AdminManageAttendanceView(AdminRequiredMixin, ListView):
    model = Attendance
    template_name = 'admin_manage_attendance.html'
    context_object_name = 'attendance_records'
    paginate_by = 15
    ordering = ['-date', '-clock_in']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Debug: Print initial queryset count
        print(f"DEBUG: Initial attendance queryset count: {queryset.count()}")
        print(f"DEBUG: GET parameters: {dict(self.request.GET)}")
        
        # Filter by employee name/username
        employee_search = self.request.GET.get('employee')
        if employee_search:
            print(f"DEBUG: Filtering by employee: {employee_search}")
            queryset = queryset.filter(
                Q(employee__first_name__icontains=employee_search) |
                Q(employee__last_name__icontains=employee_search) |
                Q(employee__username__icontains=employee_search)
            )
            print(f"DEBUG: After employee filter count: {queryset.count()}")
        
        # Filter by date range - start date
        start_date = self.request.GET.get('start_date')
        if start_date:
            print(f"DEBUG: Filtering by start_date: {start_date}")
            queryset = queryset.filter(date__gte=start_date)
            print(f"DEBUG: After start_date filter count: {queryset.count()}")
        
        # Filter by date range - end date
        end_date = self.request.GET.get('end_date')
        if end_date:
            print(f"DEBUG: Filtering by end_date: {end_date}")
            queryset = queryset.filter(date__lte=end_date)
            print(f"DEBUG: After end_date filter count: {queryset.count()}")
        
        # Filter by attendance status (present/absent)
        status = self.request.GET.get('status')
        if status:
            print(f"DEBUG: Filtering by status: {status}")
            if status == 'present':
                queryset = queryset.filter(clock_in__isnull=False)
            elif status == 'absent':
                # For absent, we need to check if there's no attendance record for that date
                # This is more complex and might need a different approach
                pass
            print(f"DEBUG: After status filter count: {queryset.count()}")
        
        print(f"DEBUG: Final attendance queryset count: {queryset.count()}")
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filter choices
        context['status_choices'] = [
            ('', 'All Records'),
            ('present', 'Present'),
            ('absent', 'Absent'),
        ]
        
        # Add current filter values
        context['current_employee'] = self.request.GET.get('employee', '')
        context['current_start_date'] = self.request.GET.get('start_date', '')
        context['current_end_date'] = self.request.GET.get('end_date', '')
        context['current_status'] = self.request.GET.get('status', '')
        
        return context

class AdminAddAttendanceView(AdminRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'admin_add_attendance.html'
    success_url = reverse_lazy('admin_manage_attendance')
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['employee'].queryset = User.objects.filter(role='EMPLOYEE', is_approved=True)
        return form

# --- Announcement Management ---
class AdminAnnouncementListView(AdminRequiredMixin, ListView):
    model = Announcement
    template_name = 'admin_view_announcements.html'
    context_object_name = 'announcements'

class AdminAddAnnouncementView(AdminRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'admin_add_announcement.html'
    success_url = reverse_lazy('admin_view_announcements')

class AdminAnnouncementUpdateView(AdminRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'admin_edit_announcement.html'
    success_url = reverse_lazy('admin_view_announcements')

class AdminAnnouncementDeleteView(AdminRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'admin_delete_announcement.html'
    success_url = reverse_lazy('admin_view_announcements')

class EmployeeAnnouncementListView(EmployeeRequiredMixin, ListView):
    model = Announcement
    template_name = 'employee_view_announcements.html'
    context_object_name = 'announcements'
    ordering = ['-created_at']
    paginate_by = 10
