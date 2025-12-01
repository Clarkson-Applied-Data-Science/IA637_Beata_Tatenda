# Clinic Appointment and Check-in Management System
# Final Project – IA 637 / Clarkson University
Group Members:

Beata Tatenda Moyo

Tatenda Munaki

---

##  Overview
This web application is a full CRUD clinic appointment management system designed for doctors and patients. It allows patients to book appointments, check in for their visits, and view their appointment history. Doctors can manage patient appointments, view schedules, and update patient check-ins.

The system also includes an administrative analytics dashboard that provides insights into clinic operations, such as daily appointments, most-requested doctors, patient traffic patterns, and check-in activity rates
---

##  Features

###  Doctor Capabilities
- View **requested** appointments
- Confirm appointments (assign time, duration, doctor)
- Manage users
- Manage rooms
- View check-ins

### Patient Capabilities
- Log in
- Request appointments
- View personal appointment history
- Check in (optional) on arrival

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

## 🗄 Database Schema

### **1. `user` Table**

| Field | Type | Description |
|-------|-------|-------------|
| uid | int | Primary key |
| name | varchar(50) | Full name |
| email | varchar(50) | Login email |
| role | varchar(25) | doctor / patient |
| password | varchar(100) | Hashed password |
| specialty | varchar(50) | Doctor specialty (optional) |

---

### **2. `appointment` Table**

| Field | Type | Description |
|-------|-------|-------------|
| aid | int | Primary key |
| date | date | Appointment date |
| time | varchar(20) | Time of appointment |
| duration | int | Duration in minutes |
| status | varchar(20) | requested / confirmed |
| patientid | int | FK → user.uid (patient) |
| doctorid | int | FK → user.uid (doctor) |

---

### **3. `checkin` Table**

| Field | Type | Description |
|-------|-------|-------------|
| cid | int | Primary key |
| checkintime | varchar(25) | Time patient checked in |
| checkouttime | varchar(25) | Time patient checked out |
| status | varchar(25) | waiting / completed |
| aid | int | FK → appointment.aid |
| uid | int | FK → user.uid (staff handling check-in) |
| rid | int | FK → room.rid |

---

### **4. `room` Table**

| Field | Type | Description |
|-------|-------|-------------|
| rid | int | Primary key |
| roomtype | varchar(50) | exam / triage / lab |
| roomnumber | varchar(50) | Room identifier |

---

##  Appointment Workflow 

1️⃣ **Patient submits a new appointment request**  
- Patient cannot choose doctor  
- Form auto-assigns `patientid` using session  
- `status = "requested"` by default  

2️⃣ **Doctor/Admin views all `requested` appointments**  
- Can assign doctor  
- Can modify date/time/duration  
- Can update status to `confirmed`

3️⃣ **Confirmed appointments appear on both dashboards**  

4️⃣ **Patient arrives → performs check-in**  
- Check-in time recorded  
- Staff can check them out later  
- Metrics used for analytics (wait times, throughput)

---

## 📁 Project Structure

