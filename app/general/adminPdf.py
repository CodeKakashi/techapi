from flask_restful import Resource
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from app.config import G_TEMP_PATH
from reportlab.lib.units import inch


class GeneratePdf(Resource):
    def get(self):
        user_data_json = [
            {"name": "User1", "due_date": "2024-04-15", "paid": False},
            {"name": "User2", "due_date": "2024-04-10", "paid": True},
            {"name": "User3", "due_date": "2024-04-20", "paid": False},
        ]

        fileName = f"{G_TEMP_PATH}/payment_details.pdf"
        create_payment_pdf(user_data_json, fileName)


def create_payment_pdf(users, output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    elements = []

    title_style = ParagraphStyle(name="TitleStyle", fontSize=20, alignment=1)
    title = Paragraph("Payment Details", title_style)
    elements.append(title)
    elements.append(Spacer(1, 1 * inch))

    data = [["Name", "Due Date", "Is Paid"]]

    for user in users:
        data.append([user["name"], user["due_date"], "Yes" if user["paid"] else "No"])

    table_width = letter[0] - 80
    table = Table(data, colWidths=[table_width / 3] * 3)

    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    table.setStyle(style)
    elements.append(table)

    doc.build(elements)



