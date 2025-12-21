"""
Reminders package.

This package contains modules for sending various types of reminders:
- Lead magnet reminders (after lesson click)
- Offer expiration reminders (last call and regular)

Main entry point: process_reminders() function from processor module.
"""
# Import all reminder sender functions for backward compatibility
from scheduler.reminders.lead_magnet import (
    send_first_lead_reminder,
    send_second_lead_reminder,
    send_third_lead_reminder,
    send_special_offer_reminder
)
from scheduler.reminders.offer_expiration import (
    send_last_call_reminder,
    send_regular_reminder
)
from scheduler.reminders.processor import process_reminders

# Export main function and all sender functions
__all__ = [
    'process_reminders',
    'send_first_lead_reminder',
    'send_second_lead_reminder',
    'send_third_lead_reminder',
    'send_special_offer_reminder',
    'send_last_call_reminder',
    'send_regular_reminder',
]

