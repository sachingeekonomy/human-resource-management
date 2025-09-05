# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Department, Leave, Payroll, Attendance,Announcement

class AnnouncementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_attrs = {
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-3.5'
        }
        
        for field_name, field in self.fields.items():
            # Apply common styles to all fields except checkboxes
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.NumberInput, forms.Select, forms.DateInput, forms.PasswordInput)):
                field.widget.attrs.update(common_attrs)
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        

class AttendanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_attrs = {
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-3.5'
        }
        
        for field_name, field in self.fields.items():
            # Apply common styles to all fields except checkboxes
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.NumberInput, forms.Select, forms.DateInput, forms.PasswordInput)):
                field.widget.attrs.update(common_attrs)
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'clock_in', 'clock_out']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'clock_in': forms.TimeInput(attrs={'type': 'time'}),
            'clock_out': forms.TimeInput(attrs={'type': 'time'}),
        }

class PayrollForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_attrs = {
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-3.5'
        }
        
        for field_name, field in self.fields.items():
            # Apply common styles to all fields except checkboxes
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.NumberInput, forms.Select, forms.DateInput, forms.PasswordInput)):
                field.widget.attrs.update(common_attrs)
   
    class Meta:
        model = Payroll
        fields = ['employee', 'salary', 'pay_period_start', 'pay_period_end']
        widgets = {
            'pay_period_start': forms.DateInput(attrs={'type': 'date'}),
            'pay_period_end': forms.DateInput(attrs={'type': 'date'}),
        }

class LeaveForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_attrs = {
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-3.5'
        }
        
        for field_name, field in self.fields.items():
            # Apply common styles to all fields except checkboxes
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.NumberInput, forms.Select, forms.DateInput, forms.PasswordInput)):
                field.widget.attrs.update(common_attrs)
    class Meta:
        model = Leave
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class DepartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_attrs = {
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
        }
        
        for field_name, field in self.fields.items():
            # Apply common styles to all fields except checkboxes
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.NumberInput, forms.Select, forms.DateInput, forms.PasswordInput)):
                field.widget.attrs.update(common_attrs)
    class Meta:
        model = Department
        fields = ['name']

class EmployeeSignUpForm(UserCreationForm):
    """
    A form for creating new employee users with additional profile information.
    Inherits from Django's UserCreationForm and uses the custom User model.
    """
    # Making birthday a DateField with a widget for better UX
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    # Make the department field not required
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(), 
        empty_label="Select Department (Optional)",
        required=False 
    )
    # Make salary not required
    salary = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    # Make experience not required
    experience = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=50,
        widget=forms.NumberInput(attrs={'min': '0', 'max': '50'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_attrs = {
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
        }
        
        for field_name, field in self.fields.items():
            # Apply common styles to all fields except checkboxes
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.NumberInput, forms.Select, forms.DateInput, forms.PasswordInput)):
                field.widget.attrs.update(common_attrs)
        
        # Ensure required fields are marked
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True
        
        # Remove strict password validation - make it simple
        self.fields['password1'].help_text = "Enter your password (minimum 1 character)"
        self.fields['password2'].help_text = "Enter the same password as before, for verification."
        
        # Remove Django's built-in password validators to avoid similarity checks
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []

    def clean_password1(self):
        """Custom password validation - only check minimum length."""
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) < 1:
            raise forms.ValidationError("Password must be at least 1 character long.")
        return password1

    def clean_password2(self):
        """Custom password confirmation validation."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def clean_username(self):
        """Check if username is already taken."""
        username = self.cleaned_data.get('username')
        print(f"DEBUG: clean_username called with: '{username}'")
        print(f"DEBUG: Form instance: {self.instance}")
        print(f"DEBUG: Form instance.pk: {getattr(self.instance, 'pk', None)}")
        
        if username:
            # If we're editing an existing user, exclude that user from the check
            queryset = User.objects.filter(username=username)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
                print(f"DEBUG: Excluding user with pk: {self.instance.pk}")
            
            exact_match = queryset.exists()
            print(f"DEBUG: Exact match for '{username}': {exact_match}")
            
            # Check for case-insensitive match
            case_insensitive_queryset = User.objects.filter(username__iexact=username)
            if self.instance and self.instance.pk:
                case_insensitive_queryset = case_insensitive_queryset.exclude(pk=self.instance.pk)
            
            case_insensitive_match = case_insensitive_queryset.exists()
            print(f"DEBUG: Case-insensitive match for '{username}': {case_insensitive_match}")
            
            # List all existing usernames for debugging
            existing_usernames = list(User.objects.values_list('username', flat=True))
            print(f"DEBUG: All existing usernames: {existing_usernames}")
            
            if exact_match:
                print(f"DEBUG: Username '{username}' already exists!")
                raise forms.ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        """Check if email is already taken."""
        email = self.cleaned_data.get('email')
        print(f"DEBUG: clean_email called with: '{email}'")
        print(f"DEBUG: Form instance: {self.instance}")
        print(f"DEBUG: Form instance.pk: {getattr(self.instance, 'pk', None)}")
        
        if email:
            # If we're editing an existing user, exclude that user from the check
            queryset = User.objects.filter(email=email)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
                print(f"DEBUG: Excluding user with pk: {self.instance.pk}")
            
            exact_match = queryset.exists()
            print(f"DEBUG: Exact email match for '{email}': {exact_match}")
            
            # Check for case-insensitive match
            case_insensitive_queryset = User.objects.filter(email__iexact=email)
            if self.instance and self.instance.pk:
                case_insensitive_queryset = case_insensitive_queryset.exclude(pk=self.instance.pk)
            
            case_insensitive_match = case_insensitive_queryset.exists()
            print(f"DEBUG: Case-insensitive email match for '{email}': {case_insensitive_match}")
            
            # List all existing emails for debugging
            existing_emails = list(User.objects.values_list('email', flat=True))
            print(f"DEBUG: All existing emails: {existing_emails}")
            
            if exact_match:
                print(f"DEBUG: Email '{email}' already exists!")
                raise forms.ValidationError("A user with this email already exists.")
        return email

    def _post_clean(self):
        """Override to run our custom validations while skipping Django's password validation."""
        print(f"DEBUG: _post_clean called")
        print(f"DEBUG: Form fields: {list(self.fields.keys())}")
        
        # Run individual field clean methods (including our custom clean_username and clean_email)
        self._clean_fields()
        
        # Run our custom clean method
        self._clean_form()
        
        # Skip the parent's _post_clean to avoid Django's built-in password validation
        # We only want our custom validation from clean_password1 and clean_password2

    def clean(self):
        """Custom validation for the form."""
        cleaned_data = super().clean()
        print(f"DEBUG: Form clean method called. Data: {cleaned_data}")
        return cleaned_data

    class Meta(UserCreationForm.Meta):
        model = User
        # Add the new fields to the form, including password fields
        fields = (
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'department', 
            'salary', 
            'birthday', 
            'experience',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        """
        Saves the user instance, setting the role to 'EMPLOYEE'.
        The user will not be approved by default but will be active.
        """
        print(f"DEBUG: Form save method called. Commit: {commit}")
        print(f"DEBUG: Form cleaned_data: {self.cleaned_data}")
        
        user = super().save(commit=False)
        
        # Ensure the user object has the correct values from the form
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.department = self.cleaned_data.get('department')
        user.salary = self.cleaned_data.get('salary')
        user.birthday = self.cleaned_data.get('birthday')
        user.experience = self.cleaned_data.get('experience')
        
        user.role = 'EMPLOYEE'
        # For self-signup, is_approved should be False
        user.is_approved = False
        user.is_active = True # IMPORTANT: This allows the user to be authenticated
        
        print(f"DEBUG: User object before save - Username: '{user.username}', Email: '{user.email}'")
        
        if commit:
            # Final check right before saving to database
            username = user.username
            email = user.email
            
            print(f"DEBUG: Final check before save - Username: '{username}', Email: '{email}'")
            
            # Check username one more time
            if User.objects.filter(username=username).exists():
                print(f"DEBUG: Username '{username}' now exists in database!")
                raise forms.ValidationError("A user with this username already exists.")
            
            # Check email one more time
            if User.objects.filter(email=email).exists():
                print(f"DEBUG: Email '{email}' now exists in database!")
                raise forms.ValidationError("A user with this email already exists.")
            
            print(f"DEBUG: Saving user to database: {user.username}")
            try:
                user.save()
                print(f"DEBUG: User saved successfully! User ID: {user.id}")
            except Exception as e:
                print(f"DEBUG: Error saving user: {e}")
                # Re-raise as ValidationError so it's handled properly by the form
                if "UNIQUE constraint failed" in str(e):
                    if "username" in str(e):
                        raise forms.ValidationError("A user with this username already exists.")
                    elif "email" in str(e):
                        raise forms.ValidationError("A user with this email already exists.")
                raise forms.ValidationError(f"Error saving user: {str(e)}")
        return user

class EmployeeUpdateForm(UserChangeForm):
    password = None # Exclude password from the form
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(), 
        empty_label="Select Department (Optional)",
        required=False
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_attrs = {
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
        }
        
        for field_name, field in self.fields.items():
            # Apply common styles to all fields except checkboxes
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.NumberInput, forms.Select, forms.DateInput)):
                field.widget.attrs.update(common_attrs)

    class Meta:
        model = User
        fields = (
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'department', 
            'salary', 
            'birthday', 
            'experience'
        )
