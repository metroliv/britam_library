from django.urls import path
from . import views

urlpatterns = [
    path('', views.borrow_dashboard, name='borrow_dashboard'),  # ✅ this is the fix
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:record_id>/', views.return_book, name='return_book'),
    path('history/', views.borrow_history, name='borrow_history'),
    path('all-records/', views.all_borrow_records, name='all_borrow_records'),

]
