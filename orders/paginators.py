from rest_framework import pagination


class OrdersPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 50