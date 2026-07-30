from enum import Enum

class TodoStatus(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"

class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"