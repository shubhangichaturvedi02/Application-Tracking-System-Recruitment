from django.urls import path
from .views import CandidateListCreateView, CandidateRetrieveUpdateDestroyView, CandidateSearchListView, CandidateSearchNameView

urlpatterns = [
    path('candidates', CandidateListCreateView.as_view(), name='candidate-list-create'),
    path('candidates/<int:pk>', CandidateRetrieveUpdateDestroyView.as_view(), name='candidate-retrieve-update-destroy'),
    path('candidates/search', CandidateSearchListView.as_view(), name='candidate-search'),
    path('candidates/search/name', CandidateSearchNameView.as_view(), name='candidate_name_search')
]
