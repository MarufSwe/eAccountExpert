from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum, Q
from sales.models import SalesData, Reconciliation
from decimal import Decimal
import json


def pl_report(request, sales_data_id):
    """Generate P&L report from reconciled data"""
    sales_data = get_object_or_404(SalesData, id=sales_data_id)
    
    # Get all reconciliations for this sales data
    reconciliations = Reconciliation.objects.filter(sales_data=sales_data)
    
    # Separate reconciled and unreconciled transactions
    reconciled_transactions = reconciliations.filter(
        Q(slicer_new__isnull=False) & ~Q(slicer_new='') & 
        Q(category_new__isnull=False) & ~Q(category_new='')
    )
    
    unreconciled_transactions = reconciliations.exclude(
        Q(slicer_new__isnull=False) & ~Q(slicer_new='') & 
        Q(category_new__isnull=False) & ~Q(category_new='')
    )
    
    # Calculate totals
    total_revenue = reconciled_transactions.filter(amount__gt=0).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')
    
    total_expenses = reconciled_transactions.filter(amount__lt=0).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')
    
    # Convert expenses to positive for display
    total_expenses = abs(total_expenses)
    
    # Calculate net profit/loss
    net_profit = total_revenue - total_expenses
    
    # Group by categories for detailed breakdown with proper P&L sections
    revenue_breakdown = {}
    cogs_breakdown = {}
    operating_expenses_breakdown = {}
    other_expenses_breakdown = {}
    
    # Define COGS categories (Cost of Goods Sold)
    cogs_categories = [
        'food cost', 'cost of goods sold', 'inventory', 'materials', 'supplies cost',
        'raw materials', 'direct materials', 'purchases', 'cogs'
    ]
    
    # Define operating expense categories
    operating_expense_categories = [
        'salary', 'wages', 'rent', 'lease', 'utilities', 'insurance', 'repair', 
        'maintenance', 'office', 'professional fees', 'royalty', 'delivery',
        'subscription', 'licenses', 'payroll taxes', 'corp tax', 'other tax',
        'automobile', 'supplies', 'advertising', 'marketing', 'travel'
    ]
    
    for transaction in reconciled_transactions:
        category = transaction.category_new.lower() if transaction.category_new else ''
        amount = abs(transaction.amount)
        
        if transaction.amount > 0:  # Revenue
            if category in revenue_breakdown:
                revenue_breakdown[category] += amount
            else:
                revenue_breakdown[category] = amount
        else:  # Expenses
            # Categorize expenses into proper P&L sections
            is_cogs = any(cogs_term in category for cogs_term in cogs_categories)
            is_operating = any(op_term in category for op_term in operating_expense_categories)
            
            if is_cogs:
                if category in cogs_breakdown:
                    cogs_breakdown[category] += amount
                else:
                    cogs_breakdown[category] = amount
            elif is_operating:
                if category in operating_expenses_breakdown:
                    operating_expenses_breakdown[category] += amount
                else:
                    operating_expenses_breakdown[category] = amount
            else:
                if category in other_expenses_breakdown:
                    other_expenses_breakdown[category] += amount
                else:
                    other_expenses_breakdown[category] = amount
    
    # Sort categories by amount (descending)
    revenue_breakdown = dict(sorted(revenue_breakdown.items(), key=lambda x: x[1], reverse=True))
    cogs_breakdown = dict(sorted(cogs_breakdown.items(), key=lambda x: x[1], reverse=True))
    operating_expenses_breakdown = dict(sorted(operating_expenses_breakdown.items(), key=lambda x: x[1], reverse=True))
    other_expenses_breakdown = dict(sorted(other_expenses_breakdown.items(), key=lambda x: x[1], reverse=True))
    
    # Calculate totals for each section
    total_cogs = sum(cogs_breakdown.values()) if cogs_breakdown else Decimal('0')
    total_operating_expenses = sum(operating_expenses_breakdown.values()) if operating_expenses_breakdown else Decimal('0')
    total_other_expenses = sum(other_expenses_breakdown.values()) if other_expenses_breakdown else Decimal('0')
    
    # Calculate gross profit
    gross_profit = total_revenue - total_cogs
    
    # Calculate operating income
    operating_income = gross_profit - total_operating_expenses
    
    # Calculate net income (including other expenses)
    net_income = operating_income - total_other_expenses
    
    # Calculate unreconciled amounts
    unreconciled_revenue = unreconciled_transactions.filter(amount__gt=0).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')
    
    unreconciled_expenses = unreconciled_transactions.filter(amount__lt=0).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')
    
    unreconciled_expenses = abs(unreconciled_expenses)
    
    context = {
        'sales_data': sales_data,
        'total_revenue': total_revenue,
        'total_cogs': total_cogs,
        'gross_profit': gross_profit,
        'total_operating_expenses': total_operating_expenses,
        'operating_income': operating_income,
        'total_other_expenses': total_other_expenses,
        'net_income': net_income,
        'revenue_breakdown': revenue_breakdown,
        'cogs_breakdown': cogs_breakdown,
        'operating_expenses_breakdown': operating_expenses_breakdown,
        'other_expenses_breakdown': other_expenses_breakdown,
        'unreconciled_revenue': unreconciled_revenue,
        'unreconciled_expenses': unreconciled_expenses,
        'reconciled_count': reconciled_transactions.count(),
        'unreconciled_count': unreconciled_transactions.count(),
        'total_transactions': reconciliations.count(),
    }
    
    return render(request, 'reconciliation/pl_report.html', context)


def pl_report_json(request, sales_data_id):
    """Return P&L data as JSON for API calls"""
    sales_data = get_object_or_404(SalesData, id=sales_data_id)
    
    # Get all reconciliations for this sales data
    reconciliations = Reconciliation.objects.filter(sales_data=sales_data)
    
    # Separate reconciled and unreconciled transactions
    reconciled_transactions = reconciliations.filter(
        Q(slicer_new__isnull=False) & ~Q(slicer_new='') & 
        Q(category_new__isnull=False) & ~Q(category_new='')
    )
    
    # Calculate totals
    total_revenue = reconciled_transactions.filter(amount__gt=0).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')
    
    total_expenses = reconciled_transactions.filter(amount__lt=0).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')
    
    total_expenses = abs(total_expenses)
    net_profit = total_revenue - total_expenses
    
    # Group by categories
    revenue_breakdown = {}
    expense_breakdown = {}
    
    for transaction in reconciled_transactions:
        category = transaction.category_new
        amount = abs(transaction.amount)
        
        if transaction.amount > 0:  # Revenue
            if category in revenue_breakdown:
                revenue_breakdown[category] += float(amount)
            else:
                revenue_breakdown[category] = float(amount)
        else:  # Expenses
            if category in expense_breakdown:
                expense_breakdown[category] += float(amount)
            else:
                expense_breakdown[category] = float(amount)
    
    return JsonResponse({
        'success': True,
        'data': {
            'total_revenue': float(total_revenue),
            'total_expenses': float(total_expenses),
            'net_profit': float(net_profit),
            'revenue_breakdown': revenue_breakdown,
            'expense_breakdown': expense_breakdown,
            'reconciled_count': reconciled_transactions.count(),
            'total_transactions': reconciliations.count(),
        }
    })
