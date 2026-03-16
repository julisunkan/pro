import io
from fpdf import FPDF


def export_email_txt(subject: str, body: str):
    """Return (content_str, mimetype, filename) for TXT export."""
    content = f"Subject: {subject}\n\n{body}"
    return content, 'text/plain', 'email.txt'


def export_email_html(subject: str, body: str):
    """Return (content_str, mimetype, filename) for HTML export."""
    body_html = body.replace('\n', '<br>')
    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{subject}</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; color: #333; }}
    h2 {{ border-bottom: 1px solid #eee; padding-bottom: 8px; }}
    p {{ line-height: 1.6; }}
  </style>
</head>
<body>
  <h2>{subject}</h2>
  <p>{body_html}</p>
</body>
</html>"""
    return content, 'text/html', 'email.html'


def export_email_pdf(subject: str, body: str):
    """Return (bytes, mimetype, filename) for PDF export."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 14)
    pdf.multi_cell(0, 8, f'Subject: {subject}')
    pdf.ln(4)
    pdf.set_font('Helvetica', '', 11)
    # Split body into lines to handle encoding
    for line in body.split('\n'):
        # Replace non-latin chars with closest ASCII
        safe_line = line.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 6, safe_line)
    pdf_bytes = pdf.output()
    return bytes(pdf_bytes), 'application/pdf', 'email.pdf'
