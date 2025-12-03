from baseObject import baseObject

class appointment(baseObject):
    def __init__(self):
        self.setup()

    # ------------------------------------------------------------
    # BASIC CRUD + SELECT METHODS
    # ------------------------------------------------------------

    def getAll(self):
        sql = """
            SELECT 
                a.*,
                p.name AS patient_name,
                d.name AS doctor_name
            FROM appointment a
            LEFT JOIN user p ON a.patientid = p.uid
            LEFT JOIN user d ON a.doctorid = d.uid
            ORDER BY a.date, a.time
        """
        self.cur.execute(sql)
        self.data = self.cur.fetchall()


    def getByField(self, field, value):
        sql = f"""
            SELECT 
                a.*,
                p.name AS patient_name,
                d.name AS doctor_name
            FROM appointment a
            LEFT JOIN user p ON a.patientid = p.uid
            LEFT JOIN user d ON a.doctorid = d.uid
            WHERE a.{field} = %s
            ORDER BY a.date, a.time
        """
        self.cur.execute(sql, (value,))
        self.data = self.cur.fetchall()
    

    def getUpcomingForPatient(self, uid):
        sql = """
            SELECT 
                a.*, 
                p.name AS patient_name, 
                d.name AS doctor_name
            FROM appointment a
            LEFT JOIN user p ON a.patientid = p.uid
            LEFT JOIN user d ON a.doctorid = d.uid
            WHERE a.patientid = %s
            AND a.date >= CURDATE()
            ORDER BY a.date, a.time
            LIMIT 1
        """
        self.cur.execute(sql, (uid,))
        self.data = self.cur.fetchall()


    def verify_new(self):
        self.errorList = []

        if not self.data[0].get('date'):
            self.errorList.append("Date is required.")

        if not self.data[0].get('time'):
            self.errorList.append("Time is required.")

        if self.data[0].get('patientid') is None:
            self.errorList.append("Patient is required.")

        return len(self.errorList) == 0


    def verify_update(self):
        self.errorList = []

        if not self.data[0].get('date'):
            self.errorList.append("Date is required.")

        if not self.data[0].get('time'):
            self.errorList.append("Time is required.")

        if self.data[0].get('status') == "confirmed" and not self.data[0].get('doctorid'):
            self.errorList.append("Doctor must be assigned for a confirmed appointment.")

        return len(self.errorList) == 0

       # ------------------------------------------------------------
    # ANALYTICS 
    # ------------------------------------------------------------

    # 1. Daily Appointment Count
    def daily_appointment_count(self):
        sql = """
            SELECT 
                date AS day,
                COUNT(*) AS total
            FROM appointment
            GROUP BY date
            ORDER BY date;
        """
        self.cur.execute(sql)
        return self.cur.fetchall()

    # 2. Doctor Appointment Volume (Last 30 Days)
    def doctor_volume_last_30_days(self):
        sql = """
            SELECT
                u.name AS doctor_name,
                COUNT(a.aid) AS total
            FROM appointment a
            JOIN user u ON a.doctorid = u.uid
            WHERE a.date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            GROUP BY a.doctorid
            ORDER BY total DESC;
        """
        self.cur.execute(sql)
        return self.cur.fetchall()

    # 3. Appointment Check-In Conversion Rate
    def checkin_conversion_rate(self):
        sql = """
            SELECT 
                (SELECT COUNT(*) FROM checkin) /
                (SELECT COUNT(*) FROM appointment) AS rate;
        """
        self.cur.execute(sql)
        row = self.cur.fetchone()
        return row['rate'] if row else 0

    # 4. Hourly Appointment Distribution
    def hourly_appointment_distribution(self):
        sql = """
            SELECT 
                HOUR(STR_TO_DATE(time, '%H:%i')) AS hour,
                COUNT(*) AS total
            FROM appointment
            GROUP BY hour
            ORDER BY hour;
        """
        self.cur.execute(sql)
        return self.cur.fetchall()
