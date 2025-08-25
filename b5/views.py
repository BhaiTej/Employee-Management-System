from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# ✅ View all employees
@login_required(login_url='login')
def all_emp(request):
    query = request.GET.get("q")      # search term
    sort = request.GET.get("sort")    # sort parameter

    if query:
        employees = Employee.objects.filter(first_name__icontains=query)
    else:
        employees = Employee.objects.all()

    # 🔹 Salary sorting
    if sort == "salary":       # ascending
        employees = employees.order_by("salary")
    elif sort == "-salary":    # descending
        employees = employees.order_by("-salary")

    return render(request, "all_emp.html", {"employees": employees, "query": query, "sort": sort})


# ✅ Add employee
@login_required(login_url='login')
def add_emp(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_emp')
    else:
        form = EmployeeForm()
    return render(request, 'add_emp.html', {'form': form})

# ✅ Update employee
@login_required(login_url='login')
def update_emp(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('all_emp')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'update_emp.html', {'form': form})

# ✅ Delete employee
@login_required(login_url='login')
def remove_emp(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('all_emp')


# ✅ Authentication views (login, logout, signup) remain public
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("all_emp")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")

        # create user
        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "signup.html")
