# Clinic Appointment and Check-in Management System
# Final Project – IA 637 / Clarkson University
Group Members:

Beata Tatenda Moyo

Tatenda Munaki

---

##  Overview

The Clinic Appointment & Check-In Management System is a full-stack web application designed to streamline how clinics manage patient bookings, doctor schedules, and check-in workflows. The system supports two primary user roles—patients and doctors—and provides role-based functionality to ensure an efficient and secure medical appointment experience.

This project was developed using the Flask web framework, following the same object-oriented structure used in class (with baseObject, entity classes, SQL scripts, and Jinja templates). It demonstrates core software engineering concepts including CRUD operations, relational database management, authentication, analytics, and dynamic visualizations.

The application features a complete appointment workflow:

Patients can:

Create an account and log in

Book appointments with available doctors

View upcoming appointments

Self-check-in when they arrive at the clinic

Doctors can:

View patient appointment lists

Confirm check-ins and manage appointment statuses

Update appointment details

Access a full Analytics Dashboard with real data visualizations

Administrators / Doctors also get a dedicated dashboard showing:

Daily appointment volume

Doctor appointment volume over the last 30 days

Patient check-in conversion rate

Most common appointment times (hourly distribution)

These analytics help the clinic understand patient behavior, doctor workload, and peak traffic times, allowing them to improve efficiency and resource allocation.

The system uses a relational MySQL database with four main tables:

user – Stores login credentials, names, and roles (doctor or patient)

appointment – Records appointment date, time, patient, doctor, and status

checkin – Tracks patient check-in activity

room – Stores clinic room information (optional for future features)

The front-end is implemented using standard HTML and CSS, with dynamic server-side rendering using Jinja templates. The analytics charts are generated using Matplotlib and stored as static PNG files.

This project demonstrates a complete, user-centered appointment workflow from registration → booking → check-in → doctor confirmation → data analytics, making it an excellent foundation for a more advanced healthcare management system or a future capstone project
---

##  Relational Schema
<img width="1110" height="644" alt="image" src="https://github.com/user-attachments/assets/d3ed120a-8c60-45de-b1a8-83eea5a866e0" />

---

##  Test Login Credentials

### **Doctor Account**
| Field | Value |
|-------|-------|
| Email | **beata@clarkson.edu** |
| Password | **1234** |

### **Patient Account**
| Field | Value |
|-------|-------|
| Email | **tatenda@clarkson.edu** |
| Password | **1234** |

---

---

##  Getting Started (Setup Instructions)
1. Download or Clone the Project

Clone the repository or download the ZIP file:

2. Configure the Database

Open your MySQL or phpMyAdmin environment.

Create a new database (your project used one like ia637_clinicappointment).

Run the SQL script provided in:DB_mysql.sql

3. Add Your Database Credentials
In the project folder, locate: config_example.yml
Make a copy and rename it: config.yml
Then fill in your MySQL login details:
   database:
  host: "localhost"
  user: "root"
  password: "your_password_here"
  database: "ia637_clinicappointment"

4. Run the Application
Navigate to the project folder and open your terminal: python app.py
You will see output like:  Running on http://127.0.0.1:5000

5.Open the Application in the Browser
http://127.0.0.1:5000
This loads the login page.
Use any of the preset demo accounts created during initialization.

6.Using the Application
Patients can create an account, book appointments, and check in.
Doctors can view schedules, manage check-ins, confirm appointments, and access the Analytics Dashboard.
The dashboard automatically generates visual charts stored in: /static/analytics/





---

## Analytical SQL Queries
Our system includes an analytics dashboard that provides operational insights into clinic performance. The dashboard includes four analytical queries, each designed to support scheduling decisions, workload balancing, and patient flow management.

1. Daily Appointment Count

Shows how many appointments occur on each day. Used to understand clinic workload patterns and identify high-traffic or slow days.

2. Doctor Appointment Volume (With Time Normalization)

Counts the number of appointments per doctor within a recent time window (e.g., last 30 days). This avoids bias toward older doctors with longer history and highlights trending or high-performing providers.

3. Appointment Check-In Conversion Rate

Shows the percentage of appointments that successfully result in a patient check-in. Helps identify no-show problems, communication issues, and the effectiveness of reminder systems.

4. Most Common Appointment Times (Time-of-Day Distribution)

Groups appointments by hour of the day to determine peak times and patient preferences. Useful for staffing, scheduling, and room allocation.

Each query is implemented in the appointment class, and results are displayed on the analytics dashboard using tables and charts.
