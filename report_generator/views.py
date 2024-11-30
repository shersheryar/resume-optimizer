from django.http import HttpResponse
from django.shortcuts import render
import os
from django.shortcuts import render
from .forms import UploadPDFForm
from .utils import process_pdf_and_generate_report  # Import your backend logic


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
