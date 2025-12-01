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

## SQL Init File Description



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

