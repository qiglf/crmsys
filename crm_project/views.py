from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from . import models
from .models import Member, Work
from .forms import MemberForm
import crm_project.forecasting.feedforward as ffd
from django.db.models import Q

def quick_sort(arr, low, high):
  def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
      if arr[j]['id'] >= pivot['id']:
        i += 1
        arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

  if low < high:
    pivot = partition(arr, low, high)
    quick_sort(arr, low, pivot - 1)
    quick_sort(arr, pivot + 1, high)

def run_feed_forward(request):
  ffd

@login_required
def add_member(request):
  if request.method == 'POST':
    form = MemberForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('contacts')
  else:
    form = MemberForm()
  return render(request, 'add_member.html', {'form': form})

@login_required
def delete_member(request, id):
  # Retrieve the member from the database
  member = Member.objects.get(id=id)
  works = Work.objects.all().filter(mId=member)
  for i in works:
    i.delete()

  # Delete the member from the database
  member.delete()

  # Show a success message to the user
  messages.success(request, 'Member deleted successfully.')

  # Redirect to a success page
  return redirect('contacts')

@login_required
def contacts(request):
  # Retrieve all members from the database
  members = Member.objects.all()

  # Check if the user has submitted a sort form
  if request.method == 'POST':
    # Retrieve the sort field and direction from the form
    sort_field = request.POST.get('sort_field')
    sort_direction = request.POST.get('sort_direction')

    # Sort the list of members according to the chosen field and direction
    if sort_field == 'firstname':
      if sort_direction == 'asc':
        members = members.order_by('firstname')
      else:
        members = members.order_by('-firstname')
    elif sort_field == 'lastname':
      if sort_direction == 'asc':
        members = members.order_by('lastname')
      else:
        members = members.order_by('-lastname')
    elif sort_field == 'id':
      if sort_direction == 'asc':
        members = members.order_by('id')
      else:
        members = members.order_by('-id')

  # Render the template with the sorted list of members
  context = {'members': members}
  return render(request, 'contacts.html', context)

@login_required
def details(request, id):
  mymember = Member.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
  }
  return HttpResponse(template.render(context, request))

@login_required
def edit_details(request, id):
  member = get_object_or_404(Member, pk=id)

  if request.method == 'POST':
    form = MemberForm(request.POST, instance=member)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('details', args=(id,)))
  else:
    form = MemberForm(instance=member)

  return render(request, 'edit_details.html', {'form': form})

@login_required
def main(request):
  template = loader.get_template('prediction.html')
  return HttpResponse(template.render())


def home(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())

@login_required
def delete(request, id):
  member = Member.objects.get(id=id)
  member.delete()
  return HttpResponse('home.html')

@login_required
def contactSearch(request):
  query = request.GET.get('q')
  mymembers = Member.objects.filter(
    models.Q(firstname__icontains=query) |
    models.Q(lastname__icontains=query) |
    models.Q(email__icontains=query) |
    models.Q(phone__icontains=query) |
    models.Q(country__icontains=query) |
    models.Q(id__icontains=query) |
    models.Q(education__icontains=query) |
    models.Q(desired_position__icontains=query) |
    models.Q(amount_of_workplaces__icontains=query) |
    models.Q(total_years_of_exp__icontains=query)
  )

  context = {'members': mymembers}
  return render(request, 'contacts.html', context)







