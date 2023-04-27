from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Student
from .forms import StudentForm


# Create your views here.
@login_required
def index(request):
    return render(request, 'students/index.html', {
        'students': Student.objects.all()
    })


@login_required
def view_student(request, id):
    student = Student.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))


@login_required
def add(request):
    if request.method != 'POST':
        form = StudentForm()
        return render(request, 'students/add.html', {
            'form': StudentForm()
        })
    
    form = StudentForm(request.POST)
    if form.is_valid():
        Student(
            student_number = form.cleaned_data['student_number'],
            first_name = form.cleaned_data['first_name'],
            last_name = form.cleaned_data['last_name'],
            email = form.cleaned_data['email'],
            field_of_study = form.cleaned_data['field_of_study'],
            gpa = form.cleaned_data['gpa']
        ).save()
        return render(request, 'students/add.html', {
            'form': StudentForm(),
            'success': True
        })


@login_required
def edit(request, id):
    if request.method != 'POST':
        student = Student.objects.get(pk=id)
        form = StudentForm(instance=student)
        return render(request, 'students/edit.html', {
        'form': form
        })
    
    student = Student.objects.get(pk=id)
    form = StudentForm(request.POST, instance=student)
    if form.is_valid():
        form.save()
        return render(request, 'students/edit.html', {
            'form': form,
            'success': True
        })


@login_required
def delete(request, id):
    if request.method == 'POST':
        student = Student.objects.get(pk=id)
        student.delete()
    return HttpResponseRedirect(reverse('index'))
