import smtplib
from email.message import EmailMessage
import time as t
import os
from dotenv import load_dotenv

load_dotenv()

def bill_and_email():
    order_id=int(input("Enter order id: "))
    product_name=input("Enter product name: ")
    p_price=float(input("Enter product price: "))
    p_quantity=int(input("Enter product quantity: "))

    amount=p_price*p_quantity

    idname = str(order_id)
    ordertime=t.ctime()

    x = open(f"{idname}.txt", "w", encoding="utf-8")
    x.write(f"""
╭──────────────────────────────────────────╮
│              BILL RECEIPT                │
├──────────────────────────────────────────┤
│ Order ID    : {order_id:<27}│
│ Product     : {product_name:<27}│
│ Quantity    : {p_quantity:<27}│
│ Unit Price  : ₹{p_price:<26.2f}│
├──────────────────────────────────────────┤
│ TOTAL       : ₹{amount:<26.2f} │
├──────────────────────────────────────────┤
│ {ordertime:<40}│
╰──────────────────────────────────────────╯

        Thank you for your purchase!
""")
    x.close()

    receiver_email = input("Enter customer email: ")
    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("PASSWORD") # Gmail App Password


    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Your Bill Receipt"
    msg.set_content("""
    Hello,
    Please find your bill attached with this email.
    Thank you for your purchase.
    """)

    with open(f"{idname}.txt", "rb") as file:
        msg.add_attachment(
            file.read(),
            maintype="text",
            subtype="plain",
            filename=f"{idname}"
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print("Bill sent successfully!")

    except Exception as e:
        print("Failed to send email:", e)
    
bill_and_email()
