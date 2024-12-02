from django.http import HttpResponse
from django.shortcuts import render
import os
from django.shortcuts import render
from .forms import UploadPDFForm
from .utils import process_pdf_and_generate_report  # Import your backend logic
from reportlab.pdfgen import canvas
from io import BytesIO


def index(request):
    return render(request, 'upload.html')


def home(request):
    return HttpResponse("Hello, world. You're at the report_generator index.")


def upload_pdf(request):
    print("asfsffdsfsdf")
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():

            # Get the uploaded PDF file
            pdf_file = request.FILES['pdf_file']

            # Save the file temporarily
            temp_dir = "temp"
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, pdf_file.name)
            with open(temp_path, 'wb+') as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)

            try:
                # Process the uploaded PDF and generate a report
                report = process_pdf_and_generate_report(temp_path)
                os.remove(temp_path)  # Clean up temporary file
                return render(request, 'report.html', {'report': report})
            except Exception as e:
                os.remove(temp_path)  # Clean up on error
                return render(request, 'error.html', {'error': str(e)})
    else:
        form = UploadPDFForm()

    return render(request, 'upload.html', {'form': form})


def download_report(request):
    # Create a BytesIO buffer to hold the PDF data
    buffer = BytesIO()

    # Create a PDF using ReportLab
    pdf = canvas.Canvas(buffer)
    pdf.setTitle("Generated Report")

    # Sample report content (replace this with actual report content)
    report_content = [
        "This is the generated report content.",
        "Optimized for your needs!",
        "",
        "Thank you for using Resume Optimizer."
    ]

    # Write content to the PDF
    pdf.setFont("Helvetica", 12)
    y = 800  # Start position for the content
    for line in report_content:
        pdf.drawString(50, y, line)  # Draw each line at the specified position
        y -= 20  # Move to the next line

    # Finalize the PDF
    pdf.showPage()
    pdf.save()

    # Get the PDF data from the buffer
    buffer.seek(0)

    # Create the HTTP response with the PDF
    response = HttpResponse(
        buffer,
        content_type="application/pdf"
    )
    response['Content-Disposition'] = 'attachment; filename="Generated_Report.pdf"'

    return response
