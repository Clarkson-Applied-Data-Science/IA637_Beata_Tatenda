from baseObject import baseObject

class checkin(baseObject):

    def __init__(self):
        self.setup()


    def verify_new(self):
        self.errors = []

        d = self.data[0]

        required = ['aid', 'uid', 'rid', 'status', 'checkintime']
        for r in required:
            if d.get(r) in [None, ""]:
                self.errors.append(f"{r} is required.")


        return len(self.errors) == 0

    def verify_update(self):
        self.errors = []

        d = self.data[0]

        required = ['aid', 'uid', 'rid', 'status', 'checkintime']
        for r in required:
            if d.get(r) in [None, ""]:
                self.errors.append(f"{r} is required.")

        return len(self.errors) == 0
