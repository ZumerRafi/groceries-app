from decimal import Decimal

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.http import HttpResponse

from django.utils.dateparse import parse_date
from django.contrib.auth.models import User

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import letter

from .models import Expense

from .forms import ExpenseForm


@login_required
def home(request):

    expenses = Expense.objects.all().order_by('-created_at')

    zumer_total = Decimal('0')
    ali_total = Decimal('0')

    for expense in expenses:

        if expense.user.username == 'Zumer':

            zumer_total += expense.amount

        else:

            ali_total += expense.amount

    total = zumer_total + ali_total

    split_amount = total / 2 if total > 0 else 0

    zumer_balance = zumer_total - split_amount

    ali_balance = ali_total - split_amount

    context = {

        'expenses': expenses,

        'zumer_total': zumer_total,

        'ali_total': ali_total,

        'total': total,

        'split_amount': split_amount,

        'zumer_balance': zumer_balance,

        'ali_balance': ali_balance,

    }

    return render(
        request,
        'expenses/home.html',
        context
    )


@login_required
def add_expense(request):

    if request.method == 'POST':

        form = ExpenseForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            expense = form.save(commit=False)

            expense.user = request.user

            expense.save()

            messages.success(
                request,
                'Expense added successfully!'
            )

            return redirect('/')

    else:

        form = ExpenseForm()

    return render(
        request,
        'expenses/add_expense.html',
        {'form': form}
    )


@login_required
def delete_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id
    )

    expense.delete()

    messages.success(
        request,
        'Expense deleted successfully!'
    )

    return redirect('/')


@login_required
def summary(request):

    expenses = Expense.objects.all()

    zumer_total = Decimal('0')
    ali_total = Decimal('0')

    for expense in expenses:

        if expense.user.username == 'Zumer':

            zumer_total += expense.amount

        else:

            ali_total += expense.amount

    total = zumer_total + ali_total

    split_amount = total / 2 if total > 0 else 0

    zumer_balance = zumer_total - split_amount

    ali_balance = ali_total - split_amount

    context = {

        'zumer_total': zumer_total,

        'ali_total': ali_total,

        'total': total,

        'split_amount': split_amount,

        'zumer_balance': zumer_balance,

        'ali_balance': ali_balance,

    }

    return render(
        request,
        'expenses/summary.html',
        context
    )


def login_view(request):

    if request.user.is_authenticated:

        return redirect('/')

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                'Login successful!'
            )

            return redirect('/')

        else:

            messages.error(
                request,
                'Invalid username or password'
            )

    return render(
        request,
        'expenses/login.html'
    )

def signup_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        confirm_password = request.POST.get(
            'confirm_password'
        )

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match'
            )

            return redirect('/signup/')

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists'
            )

            return redirect('/signup/')

        user = User.objects.create_user(

            username=username,

            password=password

        )

        login(request, user)

        messages.success(
            request,
            'Account created successfully!'
        )

        return redirect('/')

    return render(
        request,
        'expenses/signup.html'
    )
@login_required
def logout_view(request):

    logout(request)

    return redirect('/login/')


@login_required
def pdf_page(request):

    return render(
        request,
        'expenses/pdf_form.html'
    )


@login_required
def export_pdf(request):

    start_date = parse_date(
        request.GET.get('start_date')
    )

    end_date = parse_date(
        request.GET.get('end_date')
    )

    expenses = Expense.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).order_by('-created_at')

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        'attachment; filename=\"statement.pdf\"'
    )

    doc = SimpleDocTemplate(
        response,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        'Groceries Expense Statement',
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    subtitle = Paragraph(
        f'Date Range: {start_date} to {end_date}',
        styles['Heading2']
    )

    elements.append(subtitle)

    elements.append(Spacer(1, 20))

    data = [
        ['User', 'Category', 'Amount', 'Description', 'Date']
    ]

    total = 0

    for expense in expenses:

        total += float(expense.amount)

        data.append([

            expense.user.username,

            expense.category,

            f'£{expense.amount:.3f}',

            expense.description,

            expense.created_at.strftime('%d-%m-%Y')

        ])

    data.append([

        '',

        '',

        f'Total: £{total:.3f}',

        '',

        ''

    ])

    table = Table(data)

    table.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0ea5e9')),

        ('TEXTCOLOR', (0,0), (-1,0), colors.white),

        ('GRID', (0,0), (-1,-1), 1, colors.black),

        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

        ('BOTTOMPADDING', (0,0), (-1,0), 12),

        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),

    ]))

    elements.append(table)

    doc.build(elements)

    return response