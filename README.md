Employee Management System (EMS)

Description
This project is a comprehensive Employee Management System built with Django. It provides a robust platform for managing all aspects of an employee's lifecycle within an organization. The system features distinct dashboards and functionalities for both Admins and Employees, ensuring a secure and efficient workflow.

Features
The system is divided into two main roles, each with a specific set of features:

👤 Admin Features
Dashboard: A dynamic dashboard with real-time statistics, including total employees, employees on leave, department counts, and pending approvals.

Employee Management:

View a complete list of all employees.

Add new employees with pre-approved status.

Edit existing employee details.

Approve or reject new employee sign-ups.

Delete employee records.

Department Management:

Create, view, edit, and delete company departments.

Leave Management:

View all leave requests from employees.

Approve or reject pending leave requests.

Payroll Management:

Create and manage payroll records for employees.

Process payments and mark payrolls as "Paid".

Attendance Management:

View attendance records for all employees.

Manually add or correct attendance entries.

Announcements:

Create, view, edit, and delete company-wide announcements.

🧑‍💼 Employee Features
Dashboard: A personalized dashboard showing key stats like pending leave requests, approved leaves for the month, and total attendance days.

Leave Management:

Apply for leave through a simple form.

View the history and status of all their leave requests.

Attendance:

Clock in and clock out for the day.

View their own attendance history.

Payroll:

View a history of their payslips.

Download payslips in PDF format for their records.

Announcements:

View all company announcements posted by the admin.

Technologies Used
Backend: Django, Python 3.10

Frontend: HTML, Tailwind CSS, JavaScript

Database: SQLite (default, can be configured for others)

PDF Generation: xhtml2pdf

Setup and Installation
Follow these steps to get the project up and running on your local machine.


Install the required packages:

pip install -r requirements.txt

(Note: You will need to create a requirements.txt file by running pip freeze > requirements.txt in your project's terminal.)

Apply database migrations:

python manage.py migrate

Create a superuser (Admin):

python manage.py createsuperuser

Follow the prompts to create your admin account.

How to Run the Project
Start the development server:

python manage.py runserver

Open your browser and navigate to http://127.0.0.1:8000/.

You can now access the application:

Admin Login: Use the superuser credentials you created.

Employee Signup: Register as a new employee. Note that the admin will need to approve your account before you can log in to the employee dashboard.