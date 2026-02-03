import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Union
import logging

from config import settings

logger = logging.getLogger(__name__)

def create_contact_email_html(form_data) -> str:
    """Create HTML email for contact form submission"""
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #1976d2; border-bottom: 2px solid #1976d2; padding-bottom: 10px;">
                    New Contact Form Submission
                </h2>
                
                <div style="margin: 20px 0;">
                    <p><strong>Name:</strong> {form_data.name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{form_data.email}">{form_data.email}</a></p>
                    <p><strong>Phone:</strong> {form_data.phone}</p>
                    <p><strong>Type:</strong> {form_data.type}</p>
                </div>
                
                <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #555;">Message:</h3>
                    <p style="white-space: pre-wrap;">{form_data.message}</p>
                </div>
                
                <p style="color: #888; font-size: 12px; margin-top: 30px;">
                    This is an automated message from MedStat Contact Form.
                </p>
            </div>
        </body>
    </html>
    """

def create_demo_email_html(demo_data) -> str:
    """Create HTML email for demo request"""
    interests = demo_data.interests if demo_data.interests else "Not specified"
    
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #1976d2; border-bottom: 2px solid #1976d2; padding-bottom: 10px;">
                    🎯 New Demo Request
                </h2>
                
                <div style="margin: 20px 0;">
                    <p><strong>Name:</strong> {demo_data.name}</p>
                    <p><strong>Clinic/Organization:</strong> {demo_data.clinic}</p>
                    <p><strong>Role:</strong> {demo_data.role}</p>
                    <p><strong>Email:</strong> <a href="mailto:{demo_data.email}">{demo_data.email}</a></p>
                    <p><strong>Phone:</strong> {demo_data.phone}</p>
                </div>
                
                <div style="background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #1976d2;">Specific Interests:</h3>
                    <p style="white-space: pre-wrap;">{interests}</p>
                </div>
                
                <div style="background-color: #fff3e0; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>⏰ Action Required:</strong> Contact within 24 hours to schedule demo</p>
                </div>
                
                <p style="color: #888; font-size: 12px; margin-top: 30px;">
                    This is an automated message from MedStat Demo Request Form.
                </p>
            </div>
        </body>
    </html>
    """

async def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """
    Send email using SMTP
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML content of the email
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = settings.SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Connect to SMTP server and send
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

async def send_contact_notification(form_data) -> bool:
    """Send notification email for contact form submission"""
    subject = f"New Contact Form Submission from {form_data.name}"
    html_content = create_contact_email_html(form_data)
    
    return await send_email(
        to_email=settings.ADMIN_EMAIL,
        subject=subject,
        html_content=html_content
    )

async def send_demo_notification(demo_data) -> bool:
    """Send notification email for demo request"""
    subject = f"🎯 New Demo Request from {demo_data.clinic}"
    html_content = create_demo_email_html(demo_data)
    
    return await send_email(
        to_email=settings.ADMIN_EMAIL,
        subject=subject,
        html_content=html_content
    )
