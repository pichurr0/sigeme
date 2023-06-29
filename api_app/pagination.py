from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    En este metodo no se devuelven page ni per_page porque son los valores
    que envia el cliente [vienene en la request]
    """
    page_query_param = 'page'
    page_size = 20
    max_page_size = 100
    page_size_query_param = 'per_page'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'items': data
        })