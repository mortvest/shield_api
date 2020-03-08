from flask_sqlalchemy import Pagination

class Response():
    def __init__(self, status_code, message, result):
        self.status_code = status_code
        self.message = message
        self.result = result

    def serialize(self):
        return self.__dict__


class ErrorResponse(Response):
    def __init__(self, message="error"):
        self.status_code = 4000
        self.message = message
        self.result = None


class SingleResponse(Response):
    def __init__(self, result={}):
        self.status_code = 1000
        self.message = "success"
        if isinstance(result, dict):
            self.result = result
        else:
            self.result = result.serialize()


class ListResponse(Response):
    def __init__(self, p_obj, page=None, per_page=None, max_per_page=None):
        if not isinstance(p_obj, Pagination):
            raise TypeError("Object is not an instance of Pagination")
        else:
            self.p_obj = p_obj
            self.message = "success"
            self.status_code = 1000

    def serialize(self):
        result_dict = {
            "items": [i.serialize() for i in self.p_obj.items],
            "per_page": self.p_obj.per_page,
            "page": self.p_obj.page,
            "count": self.p_obj.pages,
            "total": self.p_obj.total,
            "has_next": self.p_obj.has_next,
            "has_prev": self.p_obj.has_prev
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
