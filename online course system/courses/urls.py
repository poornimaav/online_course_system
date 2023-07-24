from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from courses.forms import CustomPasswordResetForm 

urlpatterns = [
   
    path('', views.base, name='base'),
    path('index/', views.index, name='index'),
    path('navbar/', views.navbar_view, name='navbar'),
    path('authenticate/login/', views.login_view, name='login_view'),
    # path('student/login/', views.student_login, name='student_login'),
    # path('student/login/', views.teacher_login, name='teacher_login'),
    path('logout/', views.logout_view, name='logout'),
    path('authenticate/register/', views.register, name='register'),
    path('register/teacher/', views.teacher_registration, name='teacher_registration'),
    path('register/student/', views.student_registration, name='student_registration'),
    path('register/register_error/', views.register_error, name='register_error'),
    path('switch_to_student/', views.switch_to_student, name='switch_to_student'),
    path('switch_to_teacher/', views.switch_to_teacher, name='switch_to_teacher'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('home/', views.home, name='home'),
    path('authenticate/verify/', views.VerifyOTP, name='verify'),
    path('courses/courses_list/', views.course_list, name='course_list'),
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/course_error/', views.course_error, name='course_error'),
    path('courses/update-course/<str:pk>', views.update_course, name='update_course'),
    path('courses/delete-course/<str:pk>', views.delete_course, name='delete_course'),
    path('courses/course_detail/<int:pk>', views.course_detail, name='course_detail'),
    path('courses/contents/add-content/<str:pk>', views.add_content, name = 'add_content'),
    path('courses/contents/content_error/', views.content_error, name = 'content_error'),
    path('courses/contents/update-content/<str:pk>', views.update_content, name='update_content'),
    path('courses/contents/delete-content/<str:pk>', views.delete_content, name='delete_content'),   
    path('payment/purchase/<int:pk>/', views.purchase_course, name='purchase_course'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('student/student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/purchased-students/<int:pk>/', views.course_purchased_students, name='purchased_students'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="authenticate/password_reset.html",  form_class=CustomPasswordResetForm,), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="authenticate/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authenticate/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="authenticate/password_reset_done.html"), name="password_reset_complete"),

]

