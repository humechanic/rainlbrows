# Reminders Module Structure

This package contains modules for sending various types of reminders to users.

## Module Structure

### `__init__.py`
Main entry point for the reminders package. Exports all public functions for backward compatibility.

**Exports:**
- `process_reminders()` - Main function to process all reminders
- `send_first_lead_reminder()` - Send first lead magnet reminder
- `send_second_lead_reminder()` - Send second lead magnet reminder
- `send_third_lead_reminder()` - Send third lead magnet reminder
- `send_last_call_reminder()` - Send last call reminder (before offer expiration)
- `send_regular_reminder()` - Send regular reminder about offer

### `lead_magnet/` (package)
Individual reminder functions organized by sequence:

**Files:**
- `first.py` - First reminder to watch lesson (1 hour after click)
- `second.py` - Urgency message reminder (after first)
- `third.py` - FAQ about intensive reminder (after second)
- `fourth.py` - Final push reminder (3 hours after second)
- `special_offer.py` - Special pricing reminder (1 hour after first)

**Functions:**
- `send_first_lead_reminder()` - Reminder to watch lesson
- `send_second_lead_reminder()` - Urgency message
- `send_third_lead_reminder()` - FAQ about intensive
- `send_fourth_lead_reminder()` - Final push reminder
- `send_special_offer_reminder()` - Special pricing offer

### `offer_expiration.py`
Functions for sending reminders about offer expiration.

**Functions:**
- `send_last_call_reminder()` - Last call before expiration (24-48 hours before)
- `send_regular_reminder()` - Regular reminder (more than 48 hours before)

### `processor.py`
Main processor that coordinates all reminders.

**Functions:**
- `process_reminders()` - Checks database and sends all pending reminders

## Usage

```python
# Import main processor function
from scheduler.reminders import process_reminders

# Or import specific reminder functions
from scheduler.reminders import send_first_lead_reminder
```

## Backward Compatibility

All imports from `scheduler.reminders` continue to work as before:
- `from scheduler.reminders import process_reminders` ✅
- `from scheduler.reminders import send_first_lead_reminder` ✅

