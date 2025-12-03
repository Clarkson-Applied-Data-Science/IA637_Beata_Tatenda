from baseObject import baseObject

class room(baseObject):
    def __init__(self):
        super().setup()

    def verify_new(self):
        self.errors = []

        r = self.data[0]

        if r.get("roomtype") in [None, ""]:
            self.errors.append("Room type is required.")

        if r.get("roomnumber") in [None, ""]:
            self.errors.append("Room number is required.")

        sql = "SELECT * FROM room WHERE roomnumber = %s;"
        self.cur.execute(sql, [r["roomnumber"]])
        if self.cur.fetchone():
            self.errors.append("Room number already exists.")

        return len(self.errors) == 0

    def verify_update(self):
        self.errors = []

        r = self.data[0]

        if r.get("roomtype") in [None, ""]:
            self.errors.append("Room type is required.")

        if r.get("roomnumber") in [None, ""]:
            self.errors.append("Room number is required.")

        sql = "SELECT * FROM room WHERE roomnumber = %s AND rid != %s;"
        self.cur.execute(sql, [r["roomnumber"], r[self.pk]])
        if self.cur.fetchone():
            self.errors.append("Another room already uses this number.")

        return len(self.errors) == 0
