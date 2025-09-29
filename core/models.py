# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.conf import settings
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError('The Username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # Default role for a new user is 'EMPLOYEE'
        extra_fields.setdefault('role', 'EMPLOYEE')
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        # The superuser will also be an admin and is approved by default
        extra_fields.setdefault('is_approved', True) 
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model for the Employee Management System.
    """
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('EMPLOYEE', 'Employee'),
    )

    # Fields for the user model
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='EMPLOYEE')
    is_approved = models.BooleanField(default=False)
    
    # New fields for employee details
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    experience = models.PositiveIntegerField(null=True, blank=True, help_text="Experience in years")
    date_of_joining = models.DateField(null=True, blank=True)

    # Use the custom manager
    objects = CustomUserManager()

    # Add related_name to avoid clashes with the default User model
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",  # Unique related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions_set",  # Unique related_name
        related_query_name="user",
    )

    def is_admin(self):
        """Check if user is an admin (superuser or ADMIN role)"""
        return self.is_superuser or self.role == 'ADMIN'
    
    def is_manager(self):
        """Check if user is a manager (MANAGER role)"""
        return self.role == 'MANAGER'
    
    def is_employee(self):
        """Check if user is a regular employee"""
        return self.role == 'EMPLOYEE'
    
    def has_admin_permissions(self):
        """Check if user has admin-level permissions"""
        return self.is_admin()
    
    def has_manager_permissions(self):
        """Check if user has manager-level permissions (admin or manager)"""
        return self.is_admin() or self.is_manager()
    
    def can_manage_employees(self):
        """Check if user can manage employees"""
        return self.has_manager_permissions()
    
    def can_manage_departments(self):
        """Check if user can manage departments"""
        return self.has_admin_permissions()
    
    def can_manage_payroll(self):
        """Check if user can manage payroll"""
        return self.has_manager_permissions()
    
    def can_manage_attendance(self):
        """Check if user can manage attendance"""
        return self.has_manager_permissions()
    
    def can_manage_leaves(self):
        """Check if user can manage leaves"""
        return self.has_manager_permissions()
    
    def can_manage_announcements(self):
        """Check if user can manage announcements"""
        return self.has_manager_permissions()

class Leave(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=500)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.employee.username} - {self.start_date} to {self.end_date}"
    
class Attendance(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    clock_in = models.TimeField()
    clock_out = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.username} - {self.date}"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Payroll(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
    )
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.employee.username} - {self.pay_period_start} to {self.pay_period_end}"
