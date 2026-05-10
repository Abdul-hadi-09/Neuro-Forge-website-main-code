import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone
from zoneinfo import ZoneInfo 
import smtplib
from email.message import EmailMessage


app = Flask(__name__)
app.secret_key = 'vzo oge dpc'
APP_PASSWORD = "qlrk vzjo ogme dpyc"
OWNER_EMAIL = "abdul.hadi7860109@gmail.com"


SPREADSHEET_ID = "1jmcqyTl7UHnO6Gr9R_fApYQRaSGc-Q0Jl0ueDPH4u44"
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
        "neuroforge-meetings-27f8e4c0ea86.json",
    scope)

client = gspread.authorize(creds)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

# (Portfolio routes remain the same...)
@app.route('/portfolio/hicare24')
def project_hicare24():
    return render_template('portfolio/project_hicare24.html')

@app.route('/portfolio/amazon-scraper')
def project_amazon_scraper():
    return render_template('portfolio/project_amazon_scraper.html')

@app.route('/portfolio/autosync')
def project_autosync():
    return render_template('portfolio/project_autosync.html')

@app.route('/portfolio/rideziarah')
def project_rideziarah():
    return render_template('portfolio/project_rideziarah.html')

@app.route('/portfolio/rideziarah-chatbot')
def project_rideziarah_chatbot():
    return render_template('portfolio/project_rideziarah_bot.html')

@app.route('/portfolio/zillow-scraper')
def project_zillow():
    return render_template('portfolio/project_zillow.html')

@app.route('/portfolio/instagram-scraper')
def project_instagram():
    return render_template('portfolio/project_instagram.html')

@app.route('/portfolio/linkedin-scraper')
def project_linkedin():
    return render_template('portfolio/project_linkedin.html')

@app.route('/portfolio/indeed-scraper')
def project_indeed():
    return render_template('portfolio/project_indeed.html')

# (Service routes remain the same...)
@app.route('/services/chatbots')
def service_chatbots():
    return render_template('service/service_chatbots.html')

@app.route('/services/lead-generation')
def service_lead_gen():
    return render_template('service/service_lead_gen.html')

@app.route('/services/web-development')
def service_web_dev():
    return render_template('service/service_web_dev.html')

@app.route('/services/ai-agents')
def service_ai_agents():
    return render_template('service/service_ai_agents.html')

@app.route('/services/web-scraping')
def service_scraping():
    return render_template('service/service_scraping.html')

@app.route('/services/automation')
def service_automation():
    return render_template('service/service_automation.html')

@app.route('/services/computer-vision')
def service_computer_vision():
    return render_template('service/service_computer_vision.html')

@app.route('/services/nlp')
def service_nlp():
    return render_template('service/service_nlp.html')

@app.route('/services/generative-ai')
def service_generative_ai():
    return render_template('service/service_generative_ai.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not name or not email or not subject or not message:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('contact'))

        try:
            date, time = datetime.now(ZoneInfo("Asia/Karachi")).strftime(
                "%Y-%m-%d %H:%M"
            ).split(" ")
            sheet2 = client.open_by_key(SPREADSHEET_ID).sheet1
            sheet2.insert_row([date, time, name, email, phone, subject, message], index=2)

            msg = EmailMessage()
            msg["From"] = OWNER_EMAIL
            msg["To"] = OWNER_EMAIL
            msg["Subject"] = "NeuroForge Contact Form Submission"
            msg["Reply-To"] = email

            msg.set_content(f"""
            New message from website contact form

            Name: {name}
            Subject: {subject}

            Email: {email}
            Phone: {phone}

            Message:
            {message}
            """)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(OWNER_EMAIL, APP_PASSWORD)
                server.send_message(msg)

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('contact'))

        return redirect(url_for('submitted'))

    return render_template('contact.html')

@app.route('/quote.html', methods=['GET', 'POST'])
def quote():
    if request.method == 'POST':
        # Step 1: Contact Info
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service_type = request.form.get('service_type')
        
        # Step 2: Service Details
        project_desc = request.form.get('project_desc')
        budget = request.form.get('budget')
        timeline = request.form.get('timeline')
        
        # Step 3: Final Details
        notes = request.form.get('notes')

        if not name or not email or not service_type or not project_desc:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('quote'))

        try:
            # Prepare message for email/sheet
            full_message = f"""
            Quote Request Details:
            
            -- Contact Info --
            Phone: {phone}
            Service: {service_type}
            
            -- Service Details --
            Budget: {budget}
            Timeline: {timeline}
            
            -- Project Description --
            {project_desc}
            
            -- Additional Notes --
            {notes}
            """

            dt = datetime.now(ZoneInfo("Asia/Karachi"))

            date = dt.strftime("%Y-%m-%d")     
            time = dt.strftime("%I:%M %p")       

            
            # Save to Sheets (concatenating all details into message column for now, 
            # or could expand sheet columns if user wants)
            sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Qoute Submission Data")
            sheet.insert_row([date, time, name, email, phone, service_type, budget, timeline, project_desc, notes], index=2)

            # Send Email
            msg = EmailMessage()
            msg["From"] = OWNER_EMAIL
            msg["To"] = OWNER_EMAIL
            msg["Subject"] = f"New {service_type} Quote Request from {name}"
            msg["Reply-To"] = email

            msg.set_content(f"""
            New Quote Request from Website
            
            Name: {name}
            Email: {email}
            
            {full_message}
            """)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(OWNER_EMAIL, APP_PASSWORD)
                server.send_message(msg)

            return redirect(url_for('submitted'))

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('quote'))

    return render_template('quote.html')

@app.route('/submitted')
def submitted():
    return render_template('submitted.html')

if __name__ == '__main__':
    app.run(debug=True)

