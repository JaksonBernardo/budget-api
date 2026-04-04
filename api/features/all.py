from enum import Enum

class UserFeature(str, Enum):
    CREATE = "CREATE_USER"
    UPDATE = "UPDATE_USER"
    DELETE = "DELETE_USER"
    READ = "READ_USER"

class SegmentFeature(str, Enum):
    CREATE = "CREATE_SEGMENT"
    UPDATE = "UPDATE_SEGMENT"
    DELETE = "DELETE_SEGMENT"
    READ = "READ_SEGMENT"

class ClientFeature(str, Enum):
    CREATE = "CREATE_CLIENT"
    UPDATE = "UPDATE_CLIENT"
    DELETE = "DELETE_CLIENT"
    READ = "READ_CLIENT"

class SupplierFeature(str, Enum):
    CREATE = "CREATE_SUPPLIER"
    UPDATE = "UPDATE_SUPPLIER"
    DELETE = "DELETE_SUPPLIER"
    READ = "READ_SUPPLIER"

class MaterialFeature(str, Enum):
    CREATE = "CREATE_MATERIAL"
    UPDATE = "UPDATE_MATERIAL"
    DELETE = "DELETE_MATERIAL"
    READ = "READ_MATERIAL"


