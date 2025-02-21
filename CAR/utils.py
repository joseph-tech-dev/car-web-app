import io
import os
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings

def generate_payment_receipt(transaction):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A5)
    pdf.setTitle(f"Receipt_{transaction.id}.pdf")

    # Set background color
    pdf.setFillColor(colors.HexColor("#AEB6C3"))
    pdf.rect(0, 0, A5[0], A5[1], fill=1)

    # Logo Path
    logo_filename = "logo.jpeg"
    logo_path = os.path.join(settings.STATIC_ROOT, logo_filename)

    if os.path.exists(logo_path):
        try:
            logo = ImageReader(logo_path)
            pdf.drawImage(logo, A5[0] - 150, 520, width=100, height=50, preserveAspectRatio=True)
        except Exception as e:
            print(f"Error loading logo: {e}")
    else:
        print(f"Logo file '{logo_filename}' not found.")
    
    
    font_filename = "AnastasiaScript-Regular.ttf"
    font_path = os.path.join(settings.STATIC_ROOT, font_filename)  # Use settings.STATIC_ROOT

    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('AnastasiaScript', font_path))
    else:
        print(f"Font file '{font_filename}' not found at {font_path}") #Print the path to help debugging



    # Company Header
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 550, "HotWheelsIQ")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 535, "123 Auto Street, City, Country")
    pdf.drawString(50, 520, "support@hotwheelsiq.com")

    # Transaction Details Table
    data = [
        ["Transaction ID:", transaction.id],
        ["Buyer Name:", transaction.buyer.username],
        ["Car Model:", f"{transaction.car.make} {transaction.car.model}"],
        ["Amount Paid:", f"${transaction.amount}"],
        ["Payment Status:", transaction.status],
    ]

    table = Table(data, colWidths=[120, 180])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    table.wrapOn(pdf, 50, 400)
    table.drawOn(pdf, 50, 390)

    # Thank You Message
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 360, "Thank you for your purchase! If you have any questions,")
    pdf.drawString(50, 345, "please contact our support team.")

    # Footer (Signature Area)
    pdf.line(50, 310, 200, 310)  # Signature Line
    pdf.drawString(50, 295, "Authorized Signature")

    pdfmetrics.registerFont(TTFont('AnastasiaScript', 'AnastasiaScript-Regular.ttf'))  # Replace with actual path if needed
    pdf.setFont('AnastasiaScript', 12)  # Adjust font size as needed
    pdf.drawString(50, 320, "ApprovedHotWheelsIQ")  # Adjust position as needed


    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer