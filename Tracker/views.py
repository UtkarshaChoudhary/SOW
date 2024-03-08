# views.py
import csv
from django.shortcuts import render
from .forms import CSVUploadForm
from .models import Book

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a CSV file.')
            else:
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string)
                for row in csv.reader(io_string, delimiter=',', quotechar='"'):
                    _, created = Book.objects.update_or_create(
                        title=row[0],
                        author=row[1],
                        publication_year=row[2]
                    )
        return render(request, 'upload_success.html')
    else:
        form = CSVUploadForm()
    return render(request, 'upload_form.html', {'form': form})
