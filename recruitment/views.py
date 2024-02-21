from rest_framework import generics
from .models import Candidate
from .serializers import CandidateSerializer
from django.db.models import Q



class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateSearchListView(generics.ListAPIView):
    serializer_class = CandidateSerializer


    def get_queryset(self):
        queryset = Candidate.objects.all()
        query_params = self.request.query_params

        filters = {
            'expected_salary__gte': query_params.get('expected_salary_min'),
            'expected_salary__lte': query_params.get('expected_salary_max'),
            'age__gte': query_params.get('age_min'),
            'age__lte': query_params.get('age_max'),
            'years_of_exp__gte': query_params.get('years_of_exp_min'),
            'years_of_exp__lte': query_params.get('years_of_exp_max'),
        }

        search_query = query_params.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(email__icontains=search_query)
            )

        return queryset.filter(**{k: v for k, v in filters.items() if v is not None})
    


class CandidateSearchNameView(generics.ListAPIView):
    serializer_class = CandidateSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        candidates = Candidate.objects.all().values()
        sorted_candidates = self.get_sorted_candidates(query, candidates)
        return sorted_candidates

    def get_sorted_candidates(self, query, candidates):
        query_parts = query.split()
        sorted_candidates = sorted(candidates, key=lambda candidate: (
            candidate['name'] == query,  # Exact match
            sum(part in candidate['name'] for part in query_parts),  # Number of overlapping words
            candidate['name']  # Alphabetical order for tie-breakers
        ), reverse=True)
        return sorted_candidates
