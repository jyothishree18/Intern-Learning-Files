
# PATIENT EXCEPTIONS
class PatientNotFoundException(Exception):
    pass


class PatientAlreadyExistsException(Exception):
    pass


# REPORT EXCEPTIONS
class ReportNotFoundException(Exception):
    pass


# STAFF EXCEPTIONS
class StaffNotFoundException(Exception):
    pass


class StaffAlreadyExistsException(Exception):
    pass


class InvalidStaffRoleException(Exception):
    pass
