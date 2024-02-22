from rest_framework import generics
from .models import Candidate
from .serializers import CandidateSerializer
from django.db.models import Q, Case, When, Value, IntegerField, Sum
from django.db.models.functions import Length



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

        # Split query into individual words
        query_parts = query.split()

        # Construct query for exact matches
        exact_match_query = Q(name__iexact=query)

        # Construct query for partial matches based on overlapping words
        partial_match_queries = [
            Q(name__icontains=part)
            for part in query_parts
        ]

        # Query database for candidates
        queryset = Candidate.objects.annotate(
            exact_match=Case(
                When(name__iexact=query, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            ),
            num_matches=Sum(
                Case(
                    *[When(name__icontains=part, then=Value(1)) for part in query_parts],
                    default=Value(0),
                    output_field=IntegerField()
                )
            )
        ).filter(Q(exact_match=1) | Q(num_matches__gt=0)).order_by(
            '-exact_match',       # Exact matches first
            '-num_matches'     # More overlapping words first for partial matches
        )

        return queryset