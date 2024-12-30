from typing import List, Dict

class PaginatedResponse:
    def __init__(self, items: Dict, total_count: int, page: int, limit: int):
        self.items = items
        self.total_count = total_count
        self.page = page
        self.limit = limit

    def get_paginated_response(self) -> Dict:
        # Calculate pagination metadata
        total_pages = (self.total_count + self.limit - 1) // self.limit  # ceil division
        has_next = self.page < total_pages
        has_previous = self.page > 1

        return {
            "data": self.items,
            "pagination": {
                "total_count": self.total_count,
                "total_pages": total_pages,
                "page": self.page,
                "limit": self.limit,
                "has_next": has_next,
                "has_previous": has_previous
            }
        }
