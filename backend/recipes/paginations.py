from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    """Custom pagination."""
    page_size = 6
    page_size_query_param = 'limit'
