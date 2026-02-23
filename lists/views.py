from django.shortcuts import render, redirect
from django.http import response, HttpResponse
from .models import BookList
from books.models import Book
from django.contrib.auth.decorators import login_required
from .forms import CreateListForm, EditListForm
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
from io import BytesIO
import csv

# Create your views here.

# Display all users lists
@login_required
def my_lists(request):
    
    # Get all lists that belong to the current user
    lists = BookList.objects.filter(user=request.user)
    
    # Get all books that belong to the current user
    books = Book.objects.filter(user=request.user)
    
    # Get the number of users finished books
    finished_count = books.filter(status='finished').count()
    
    # Get number of users currently reading books
    currently_reading_count = books.filter(status='currently_reading').count()
    
    # Get number of users want to read books
    want_to_read_count = books.filter(status='want_to_read').count()
    
    # Get the books to use for the list images
    finished_books = books.filter(status='finished')[:4]
    currently_reading_books = books.filter(status='currently_reading')[:4]
    want_to_read_books = books.filter(status='want_to_read')[:4]
    
    
    
    context = {
        'lists': lists, 
        'finished_count': finished_count, 
        'currently_reading_count': currently_reading_count, 
        'want_to_read_count': want_to_read_count,
        'finished_books': finished_books,
        'currently_reading_books': currently_reading_books,
        'want_to_read_books': want_to_read_books
    }
    
    return render(request, 'lists/my-lists.html', context)

# Create a list page
@login_required
def create_list(request):
    
    # If user submits the registration form
    if request.method == 'POST':
        
        #  Create and fill customized form with the user entered data
        form = CreateListForm(request.POST)
        
        # Verify the user entered data is valid
        if form.is_valid():
            
            # Since we used ModelForm for the form we can use form.save to save it
            new_list = form.save(commit=False)
            new_list.user = request.user
            
            # Save the new list after we got the user
            new_list.save()
            
            # Redirect to main lists page
            return redirect('my-lists')
    
    # Display form
    else:
        form = CreateListForm()
            
    context = {'form': form}
    return render(request, 'lists/create-list.html', context)

# List detail page
@login_required
def list_detail(request, list_id):
    
    # Get the user list that matches the list_id
    user_list = BookList.objects.get(pk=list_id, user=request.user)
    
    # Get all books from that list
    books = user_list.books.all()
    
    context = {'user_list': user_list, 'books': books}      
    return render(request, 'lists/list-detail.html', context)
    
      
@login_required  
def add_books(request, list_id):
    
    # Get the user list that matches the list_id
    user_list = BookList.objects.get(pk=list_id, user=request.user)
    
    if request.method == 'POST':
        
        # Get the list of book ids from the form the user submitted
        selected_books = request.POST.getlist('book_ids')
        
        # Iterate through the book ids selected to add by the user
        for book in selected_books:
            # Get the book that matches the primary key taken from book_ids
            book_to_add = Book.objects.get(pk=book, user=request.user)
            
            # Add the book to the users list
            user_list.books.add(book_to_add)
    
        # Redirect to list detail page
        return redirect('list-detail', list_id=list_id)
    
    else:
        
        # Get all available books that belong to current user and are not already in list
        # Use exclude to remove books whose ID is in the list
        books = Book.objects.filter(user=request.user).exclude(id__in=user_list.books.all())
        
        # Sort the title in ascending order
        books = books.order_by('title')
        
        
    context = {'books': books, 'user_list': user_list}
    return render(request, 'lists/add-books.html', context)


@login_required
def remove_books(request, list_id):
    
    # Get the user list that matches the list_id
    user_list = BookList.objects.get(pk=list_id, user=request.user)
    
    if request.method == 'POST':
        
        # Get the list of book ids from the form the user submitted
        selected_books = request.POST.getlist('book_ids')
        
        # Iterate through the book ids selected to remove by the user
        for book in selected_books:
            # Get the book that matches the primary key taken from book_ids
            book_to_remove = Book.objects.get(pk=book, user=request.user)
            
            # Remove the book from the users list
            user_list.books.remove(book_to_remove)
    
        # Redirect to list detail page
        return redirect('list-detail', list_id=list_id)
    
    else:
        
        # Get all current books that are in the users list
        books = user_list.books.all()
        
        # Sort the title in ascending order
        books = books.order_by('title')
        
        
    context = {'books': books, 'user_list': user_list}
    return render(request, 'lists/remove-books.html', context)
    
            

@login_required
def edit_list(request, list_id):
    
    # Get the list that will have its name changed
    user_list = BookList.objects.get(pk=list_id, user=request.user)
    
    # If user submits the edit form
    if request.method == 'POST':
        
        #  Create and fill customized form for this specific user list
        form = EditListForm(request.POST, instance=user_list)
        
        # Verify the user entered data is valid
        if form.is_valid():
            
            # Save the new list name
            form.save()
            
            # Redirect to main lists page
            return redirect('list-detail', list_id=list_id)
    
    # Display form
    else:
        form = EditListForm(instance=user_list)
            
    context = {'form': form, 'user_list': user_list}
    return render(request, 'lists/edit-list.html', context)
        
        
@login_required
def delete_list(request, list_id):
    
    user_list = BookList.objects.get(pk=list_id, user=request.user)
    
    if request.method == 'POST':
        user_list.delete()
        return redirect('my-lists')
    
    context = {'user_list': user_list}
    return render(request, 'lists/delete-list.html', context)


@login_required
def essential_list(request, status):
    
    books = Book.objects.filter(status=status, user=request.user)
    
    status_names = {
        'finished': 'Finished',
        'currently_reading': 'Currently Reading',
        'want_to_read': 'Want to Read'
    }
    
    # Assign the list name the value of the status depending on what the user clicks
    list_name = status_names[status]
    
    books = books.order_by('title')
    
    context = {'books': books, 'list_name': list_name, 'status': status}
    
    return render(request, 'lists/essential-list.html', context)

# Create view that takes format parameter as well as list_id and status as optional parameters
@login_required
def export_list(request, format, list_id=None, status=None):
    
    # If user is trying to export a custom list
    if list_id:
        
        # Get the current user list
        user_list = BookList.objects.get(pk=list_id, user = request.user)
        
        # Get all the books from that list
        books = user_list.books.all()
        
        # Order the books in alphabetical order
        books = books.order_by('title')
        
        # Get list name for the filename
        list_name = user_list.name
    
    # If user is trying to export a essential list
    else:
        # Get all books for the user filtered by the status value
        books = Book.objects.filter(status=status, user=request.user)
        
        # Order the books in alhabetical order
        books = books.order_by('title')
        
        status_names = {
            'finished': 'Finished',
            'currently_reading': 'Currently Reading',
            'want_to_read': 'Want to Read'
        }
        
        # Assign the list name the value of the status for the filename
        list_name = status_names[status]
           
    if format == 'csv':
        # Create a CSV response
        response = HttpResponse(content_type='text/csv')
        
        # Create a file name by replacing spaces with underscores and making it lowercase
        filename = list_name.replace(' ', '_').lower() + '.csv'
        
        # Tell browser to download file with the filename
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Create a CSV writer to write to the response
        writer = csv.writer(response)
        
        # Write header row for the column names
        writer.writerow(['Title', 'Author', 'Genre', 'Rating', 'Review', 'Purchase Link'])
        
        # Fill out each following row with the info from each book
        for book in books:
            writer.writerow([
                book.title,
                book.author,
                # Display the Display names for genre
                book.get_genre_display(),
                f"{book.rating}/5" if book.rating else '',
                book.review or '',
                book.purchase_link or '',
            ])
        
        # Return the HttpResponse that tells the browser to download the newly created csv file
        return response
    
    elif format == 'pdf':
        filename = list_name.replace(' ', '_').lower() + '.pdf'
    
        # BytesIO creates an in-memory buffer to hold the PDF data
        # This is better than saving to disk because it's faster and doesn't require file cleanup
        buffer = BytesIO()
    
        # SimpleDocTemplate is ReportLab's PDF document builder
        # Set the page size to normal letter page size and set margins on all sides
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=inch, leftMargin=inch, topMargin=inch, bottomMargin=inch)
    
        # getSampleStyleSheet gives us pre-built styles like Title, Heading2, Normal
        # These control font size, weight, spacing, etc.
        styles = getSampleStyleSheet()
    
        # Clone the Normal style to create a custom link style
        # clone() copies all existing properties
        link_style = styles['Normal'].clone('LinkStyle')
        link_style.textColor = colors.blue
        link_style.underline = True
    
        # elements is a list of content blocks that ReportLab will stack vertically in the PDF
        # Everything gets added to this list and then built into the PDF at the end
        elements = []
    
        # Add the list name as a large centered title at the top of the PDF
        elements.append(Paragraph(list_name, styles['Title']))
        
        # Draw a line under title
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
        
        # Spacer to add vertical whitespace
        elements.append(Spacer(1, 0.3 * inch))
    
        # Loop through each book and add its information as a block of content
        for book in books:
            book_elements = []

            # Book title as a bold heading
            book_elements.append(Paragraph(book.title, styles['Heading2']))
            
            # Author in normal text
            book_elements.append(Paragraph(f"by {book.author}", styles['Normal']))
            book_elements.append(Spacer(1, 0.10 * inch))

            # Show rating as the rating out of 5 if one exists, otherwise show "Not rated"
            rating_text = f"{book.rating}/5" if book.rating else "Not rated"
            book_elements.append(Paragraph(f"<b>Genre:</b> {book.get_genre_display()}  |  <b>Rating:</b> {rating_text}", styles['Normal']))
            book_elements.append(Spacer(1, 0.10 * inch))

            # Only add review if the user wrote one and use a grey background with it
            if book.review:
                review_data = [[Paragraph(f"<i>\"{book.review}\"</i>", styles['Normal'])]]
                review_table = Table(review_data, colWidths=[6.5 * inch])
                review_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f5f5')),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                book_elements.append(review_table)
                book_elements.append(Spacer(1, 0.05 * inch))

            # Only add purchase link if one exists
            if book.purchase_link:
                book_elements.append(Spacer(1, 0.05 * inch))
                book_elements.append(Paragraph(f'<font color="#555555">Purchase:</font> <link href="{book.purchase_link}"><u>Check it out here</u></link>', link_style))

            book_elements.append(Spacer(1, 0.1 * inch))
            
            # Divider line between books
            book_elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
            book_elements.append(Spacer(1, 0.15 * inch))

            # Use KeepTogether prevent one book's info from being split across 2 pages
            elements.append(KeepTogether(book_elements))
    
        # Build converts the elements list into the actual PDF and writes it to the buffer
        doc.build(elements)
    
        # Get the PDF bytes from the buffer and close it to free memory
        pdf = buffer.getvalue()
        buffer.close()
    
        # Return the PDF as a downloadable file response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response    
    
    else:
        return HttpResponse("Invalid format. Use 'csv' or 'pdf'.", status=400)
        
        
        
        
        
    
    
    
    
      
        
        
        
        
        
        
        
          
            
            
            
            

        
        
    
    
    
    
    

