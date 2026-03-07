import os
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import qrcode
import tempfile

CERTIFICATE_MILESTONES = {
    "Cultural Guardian": 300,
    "Sanskriti Master": 600
}

def get_certificates_dir():
    current_dir = Path(__file__).resolve().parent
    certs_dir = current_dir.parent.parent / "assets" / "certificates"
    certs_dir.mkdir(parents=True, exist_ok=True)
    return certs_dir

def generate_certificate(user_id, level):
    if level not in CERTIFICATE_MILESTONES:
        return None
        
    certs_dir = get_certificates_dir()
    filepath = certs_dir / f"{user_id}_{level.replace(' ', '_')}_certificate.pdf"
    
    # Generate QR Code
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(f"Verified Sanskriti AI Certificate\nUser: {user_id}\nLevel: {level}")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_qr:
        qr_img.save(temp_qr.name)
        temp_qr_path = temp_qr.name

    # Create PDF
    width, height = landscape(A4)
    c = canvas.Canvas(str(filepath), pagesize=landscape(A4))
    
    # Outer Border
    c.setStrokeColor(HexColor("#C9A84C")) # Gold
    c.setLineWidth(10)
    c.rect(0.5*inch, 0.5*inch, width - 1*inch, height - 1*inch)
    
    # Inner Border
    c.setLineWidth(2)
    c.rect(0.6*inch, 0.6*inch, width - 1.2*inch, height - 1.2*inch)
    
    # Title
    c.setFont("Helvetica-Bold", 40)
    c.setFillColor(HexColor("#1A0E30"))
    c.drawCentredString(width/2.0, height - 2*inch, "CERTIFICATE OF ACHIEVEMENT")
    
    # Subtitle
    c.setFont("Helvetica", 20)
    c.setFillColor(HexColor("#8A7560"))
    c.drawCentredString(width/2.0, height - 2.8*inch, "Sanskriti AI - Cultural Explorer Program")
    
    # Content
    c.setFont("Helvetica", 24)
    c.setFillColor(HexColor("#1A0E30"))
    c.drawCentredString(width/2.0, height - 4*inch, "This is to certify that")
    
    # User ID
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(HexColor("#D4893F"))
    c.drawCentredString(width/2.0, height - 4.8*inch, user_id.replace("_", " ").title())
    
    # Achievement
    c.setFont("Helvetica", 24)
    c.setFillColor(HexColor("#1A0E30"))
    c.drawCentredString(width/2.0, height - 5.8*inch, f"has successfully achieved the rank of")
    
    # Level
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(HexColor("#C9A84C"))
    c.drawCentredString(width/2.0, height - 6.5*inch, level.upper())
    
    # QR Code
    c.drawImage(temp_qr_path, width - 2.5*inch, 0.8*inch, width=1.2*inch, height=1.2*inch)
    
    # Verification text
    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor("#8A7560"))
    c.drawCentredString(width - 1.9*inch, 0.6*inch, "Scan to verify")
    
    # Signature line
    c.setStrokeColor(HexColor("#1A0E30"))
    c.setLineWidth(1)
    c.line(1.5*inch, 1.2*inch, 4*inch, 1.2*inch)
    c.setFont("Helvetica-Oblique", 14)
    c.setFillColor(HexColor("#1A0E30"))
    c.drawString(2*inch, 0.9*inch, "Sanskriti AI Team")
    
    c.save()
    
    # Cleanup temp QR
    try:
        os.remove(temp_qr_path)
    except:
        pass
        
    return str(filepath)
