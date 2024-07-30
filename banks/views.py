from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import BankForm, BranchForm
from .models import Bank, Branch
from django.shortcuts import render

def banks_list(request):
    context = {
        'banks': [
            {'name': 'Bank 1', 'branches': ['Branch 1A', 'Branch 1B']},
            {'name': 'Bank 2', 'branches': ['Branch 2A', 'Branch 2B']}
        ]
    }
    return render(request, 'banks/banks_list.html', context)


@login_required
def add_bank(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            bank = form.save(commit=False)
            bank.owner = request.user
            bank.save()
            return redirect('bank_details', bank_id=bank.id)
    else:
        form = BankForm()
    return render(request, 'banks/add_bank.html', {'form': form})

@login_required
def add_branch(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id)
    if request.user != bank.owner:
        return HttpResponse('Forbidden', status=403)
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.bank = bank
            branch.save()
            return redirect('branch_details', branch_id=branch.id)
    else:
        form = BranchForm(initial={'email': 'admin@utoronto.ca'})
    return render(request, 'banks/add_branch.html', {'form': form, 'bank': bank})

def list_banks(request):
    banks = Bank.objects.all()
    return render(request, 'banks/list_banks.html', {'banks': banks})

def bank_details(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id)
    branches = bank.branches.all()
    return render(request, 'banks/bank_details.html', {'bank': bank, 'branches': branches})

def branch_details(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    return JsonResponse({
        'id': branch.id,
        'name': branch.name,
        'transit_num': branch.transit_number,
        'address': branch.address,
        'email': branch.email,
        'capacity': branch.capacity,
        'last_modified': branch.last_modified
    })

@login_required
def edit_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    if request.user != branch.bank.owner:
        return HttpResponse('Forbidden', status=403)
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect('branch_details', branch_id=branch.id)
    else:
        form = BranchForm(instance=branch)
    return render(request, 'banks/edit_branch.html', {'form': form, 'branch': branch})
