# Promocode configuration
# Format: {promocode: discount_value}
# If discount_value contains '%' - it's percentage discount (e.g., "10%" = 10% off)
# If discount_value is a number without '%' - it's fixed amount discount in cents (e.g., "5000" = 50.00 BYN off)
PROMOCODES = {
    "МАРАФОН": "6000",  # 60 BYN fixed discount
    "МАРАФОН20": "20%",   # 20% discount
    "МАРАФОН15": "15%",   # 15% discount
    "УРОК": "6000",  # 60 BYN fixed discount (290 instead of 350 BYN)
    # Example of fixed discount: "МАРАФОН5000": "5000"  # 50.00 BYN fixed discount
}

def is_percentage_discount(discount_value: str) -> bool:
    """Check if discount is percentage (contains %)"""
    return "%" in discount_value

def get_discount_value(promocode: str) -> str:
    """Get discount value for promocode, returns empty string if not found"""
    return PROMOCODES.get(promocode.upper(), "")

def is_valid_promocode(promocode: str, user_id: int = None, db_session = None) -> bool:
    """Check if promocode exists and is valid
    
    Args:
        promocode: Promocode to check
        user_id: Optional user ID to check offer expiration for "УРОК" promocode
        db_session: Optional database session to check offer expiration
    
    Returns:
        True if promocode is valid, False otherwise
    """
    promocode_upper = promocode.upper()
    
    # Check if promocode exists
    if promocode_upper not in PROMOCODES:
        return False
    
    # Special check for "УРОК" promocode - must check offer expiration
    if promocode_upper == "УРОК":
        if user_id is None or db_session is None:
            # If no user_id or db_session provided, we can't validate - return False for safety
            return False
        
        # Check if user has active offer that hasn't expired
        from db.repository import get_active_offer_for_user
        from datetime import datetime, timezone
        
        offer = get_active_offer_for_user(db_session, user_id)
        if not offer:
            return False
        
        # Check if offer has expired
        now = datetime.now(timezone.utc)
        if offer.offer_expiration_date < now:
            return False
    
    return True

def calculate_discount_amount(base_price: int, discount_value: str) -> int:
    """Calculate discount amount based on discount value (percentage or fixed)"""
    if not discount_value:
        return 0
    
    if is_percentage_discount(discount_value):
        # Percentage discount: "10%" -> 10
        percent = int(discount_value.replace("%", ""))
        return int(base_price * percent / 100)
    else:
        # Fixed discount: "5000" -> 5000 (in cents)
        return int(discount_value)

def calculate_final_price(base_price: int, discount_value: str) -> int:
    """Calculate final price after discount"""
    discount_amount = calculate_discount_amount(base_price, discount_value)
    return max(0, base_price - discount_amount)  # Ensure price is not negative

