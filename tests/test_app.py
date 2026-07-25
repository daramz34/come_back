import pytest
import sys
import os
from fastapi.testclient import TestClient


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "...")))
from error_project.main import app

def validate_price(price:float) -> bool:
    """Helper function simulating product price validation logic."""
    if price < 0:
        raise ValueError("Price cannot be negative")
    return True

def test_unit_price_cannot_be_negative():
    """Unit Test 1: Ensure negative price raise ValueError"""

    with pytest.raises(ValueError, match="Price cannot be negative"):
        validate_price(-10.0)


def test_unit_price_postive_valid():
    """Unit Test 2: Ensure Valid/Postive price passes"""
    assert validate_price(25.50) is True



def test_unit_price_zero_valid():
    """Unit Test 3: Ensure zero price (free item) passes"""
    assert validate_price(0.0) is True



client = TestClient(app)

def test_integration_singup_or_health():
    """Integration Test: Simulates hitting an API route"""
    response = client.get("/")


    assert response.status_code in [200, 404]