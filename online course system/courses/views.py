from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm, CourseForm,  TeacherRegistrationForm, StudentRegistrationForm, ContentForm
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.core.mail import send_mail
from django.conf import settings
from online_system.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required,  user_passes_test
from .models import Course, Content
import paypalrestsdk
from django.urls import reverse
from django.template.loader import render_to_string

from django.db.models import Q
from .models import Teacher, Student
from paypalrestsdk import exceptions
from django.utils.crypto import get_random_string
import random
import string


def base(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'base.html', context)

def navbar_view(request):
    return render(request, 'navbar.html')
    
def home(request):
    return render(request, 'home.html')

@csrf_exempt
def VerifyOTP(request):
    User = get_user_model()

    if request.method == "POST":
        userotp = request.POST.get('otp')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        is_teacher = (request.POST.get('is_teacher'))=='True'
        is_student = (request.POST.get('is_student'))=='True'

        print(is_teacher)
        print(is_student)

        if password1 == password2:         
            user = User.objects.create_user(  
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password1,
                is_teacher=is_teacher,
                is_student=is_student                
            )
            print(is_teacher)
           
            if is_teacher:
                bio = request.POST.get('bio')
                expertise = request.POST.get('expertise')
                teacher = Teacher.objects.create(user=user, 
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                bio=bio,
                expertise=expertise)
                user.is_teacher = True
                user.save()  


            elif is_student:
                major = request.POST.get('major')
                university = request.POST.get('university')
                degree = request.POST.get('degree')
                student = Student.objects.create(user=user, first_name=first_name,last_name=last_name,
                username=username, email=email)
                # major=major, university=university, degree=degree)
                user.is_student = True
                user.save() 

            print("is_teacher:", is_teacher)
            print("is_student:", is_student)
            # # user.set_password(password1)
           
            print("User:", user)
            # Save the user object to the database
          # Set is_teacher to True
            # user.save()
            
            print("OTP: ", userotp)
          
            return redirect('login_view')
            # return JsonResponse({'data': 'Hello'}, status=200)            else:                # Handle form validation errors
        else:
            msg = 'Wrong OTP. Please try again.'
    else:
            # Handle password mismatch error
        return JsonResponse({'errors': 'Passwords do not match'}, status=400)
    return render(request, 'authenticate/verify.html')

def index(request):
    return render(request, 'index.html')

def register(request):
    # form = SignUpForm()
    msg = None
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        is_teacher = request.POST.get('is_teacher')
        is_student = request.POST.get('is_student')
        form = SignUpForm(request.POST)

        if is_teacher:

            form = TeacherRegistrationForm(request.POST)
        else:
            form = SignUpForm(request.POST)

        if form.is_valid():

            otp = random.randint(1000, 9999)
            send_mail(
                "OTP: ",
                 f"Verify Your Mail by the OTP: \n{otp}",  
                EMAIL_HOST_USER,
                [email]
                )
            return render(request, 'authenticate/verify.html' , {'otp': otp,  'first_name':  first_name, 'last_name':last_name ,'email': email, 'username': username, 'password1': password1, 'password2': password2, 'is_student': is_student, 'is_teacher': is_teacher})
             
        else:
            msg = 'form is not valid'

    else:
        form = SignUpForm()
    return render(request, 'authenticate/register.html', {'form': form, 'msg': msg})

def teacher_registration(request):
    try:
        msg = None
        if request.method == "POST":
            form = TeacherRegistrationForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                username = form.cleaned_data['username']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                bio = form.cleaned_data['bio']
                expertise = form.cleaned_data['expertise']
            

                if password1 == password2:
                    otp = random.randint(1000, 9999)
                    send_mail(
                        "OTP: ",
                        f"Verify Your Mail by the OTP: \n{otp}",  # Corrected newline character
                        EMAIL_HOST_USER,
                        [email]
                    )
                    print(otp)

                    # Redirect to a verification page along with form data
                    return render(request, 'authenticate/verify.html', {
                        'otp': otp,
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'username': username,
                        'password1': password1,
                        'password2': password2,
                        'is_teacher': True,
                        'bio': bio,
                        'expertise': expertise,
                       
                    })
                else:
                    return HttpResponse('Passwords did not match')
            else:
                msg = 'Form is not valid'
        else:
            form = TeacherRegistrationForm()

        return render(request, 'authenticate/teacher_registration.html', {'form': form, 'msg': msg})

    except Exception as e:
        # Log the exception for debugging purposes
        print(e)
        return render(request, 'register_error.html')


def student_registration(request):
    try:
        msg = None
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            # major = request.POST.get('major')
            # university = request.POST.get('university')
            # degree =request.POST.get('degree')
            
                
            form = StudentRegistrationForm(request.POST)
        
            if form.is_valid():
                if password1==password2:
                    otp = random.randint(1000, 9999)
                    send_mail(
                        "OTP: ",
                        f"Verify Your Mail by the OTP: \n{otp}",  # Corrected newline character
                        EMAIL_HOST_USER,
                        [email]
                        )
                    print(otp)
                    return render(request, 'authenticate/verify.html' , {'otp': otp,  'first_name':  first_name, 'last_name':last_name ,'email': email, 'username': username, 'password1': password1, 'password2': password2,  'is_student': True})
                # 'major': major, 'degree':degree, 'university': university})
                else:
                    return HttpResponse('Passwords did not match')
            else:
                msg = 'form is not valid'

        else:
            form = StudentRegistrationForm()
        return render(request, 'authenticate/student_registration.html', {'form': form, 'msg': msg})
    
    except Exception as e:
        # Log the exception for debugging purposes
        print(e)
        return render(request, 'register_error.html')

def register_error(request):
    return render(request, 'authenticate/register_error.html')
        

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_student:
                    return redirect('student_dashboard')
                else:
                    return redirect('teacher_dashboard')  # Redirect to create course for other user types
                
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'authenticate/login.html', {'form': form, 'msg': msg})



def logout_view(request):
    logout(request)
    return redirect('base')

def switch_to_student(request):
    user = request.user

    # Check if the user is currently logged in as a teacher
    if user.is_authenticated and user.is_teacher:
        # Update the user's attributes
        user.is_student = True
        user.is_teacher = False

        user.save()

        # Redirect to the student dashboard or any other desired page
        return redirect('student_dashboard')

    # If the user is not logged in as a teacher, redirect to an error page or display a message
    return HttpResponse('Unable to switch to student mode')

def switch_to_teacher(request):
    user = request.user
    if user.is_authenticated and user.is_student:
        user.is_teacher = True
        user.is_student = False
        user.save()

        # Redirect to the student dashboard or any other desired page
        return redirect('teacher_dashboard')

    return HttpResponse('Unable to switch to teacher mode')
    # return render(request, 'teacher/switch_to_student.html')

def course_list(request):
    courses = Course.objects.all()
    search_query = request.GET.get('search', '')  # Get the search query from the request
    
    if search_query:
        courses = Course.objects.filter(title__icontains=search_query)  # Filter courses based on the search query
    else:
        courses = Course.objects.all()
    
    context = {
        'courses': courses,
        'user': request.user
    }
    
    return render(request, 'courses/course_list.html', context)


@login_required
def create_course(request):
    try:
        User = get_user_model()

        if request.method == 'POST':
            form = CourseForm(request.POST)
            if form.is_valid():
                course = form.save(commit=False)
                course.teacher = request.user
                course.save()
                
                # purchased_students = course.get_purchased_students()
                purchased_students = User.objects.filter(
                    Q(purchased_courses__teacher=request.user) &
                    Q(is_student=True)
                ).distinct()
                # Send email notifications to the purchased students
                for student in purchased_students:

                    subject = 'New Course Available: {}'.format(course.title)  # Customize the subject
                    message = render_to_string('courses/new_course_notification.html', {'course': course})  # Customize the email template
                    send_mail(subject, '', EMAIL_HOST_USER, [student.email], html_message=message)
                
                return redirect('teacher_dashboard')
        else:
            form = CourseForm()
        return render(request, 'courses/create_course.html',{'form':form})
    
    except Exception as e:
        print(e)
        return render(request,'courses/course_error.html')

def course_error(request):
    return render(request, 'courses/course_error.html')

@login_required
def update_course(request, pk):
    course = Course.objects.get(id=pk)
    if request.method=='POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = CourseForm(instance=course)
        
    return render(request, 'courses/update_course.html', {'form':form})


@login_required
def delete_course(request, pk):
    course = Course.objects.get(id=pk)
    if request.method=='POST':
        course.delete()
        return redirect('teacher_dashboard')
    
    return render(request, 'courses/delete_course.html', {'course':course})

# @login_required
# def add_content(request, pk):
#     try:
#         course = Course.objects.get(id=pk)

#         if request.method == 'POST':
#             form = ContentForm(request.POST)
#             if form.is_valid():
#                 content = form.save(commit=False)
#                 content.course_id = course.id
#                 content.save()
#                 form.save_m2m()

#                 # Retrieve the purchased students
#                 purchased_students = course.get_purchased_students()
#                 for student in purchased_students:
#                     subject = f'New Topic Available: {content.title}'  # Customize the subject
#                     message = render_to_string('courses/topics/new_topic_notification.html', {'course': course})  # Customize the email template
#                     send_mail(subject, '', EMAIL_HOST_USER, [student.email], html_message=message)
                
#                 return redirect('teacher_dashboard')
#         else:
#             form = ContentForm()

#         return render (request, 'courses/contents/add_content.html', {'form': form, 'course':course})
    
#     except Exception as e:
#         print(e)
#         return render(request, 'courses/contents/content_error.html')


@login_required
def add_content(request, pk):
    try:
        course = Course.objects.get(id=pk)

        if request.method == 'POST':
            form = ContentForm(request.POST)
            if form.is_valid():
                content = form.save(commit=False)
                content.course = course
                content.save()

                # Retrieve the purchased students
                purchased_students = course.get_purchased_students()
                for student in purchased_students:
                    subject = f'New Topic Available: {content.title}'  # Customize the subject
                    message = render_to_string('courses/topics/new_topic_notification.html', {'course': course})  # Customize the email template
                    send_mail(subject, '', EMAIL_HOST_USER, [student.email], html_message=message)
                
                return redirect('teacher_dashboard')
        else:
            form = ContentForm()

        return render(request, 'courses/contents/add_content.html', {'form': form, 'course': course})
    
    except Exception as e:
        print(e)
        return render(request, 'courses/contents/content_error.html')
        
def content_error(request):
    return render(request, 'courses/contents/content_error.html')

def course_detail(request, pk):
    course = get_object_or_404(Course, id=pk)
    contents = course.contents
    purchased_students = course.get_purchased_students()
    
    return render(request, 'courses/course_detail.html', {'course': course, 'contents': contents, 'purchased_students': purchased_students})

@login_required
def update_content(request, pk):
    content= Content.objects.get(id=pk)
    if request.method=='POST':
        form = ContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = ContentForm(instance=content)
        
    return render(request, 'courses/contents/update_content.html', {'form':form})


@login_required
def delete_content(request, pk):
    content = Content.objects.get(id=pk)
    if request.method=='POST':
        content.delete()
        return redirect('teacher_dashboard')
    
    return render(request, 'courses/contents/delete_content.html', {'content':content})

def generate_invoice_number(course_pk, user_pk):
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return f'{course_pk}-{user_pk}-{random_string}'

def purchase_course(request, pk):
    try:
        course = get_object_or_404(Course, pk=pk)
        price = course.price
        user = request.user


        if course.is_purchased_by_user(user):
            return HttpResponse('Course already purchased')
            # return redirect('course_detail', pk=pk)

        paypalrestsdk.configure({
            'mode': settings.PAYPAL_MODE,
            'client_id': settings.PAYPAL_CLIENT_ID,
            'client_secret': settings.PAYPAL_CLIENT_SECRET
        })

        invoice_id = generate_invoice_number(course.pk, user.pk)

        # payer_id = f'{course.pk}-{uuid.uuid4().hex}'

        payment = paypalrestsdk.Payment({
            'intent': 'sale',
            'payer': {'payment_method': 'paypal'},
            'transactions': [{
                'amount': {'total': str(price), 'currency': 'USD'},
                'description': 'Course Payment',
                # 'invoice_number': str(user.pk),
                 'invoice_number': invoice_id,
            }],
            'redirect_urls': {
                'return_url': request.build_absolute_uri(reverse('payment_success')),
                'cancel_url': request.build_absolute_uri(reverse('payment_cancel')),
            }
        })

        if payment.create():
            # Redirect user to PayPal payment approval URL
            for link in payment.links:
                if link.method == 'REDIRECT':
                    return redirect(link.href)

        else:
        #     # Handle PayPal payment creation error
            return render(request, 'payment/payment_failed.html')

        return render(request, 'payment/payment_success.html')
    

    except Exception as e:
        # Handle other exceptions
        return render(request, 'payment/payment_error.html')

def payment_success(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({'payer_id': payer_id}):
        invoice_id = payment.transactions[0].invoice_number
        course_pk, user_pk, _ = invoice_id.split('-')

        course = Course.objects.get(pk=course_pk)

        user = request.user
        course.mark_as_purchased(user, payment_id)

        return render(request, 'payment/payment_success.html', {'course': course, 'payment': payment})
    else:
        return render(request, 'payment/payment_failed.html')

def payment_cancel(request):
    # Handle payment cancellation or failure
    # return HttpResponse('Payment canceled')
    payment_failed = True
    # return render(request, 'course_list.html', {'payment_failed': payment_failed})
    return render(request, 'payment/payment_failed.html')

@login_required
def student_dashboard(request):
    purchased_courses = Course.objects.filter(purchased_by=request.user)
    context = {
        'purchased_courses': purchased_courses
    }
    
    return render(request, 'student/student_dashboard.html', context)

@login_required
def teacher_dashboard(request):
    user = request.user
    if user.is_teacher:
        courses = Course.objects.filter(teacher=user)
        return render(request, 'teacher/teacher_dashboard.html', {'courses': courses})
    else:
        return HttpResponse('You are not authorized to access this page.')



def course_purchased_students(request, pk):
    course = get_object_or_404(Course, id=pk)
    purchased_students = course.get_purchased_students()
    context= {
        'course': course,
        'purchased_students': purchased_students
    }
    return render(request, 'teacher/course_purchased_students.html', context)


def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')