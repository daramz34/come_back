from pydantic import BaseModel, Field

class StudentCreate(BaseModel):
    first_name : str = Field(..., min_length=1, max_length=60)
    last_name : str = Field(..., min_length=1, max_length=60)
    matric_number : str = Field(..., min_length=1, max_length=15)
    gpa : float = Field(..., gt=0, lt=5.0)


class StudentResponse(BaseModel):
    id : int
    first_name : str
    last_name: str
    matric_number : str
    gpa : float
    is_active: bool

    class Config:
        from_attributes = True