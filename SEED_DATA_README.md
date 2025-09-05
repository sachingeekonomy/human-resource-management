# Database Seeding Commands

This document explains how to use the Django management commands to seed your Employee Management System database with sample data.

## Available Commands

### 1. Seed Data Command
Populates the database with sample data including:
- 5 departments
- 5 employees
- Leave records
- Attendance records
- Announcements
- Payroll records

**Usage:**
```bash
python manage.py seed_data
```

**What it creates:**
- **Departments**: Human Resources, Information Technology, Finance, Marketing, Operations
- **Employees**: 
  - John Doe (HR) - $45,000/year
  - Jane Smith (IT) - $55,000/year
  - Mike Johnson (Finance) - $48,000/year
  - Sarah Wilson (Marketing) - $52,000/year
  - David Brown (Operations) - $46,000/year
- **Default Password**: `password123` for all employees
- **Leave Records**: 1-3 random leave records per employee
- **Attendance**: 30 days of attendance records (weekdays only)
- **Announcements**: 5 company announcements
- **Payroll**: 6 months of payroll records

### 2. Clear Data Command
Removes all seeded data from the database.

**Usage:**
```bash
# Clear all data including employees
python manage.py clear_data

# Clear data but keep admin users
python manage.py clear_data --keep-admin
```

## Prerequisites

Before running the seed commands, ensure:
1. Django is properly installed
2. Database migrations have been applied
3. You're in the project directory

## Running the Commands

1. **Navigate to your project directory:**
   ```bash
   cd employeemanagementsystem-main
   ```

2. **Apply migrations (if not done already):**
   ```bash
   python manage.py migrate
   ```

3. **Seed the database:**
   ```bash
   python manage.py seed_data
   ```

4. **Optional: Clear data when needed:**
   ```bash
   python manage.py clear_data
   ```

## Sample Data Details

### Departments
- Human Resources
- Information Technology  
- Finance
- Marketing
- Operations

### Employee Credentials
All employees use the password: `password123`

| Username | Name | Department | Salary | Experience |
|----------|------|------------|---------|------------|
| john.doe | John Doe | HR | $45,000 | 3 years |
| jane.smith | Jane Smith | IT | $55,000 | 5 years |
| mike.johnson | Mike Johnson | Finance | $48,000 | 2 years |
| sarah.wilson | Sarah Wilson | Marketing | $52,000 | 4 years |
| david.brown | David Brown | Operations | $46,000 | 3 years |

### Generated Data
- **Leave Records**: Random dates, reasons, and statuses
- **Attendance**: Realistic clock-in/out times for weekdays
- **Announcements**: Company-related announcements
- **Payroll**: Monthly salary calculations for the past 6 months

## Notes

- The commands use `get_or_create()` to avoid duplicate data
- All employees are automatically approved (`is_approved=True`)
- Attendance records skip weekends
- Payroll records are calculated as monthly salary (annual salary ÷ 12)
- The seed command can be run multiple times safely

## Troubleshooting

If you encounter issues:

1. **Check Django version compatibility**
2. **Ensure all models are properly imported**
3. **Verify database connection**
4. **Check if migrations are up to date**

For more help, check the Django documentation or run:
```bash
python manage.py help seed_data
python manage.py help clear_data
```
