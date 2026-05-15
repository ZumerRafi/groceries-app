from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'add/',
        views.add_expense,
        name='add_expense'
    ),

    path(
        'delete/<int:expense_id>/',
        views.delete_expense,
        name='delete_expense'
    ),

    path(
        'summary/',
        views.summary,
        name='summary'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'signup/',
        views.signup_view,
        name='signup'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'pdf/',
        views.pdf_page,
        name='pdf_page'
    ),

    path(
        'pdf/download/',
        views.export_pdf,
        name='export_pdf'
    ),

]