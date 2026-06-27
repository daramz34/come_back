from pydantic import BaseModel, Field

# Inbound validation schema (Day 9 POST)
class ItemCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    price: float = Field(..., gt=0)

# Outbound response filter (Day 8 GET)
class ItemResponseDTO(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True