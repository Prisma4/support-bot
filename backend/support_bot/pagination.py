from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNumberOnlyPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        page = self.page
        return Response({
            "count": self.page.paginator.count,
            "max_pages": max(1, (self.page.paginator.count + self.page_size - 1) // self.page_size),
            "next": page.next_page_number() if page.has_next() else None,
            "previous": page.previous_page_number() if page.has_previous() else None,
            "results": data,
        })
