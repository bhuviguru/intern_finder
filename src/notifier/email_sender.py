import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

class EmailSender:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.email = os.getenv('SMTP_EMAIL')
        self.password = os.getenv('SMTP_PASSWORD')
        self.logger = logging.getLogger(self.__class__.__name__)

    def send_email(self, recipient_email, subject, body):
        if not self.email or not self.password:
            self.logger.warning("SMTP credentials not set. Skipping email.")
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'html'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            self.logger.info(f"Email sent to {recipient_email}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False

    def generate_daily_report_html(self, jobs, answer_gen=None):
        html = "<h2>🔥 Top Internship Matches</h2>"
        
        for i, job in enumerate(jobs, 1):
            answers = {}
            if answer_gen:
                answers = answer_gen.generate_answers(job.__dict__)
            
            html += f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 8px;">
                <h3 style="margin-top: 0;">{i}. {job.role} <span style="font-weight:normal; font-size: 0.9em;">at {job.company}</span></h3>
                <p>
                    💰 <strong>{job.stipend}</strong> | 📍 {job.location} | Score: {job.score}
                </p>
                
                <div style="background-color: #f9f9f9; padding: 10px; margin-top: 10px; border-left: 4px solid #007bff;">
                    <strong>📋 Ready-to-use Answers:</strong><br><br>
                    
                    <em>1. Why should we hire you?</em><br>
                    <div style="background: #fff; padding: 8px; border: 1px dashed #ccc; margin: 5px 0;">
                        {answers.get('why_hire_me', 'N/A')}
                    </div>
                    
                    <em>2. Why do you want to join?</em><br>
                    <div style="background: #fff; padding: 8px; border: 1px dashed #ccc; margin: 5px 0;">
                        {answers.get('why_join', 'N/A')}
                    </div>
                </div>

                <div style="margin-top: 15px;">
                    <a href="{job.link}" style="background-color: #28a745; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; font-weight: bold;">✅ Apply Now</a>
                </div>
            </div>
            """
        return html
