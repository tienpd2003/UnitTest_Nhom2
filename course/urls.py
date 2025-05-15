from django.urls import path
from . import views

urlpatterns = [
    path('get-moduleclass/<str:idStd>/', views.get_moduleclass, name = 'get_moduleclass_std'),
    path('search-moduleclass/<str:value>/', views.search_moduleclass, name = 'search_moduleclass_std'),
    path('get-detail-schedule/<str:idModuleClass>/', views.get_detail_schedule, name = 'get_detail_schedule_std'),
    path('save-moduleclass/<str:idStd>/', views.save_moduleclass, name = 'save_moduleclass_std'),
    path('get-saved-moduleclass/<str:idStd>/', views.get_saved_moduleclass, name = 'get_saved_moduleclass_std'),
    path('delete-moduleclass/<str:idStd>/', views.delete_moduleclass, name = 'delete_moduleclass_std'),
]