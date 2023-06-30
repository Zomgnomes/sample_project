from django.db import connection
from django.db.models import F, IntegerField
from django.db.models.expressions import ExpressionWrapper, Window
from django.db.models.functions import Cast, RowNumber
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import ExampleDataDaily
from .serializers import ExampleDataDailySerializer


class ExampleDataDailyFilter(filters.FilterSet):

    related_id = filters.NumberFilter(field_name="related_id", lookup_expr="exact")
    year = filters.NumberFilter(field_name="date__year", lookup_expr="exact")
    year_min = filters.NumberFilter(field_name="date__year", lookup_expr="gte")
    year_max = filters.NumberFilter(field_name="date__year", lookup_expr="lte")

    start_date = filters.DateTimeFilter(field_name="date", lookup_expr="gte")
    end_date = filters.DateTimeFilter(field_name="date", lookup_expr="lte")

    red = filters.RangeFilter()
    green = filters.RangeFilter()
    blue = filters.RangeFilter()
    nir = filters.RangeFilter()

    class Meta:
        model = ExampleDataDaily
        fields = ["id", "date"]


class ExampleDataViewSet(viewsets.ModelViewSet):
    queryset = ExampleDataDaily.objects.all()
    serializer_class = ExampleDataDailySerializer
    permission_classes = [AllowAny]

    @action(methods=["GET"], detail=False)
    def range(self, request, *args, **kwargs):
        # Get the generic queryset of all objects
        queryset = ExampleDataDaily.objects.all()
        # Apply all of our filters to get just the data we want
        filterset = ExampleDataDailyFilter(
            data=request.query_params, queryset=queryset, request=request
        )
        # Set up the tabibito-san query to get our distances
        tabibito = (
            filterset.qs.annotate(
                distance=ExpressionWrapper(
                    F("date")
                    - Cast(  # Cast ROW_NUMBER() from BigInt to Int, so we can subtract from a date
                        Window(
                            expression=RowNumber(),
                            partition_by=[F("related_id")],
                            order_by=[F("date")],
                        ),
                        output_field=IntegerField(),
                    ),
                    output_field=IntegerField(),  # Cast the output to integers so it's continuous across months
                )
            )
        ).values("related_id", "date", "distance")

        # Run tabibito-san through raw SQL since Django ORM doesn't support WITH clauses
        with connection.cursor() as cursor:
            cursor.execute(
                f"WITH tabibito AS ({str(tabibito.query)}) SELECT related_id, MIN(date) AS start_date, MAX(date) AS end_date FROM tabibito GROUP BY related_id, distance ORDER BY related_id, MIN(date)"
            )
            # Get a list of column names from the cursor
            columns = [col[0] for col in cursor.description]
            # Combine the column names list with our SQL results to create a dict of data to return
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return Response(data)
