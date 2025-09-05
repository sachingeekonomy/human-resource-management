from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Department, Leave, Attendance, Announcement, Payroll

User = get_user_model()

class Command(BaseCommand):
    help = 'Clear all seeded data from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep-admin',
            action='store_true',
            help='Keep admin users when clearing data',
        )

    def handle(self, *args, **options):
        self.stdout.write('Starting to clear database...')
        
        # Clear payroll records
        payroll_count = Payroll.objects.count()
        Payroll.objects.all().delete()
        self.stdout.write(f'  Deleted {payroll_count} payroll records')
        
        # Clear attendance records
        attendance_count = Attendance.objects.count()
        Attendance.objects.all().delete()
        self.stdout.write(f'  Deleted {attendance_count} attendance records')
        
        # Clear leave records
        leave_count = Leave.objects.count()
        Leave.objects.all().delete()
        self.stdout.write(f'  Deleted {leave_count} leave records')
        
        # Clear announcements
        announcement_count = Announcement.objects.count()
        Announcement.objects.all().delete()
        self.stdout.write(f'  Deleted {announcement_count} announcements')
        
        # Clear employees (but keep admin users if requested)
        if options['keep_admin']:
            employee_count = User.objects.filter(role='EMPLOYEE').count()
            User.objects.filter(role='EMPLOYEE').delete()
            self.stdout.write(f'  Deleted {employee_count} employee users (kept admin users)')
        else:
            # Clear all non-superuser users
            user_count = User.objects.filter(is_superuser=False).count()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(f'  Deleted {user_count} non-admin users')
        
        # Clear departments
        department_count = Department.objects.count()
        Department.objects.all().delete()
        self.stdout.write(f'  Deleted {department_count} departments')
        
        self.stdout.write(self.style.SUCCESS('Successfully cleared database!'))
