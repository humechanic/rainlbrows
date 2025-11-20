# Promocode configuration
# Format: {promocode: discount_value}
# If discount_value contains '%' - it's percentage discount (e.g., "10%" = 10% off)
# If discount_value is a number without '%' - it's fixed amount discount in cents (e.g., "5000" = 50.00 BYN off)
PROMOCODES = {
    "МАРАФОН": "6000", 
    "МАРАФОН20": "20%",   # 20% discount
    "МАРАФОН15": "15%",   # 15% discount
    # Example of fixed discount: "МАРАФОН5000": "5000"  # 50.00 BYN fixed discount
}

def is_percentage_discount(discount_value: str) -> bool:
    """Check if discount is percentage (contains %)"""
    return "%" in discount_value

def get_discount_value(promocode: str) -> str:
    """Get discount value for promocode, returns empty string if not found"""
    return PROMOCODES.get(promocode.upper(), "")

def is_valid_promocode(promocode: str) -> bool:
    """Check if promocode exists"""
    return promocode.upper() in PROMOCODES

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

