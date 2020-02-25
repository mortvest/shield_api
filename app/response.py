# from abc import ABC, abstractmethod

class Response():
    def __init__(self, status_code, message, result):
        self.status_code = status_code
        self.message = message
        self.result = result

    def serialize(self):
        return self.__dict__


class ErrorResponse(Response):
    def __init__(self):
        self.status_code = 4000
        self.message = "error"
        self.result = None


class SingleResponse(Response):
    def __init__(self, result):
        self.status_code = 1000
        self.message = "success"
        self.result = result.serialize


class ListResponse(Response):
    def __init__(self, items, page, count, total, has_next, has_prev):
        self.status_code = 1000
        self.message = "success"
        self.items = items
        self.per_page = len(items)
        self.page = page
        self.count = count
        self.total = total
        self.has_next = has_next
        self.has_prev = has_prev

    def serialize(self):
        result_dict = {
            "items": [i.serialize() for i in self.items],
            "per_page": self.per_page,
            "page": self.page,
            "count": self.count,
            "total": self.total,
            "has_next": self.has_next,
            "has_prev": self.has_prev
        }
        response_dict = {
            "status_code": self.status_code,
            "message": self.message,
            "result": result_dict
        }
        return response_dict


class AuthorizationErrorResponse(Response):
    def __init__(self):
        self.status_code = 4321
        self.message = "user not authorized"
        self.result = None

