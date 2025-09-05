from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, time, timedelta
from decimal import Decimal
import random

from core.models import Department, Leave, Attendance, Announcement, Payroll

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample data for Employee Management System'

    def handle(self, *args, **options):
        self.stdout.write('Starting to seed database...')
        
        # Create departments
        self.create_departments()
        
        # Create employees
        self.create_employees()
        
        # Create leaves
        self.create_leaves()
        
        # Create attendance records
        self.create_attendance()
        
        # Create announcements
        self.create_announcements()
        
        # Create payroll records
        self.create_payroll()
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))

    def create_departments(self):
        self.stdout.write('Creating departments...')
        
        departments_data = [
            'Human Resources',
            'Information Technology',
            'Finance',
            'Marketing',
            'Operations'
        ]
        
        created_departments = []
        for dept_name in departments_data:
            dept, created = Department.objects.get_or_create(name=dept_name)
            if created:
                self.stdout.write(f'  Created department: {dept_name}')
            created_departments.append(dept)
        
        return created_departments

    def create_employees(self):
        self.stdout.write('Creating employees...')
        
        # Get all departments
        departments = list(Department.objects.all())
        
        employees_data = [
            {
                'username': 'john.doe',
                'email': 'john.doe@company.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'department': departments[0] if departments else None,  # HR
                'salary': Decimal('45000.00'),
                'birthday': date(1990, 5, 15),
                'experience': 3,
                'date_of_joining': date(2021, 3, 1),
                'is_approved': True
            },
            {
                'username': 'jane.smith',
                'email': 'jane.smith@company.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'department': departments[1] if departments else None,  # IT
                'salary': Decimal('55000.00'),
                'birthday': date(1988, 8, 22),
                'experience': 5,
                'date_of_joining': date(2019, 6, 15),
                'is_approved': True
            },
            {
                'username': 'mike.johnson',
                'email': 'mike.johnson@company.com',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'department': departments[2] if departments else None,  # Finance
                'salary': Decimal('48000.00'),
                'birthday': date(1992, 12, 10),
                'experience': 2,
                'date_of_joining': date(2022, 1, 10),
                'is_approved': True
            },
            {
                'username': 'sarah.wilson',
                'email': 'sarah.wilson@company.com',
                'first_name': 'Sarah',
                'last_name': 'Wilson',
                'department': departments[3] if departments else None,  # Marketing
                'salary': Decimal('52000.00'),
                'birthday': date(1989, 3, 25),
                'experience': 4,
                'date_of_joining': date(2020, 9, 1),
                'is_approved': True
            },
            {
                'username': 'david.brown',
                'email': 'david.brown@company.com',
                'first_name': 'David',
                'last_name': 'Brown',
                'department': departments[4] if departments else None,  # Operations
                'salary': Decimal('46000.00'),
                'birthday': date(1991, 7, 8),
                'experience': 3,
                'date_of_joining': date(2021, 11, 15),
                'is_approved': True
            }
        ]
        
        created_employees = []
        for emp_data in employees_data:
            # Check if user already exists
            if not User.objects.filter(username=emp_data['username']).exists():
                user = User.objects.create_user(
                    username=emp_data['username'],
                    email=emp_data['email'],
                    password='password123',  # Default password
                    first_name=emp_data['first_name'],
                    last_name=emp_data['last_name'],
                    department=emp_data['department'],
                    salary=emp_data['salary'],
                    birthday=emp_data['birthday'],
                    experience=emp_data['experience'],
                    date_of_joining=emp_data['date_of_joining'],
                    is_approved=emp_data['is_approved'],
                    role='EMPLOYEE'
                )
                created_employees.append(user)
                self.stdout.write(f'  Created employee: {emp_data["first_name"]} {emp_data["last_name"]}')
            else:
                user = User.objects.get(username=emp_data['username'])
                created_employees.append(user)
                self.stdout.write(f'  Employee already exists: {emp_data["first_name"]} {emp_data["last_name"]}')
        
        return created_employees

    def create_leaves(self):
        self.stdout.write('Creating leave records...')
        
        employees = list(User.objects.filter(role='EMPLOYEE'))
        if not employees:
            self.stdout.write('  No employees found to create leaves for')
            return
        
        leave_reasons = [
            'Annual vacation',
            'Sick leave',
            'Personal emergency',
            'Medical appointment',
            'Family event'
        ]
        
        for employee in employees:
            # Create 1-3 leave records per employee
            num_leaves = random.randint(1, 3)
            for _ in range(num_leaves):
                start_date = date.today() - timedelta(days=random.randint(30, 180))
                end_date = start_date + timedelta(days=random.randint(1, 5))
                status = random.choice(['PENDING', 'APPROVED', 'REJECTED'])
                reason = random.choice(leave_reasons)
                
                Leave.objects.get_or_create(
                    employee=employee,
                    start_date=start_date,
                    end_date=end_date,
                    defaults={
                        'reason': reason,
                        'status': status
                    }
                )
        
        self.stdout.write(f'  Created leave records for {len(employees)} employees')

    def create_attendance(self):
        self.stdout.write('Creating attendance records...')
        
        employees = list(User.objects.filter(role='EMPLOYEE'))
        if not employees:
            self.stdout.write('  No employees found to create attendance for')
            return
        
        # Create attendance records for the last 30 days
        for employee in employees:
            for i in range(30):
                record_date = date.today() - timedelta(days=i)
                
                # Skip weekends (5=Saturday, 6=Sunday)
                if record_date.weekday() >= 5:
                    continue
                
                # Random clock in time between 8:00 AM and 9:30 AM
                clock_in_hour = random.randint(8, 9)
                clock_in_minute = random.randint(0, 59) if clock_in_hour == 8 else random.randint(0, 30)
                clock_in = time(clock_in_hour, clock_in_minute)
                
                # Random clock out time between 5:00 PM and 6:30 PM
                clock_out_hour = random.randint(17, 18)
                clock_out_minute = random.randint(0, 59)
                clock_out = time(clock_out_hour, clock_out_minute)
                
                Attendance.objects.get_or_create(
                    employee=employee,
                    date=record_date,
                    defaults={
                        'clock_in': clock_in,
                        'clock_out': clock_out
                    }
                )
        
        self.stdout.write(f'  Created attendance records for {len(employees)} employees')

    def create_announcements(self):
        self.stdout.write('Creating announcements...')
        
        announcements_data = [
            {
                'title': 'Company Holiday Schedule 2024',
                'content': 'Please review the updated holiday schedule for the upcoming year. All employees will receive 10 paid holidays.'
            },
            {
                'title': 'New Employee Benefits Package',
                'content': 'We are excited to announce enhanced benefits including improved health insurance and retirement matching.'
            },
            {
                'title': 'Office Renovation Notice',
                'content': 'The main office will undergo renovation starting next month. Some departments may be temporarily relocated.'
            },
            {
                'title': 'Annual Company Meeting',
                'content': 'Save the date for our annual company meeting on December 15th. All employees are required to attend.'
            },
            {
                'title': 'IT System Maintenance',
                'content': 'Scheduled maintenance will occur this weekend. Please save your work and expect some system downtime.'
            }
        ]
        
        for announcement_data in announcements_data:
            Announcement.objects.get_or_create(
                title=announcement_data['title'],
                defaults={
                    'content': announcement_data['content']
                }
            )
        
        self.stdout.write(f'  Created {len(announcements_data)} announcements')

    def create_payroll(self):
        self.stdout.write('Creating payroll records...')
        
        employees = list(User.objects.filter(role='EMPLOYEE'))
        if not employees:
            self.stdout.write('  No employees found to create payroll for')
            return
        
        # Create payroll records for the last 6 months
        for employee in employees:
            for i in range(6):
                # Calculate pay period dates
                end_date = date.today() - timedelta(days=i * 30)
                start_date = end_date - timedelta(days=29)
                
                # Use employee's salary or default to 45000
                salary = employee.salary or Decimal('45000.00')
                monthly_salary = salary / 12
                
                status = random.choice(['PENDING', 'PAID'])
                
                Payroll.objects.get_or_create(
                    employee=employee,
                    pay_period_start=start_date,
                    pay_period_end=end_date,
                    defaults={
                        'salary': monthly_salary,
                        'status': status
                    }
                )
        
        self.stdout.write(f'  Created payroll records for {len(employees)} employees')
