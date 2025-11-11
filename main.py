# Project - OTP verification app

import streamlit as st # for frontend
import smtplib         # send emails using smtp
import random          # for otp generation
import os              # accessing enviornment varible
import re
from email.mime.multipart import MIMEMultipart # to format email
from email.mime.text import MIMEText    # to add plain text in email
from dotenv import load_dotenv    # to load environment variable




# Accessing enviornment over here inside the code

load_dotenv()
EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

st.title("Email Verification")

# Intialize the OTP
if "otp" not in st.session_state:
    st.session_state.otp = None


with st.form("otp_form"):
    user_email = st.text_input("Enter your email address")
    send_clicked = st.form_submit_button("Send OTP")


    if send_clicked:
        email_valid = re.fullmatch(r"\b[a-zA-Z][a-zA-Z0-9]*@[a-zA-Z]+\.[a-zA-Z]{2,3}\b", user_email)

        if email_valid:
            st.success("✅ Email is valid. OTP sent successfully!")

        else:
            st.session_state.otp = random.randint(1000, 9999)


            body = f"OTP for Verification: {st.session_state.otp}"


            msg = MIMEMultipart()   # create a MIME message
            msg["from"] = EMAIL
            msg["to"] = user_email
            msg["Subject"] = "OTP to steal all your Money"
            msg.attach(MIMEText(body,"plain"))


            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(EMAIL,PASSWORD)
                server.send_message(msg)
                server.quit()


                st.success("OTP fired successfully")
            except:
                st.error("Authentication Fails OR Internet Issue or Enter a valid Email")


# verify the otp you enter is right or wrong

if st.session_state.otp:
    entered_otp = st.text_input("Enter OTP you received in Gmail")
    if st.button("Verify OTP"):
        if int(entered_otp) == st.session_state.otp:
            st.success("OTP Match")
        else:
            st.error("Wrong OTP")