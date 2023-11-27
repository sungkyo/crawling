from django.urls import path


from . import views
urlpatterns = [
    path('croll/croll_view', views.croll_view, name="croll_view"),
    path('croll/croll', views.SearchListView.as_view(), name="croll"),
    path('croll/SeleniumListView', views.SeleniumListView, name="SeleniumListView"),
    path('croll/SeleniumRunView', views.SeleniumRunView, name="SeleniumRunView"),
    #path('croll/crollinfo', views.croll_info, name="crollinfo"),
]