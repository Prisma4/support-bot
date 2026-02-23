from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNumberOnlyPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        page = self.page
        page_size = self.get_page_size(self.request) or self.page.paginator.per_page

        count = page.paginator.count
        max_pages = max(1, (count + page_size - 1) // page_size)

        return Response({
            "count": count,
            "max_pages": max_pages,
            "next": page.next_page_number() if page.has_next() else None,
            "previous": page.previous_page_number() if page.has_previous() else None,
            "results": data,
        })
