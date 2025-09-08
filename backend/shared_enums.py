import enum

class UserRole(str, enum.Enum):
    superadmin = "superadmin"
    admin = "admin"
    viewer = "viewer"
