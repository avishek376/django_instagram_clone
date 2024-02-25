from django.http import HttpResponse
from django.shortcuts import render
from .models import Users
from .form import UserSignUpForm


# Create your views here.
def index(request):
    # return HttpResponse("Hello, World!... you are in the index view")
    # f"Hello, World!...the index view of users, where user count is {users_count}"
    users_details = Users.objects.all()
    users_count = Users.objects.count()
    context = {
        "users_details": users_details,
        "users_count": users_count
    }
    return render(request, "users/index.html", context)


def signup(request):
    sign_up_form = UserSignUpForm()
    errors = []
    message = ""
    # print(request.POST)
    if request.method == "POST":
        sign_up_form = UserSignUpForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save(commit=False)
            sign_up_form.save()
            message = "User has been created successfully"

        else:
            errors = sign_up_form.errors

    context = {
        "form": sign_up_form,
        "errors": errors,
        "message": message,
    }

    return render(request, "users/signup.html", context)
