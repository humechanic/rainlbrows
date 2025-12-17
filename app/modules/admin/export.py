"""
Admin functions for exporting database data to PDF
"""
from db.session import get_db_session
from db.models import User, Offer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime, timezone
import io
import logging

logger = logging.getLogger(__name__)


def export_users_to_pdf() -> io.BytesIO:
    """Export all users to PDF format"""
    db = get_db_session()
    try:
        users = db.query(User).order_by(User.created_at.desc()).all()
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Title
        story.append(Paragraph("Users Database", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Table data
        data = [['ID', 'Telegram ID', 'First Name', 'Nickname', 'Premium', 'Registration Date']]
        
        for user in users:
            created_at = user.created_at.strftime("%d.%m.%Y %H:%M") if user.created_at else "N/A"
            data.append([
                str(user.id),
                str(user.telegram_id),
                user.first_name or user.last_name or "N/A",
                user.nickname or "N/A",
                "Yes" if user.is_premium_tg_user else "No",
                created_at
            ])
        
        # Create table
        table = Table(data, colWidths=[0.5*inch, 1*inch, 1.2*inch, 1*inch, 0.6*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"Total users: {len(users)}", styles['Normal']))
        story.append(Paragraph(f"Export date: {datetime.now(timezone.utc).strftime('%d.%m.%Y %H:%M UTC')}", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        logger.error(f"Error exporting users to PDF: {e}", exc_info=True)
        raise
    finally:
        db.close()


def export_offers_to_pdf() -> io.BytesIO:
    """Export all offers to PDF format"""
    db = get_db_session()
    try:
        offers = db.query(Offer).order_by(Offer.created_at.desc()).all()
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=0.5*inch, leftMargin=0.5*inch)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Title
        story.append(Paragraph("Offers Database", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Table data
        data = [['ID', 'User ID', 'Telegram ID', 'Active', 'Expires', 'Lesson Clicked', 'Created']]
        
        for offer in offers:
            expiration = offer.offer_expiration_date.strftime("%d.%m.%Y %H:%M") if offer.offer_expiration_date else "N/A"
            clicked = offer.lesson_clicked_at.strftime("%d.%m.%Y %H:%M") if offer.lesson_clicked_at else "No"
            created = offer.created_at.strftime("%d.%m.%Y %H:%M") if offer.created_at else "N/A"
            telegram_id = str(offer.user.telegram_id) if offer.user and offer.user.telegram_id else "N/A"
            
            data.append([
                str(offer.id),
                str(offer.user_id),
                telegram_id,
                "Yes" if offer.is_active else "No",
                expiration,
                clicked,
                created
            ])
        
        # Create table
        table = Table(data, colWidths=[0.4*inch, 0.6*inch, 0.9*inch, 0.5*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"Total offers: {len(offers)}", styles['Normal']))
        active_count = sum(1 for o in offers if o.is_active)
        story.append(Paragraph(f"Active offers: {active_count}", styles['Normal']))
        story.append(Paragraph(f"Export date: {datetime.now(timezone.utc).strftime('%d.%m.%Y %H:%M UTC')}", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        logger.error(f"Error exporting offers to PDF: {e}", exc_info=True)
        raise
    finally:
        db.close()

