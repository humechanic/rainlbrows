"""
Lead magnet reminders package.

This package contains individual reminder functions for lead magnet sequence:
- First reminder: Watch lesson reminder
- Second reminder: Urgency message
- Third reminder: FAQ about intensive
- Fourth reminder: Final push
- Special offer: Special pricing reminder
"""
from scheduler.reminders.lead_magnet.first import send_first_lead_reminder
from scheduler.reminders.lead_magnet.second import send_second_lead_reminder
from scheduler.reminders.lead_magnet.third import send_third_lead_reminder
from scheduler.reminders.lead_magnet.fourth import send_fourth_lead_reminder
from scheduler.reminders.lead_magnet.special_offer import send_special_offer_reminder

__all__ = [
    'send_first_lead_reminder',
    'send_second_lead_reminder',
    'send_third_lead_reminder',
    'send_fourth_lead_reminder',
    'send_special_offer_reminder',
]

