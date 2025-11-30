import pytest
from pydantic import ValidationError
from backend.api_gateway.models.schemas import (
    AssetCreate, 
    PriceHistoryResponse,
    UserResponse
)
from datetime import datetime

def test_asset_create_valid():
    """Test valid AssetCreate schema."""
    asset = AssetCreate(
        symbol="BTC",
        name="Bitcoin",
        description="Digital currency"
    )
    assert asset.symbol == "BTC"
    assert asset.name == "Bitcoin"

def test_asset_create_missing_symbol():
    """Test AssetCreate without symbol."""
    with pytest.raises(ValidationError):
        AssetCreate(name="Bitcoin", description="Digital currency")

def test_price_history_response():
    """Test PriceHistoryResponse schema."""
    price_data = {
        "id": 1,
        "asset_id": 1,
        "price": 45000.50,
        "timestamp": datetime.utcnow().isoformat()
    }
    price = PriceHistoryResponse(**price_data)
    assert price.price == 45000.50
    assert price.asset_id == 1