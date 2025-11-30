# Clinic Appointment and Check-in Management System
*A Flask-based clinical workflow management application for IA637.*

---

##  Overview
This web application manages clinic workflows, including:

- User login (Doctor, Patient)
- Patient account access
- Appointment requests
- Doctor confirmation workflow
- Room assignment
- Check-in & check-out tracking

It follows the CRUD structure taught in class and uses clean, modular entity classes that map directly to database tables.

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

