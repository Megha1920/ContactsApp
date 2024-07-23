from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Contact
from accounts.models import CustomUser
from .forms import ContactForm
from django.db.models import Q
from django.views.decorators.cache import cache_control
from django.db import connection
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import logout as auth_logout
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def list_contacts(request):
    query = request.GET.get('q', '')
    contacts = Contact.objects.filter(user=request.user)  # Filter contacts for the current user

    if query:
        contacts = contacts.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(address__icontains=query) |
            Q(company__icontains=query) |
            Q(phone_numbers__icontains=query)
        )
    
    paginator = Paginator(contacts, 2)  # Show 5 contacts per page
    page_number = request.GET.get('page', 1)
    contacts_page = paginator.get_page(page_number)

    # Determine the number of pages
    total_pages = paginator.num_pages

    # Build response data for AJAX requests
    contacts_data = list(contacts_page.object_list.values(
        'id', 'first_name', 'last_name', 'address', 'company', 'phone_numbers'
    ))

    response_data = {
        'contacts': contacts_data,
        'has_previous': contacts_page.has_previous(),
        'has_next': contacts_page.has_next(),
        'page_number': contacts_page.number,
        'total_pages': total_pages
    }

    # Check for AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(response_data)

    return render(request, 'contact_list.html', {
        'contacts': contacts_page,
        'query': query,  # Pass the query to the template
    })

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user  # Set the current user
            contact.save()
            return redirect('contacts:list_contacts')  # Redirect to a list or detail view
    else:
        form = ContactForm()
    
    return render(request, 'contact_form.html', {'form': form})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contacts:list_contacts')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contact_form.html', {'form': form})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == 'POST':
        contact.delete()
        return redirect('contacts:list_contacts')
    return render(request, 'confirm_delete.html', {'contact': contact})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ajax_search_contacts(request):
    query = request.GET.get('query', '')
    contacts = Contact.objects.filter(
    Q(first_name__icontains=query) |
    Q(last_name__icontains=query) |
    Q(address__icontains=query) |
    Q(company__icontains=query) |
    Q(phone_numbers__icontains=query)
)
    data = list(contacts.values('id', 'first_name', 'last_name', 'address', 'company', 'phone_numbers'))
    return JsonResponse({'contacts': data})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contacts:list_contacts')
    else:
        form = ContactForm(instance=contact)
    
    # Pass both the form and contact to the template
    return render(request, 'contact_form.html', {'form': form, 'contact': contact})


def logout_user(request):
    auth_logout(request)  # Log out the user
    response = redirect('accounts:landing_page')  # Redirect to landing page
    response['Cache-Control'] = 'no-store'  # Prevent caching
    return response




