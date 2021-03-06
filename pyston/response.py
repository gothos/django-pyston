from django.utils.translation import ugettext


class HeadersResponse(object):

    fieldset = True

    def __init__(self, result, http_headers=None, code=200):
        http_headers = {} if http_headers is None else http_headers
        self.result = result
        self.http_headers = http_headers
        self.status_code = code


class NoFieldsetResponse(HeadersResponse):

    fieldset = False


class RESTResponse(NoFieldsetResponse):

    def __init__(self, msg, http_headers=None, code=200):
        http_headers = {} if http_headers is None else http_headers
        super(RESTResponse, self).__init__(result={'messages': msg}, http_headers=http_headers, code=code)


class RESTOkResponse(NoFieldsetResponse):

    def __init__(self, msg, http_headers=None, code=200):
        http_headers = {} if http_headers is None else http_headers
        super(RESTOkResponse, self).__init__(
            result={'messages': {'success': msg}}, http_headers=http_headers, code=code
        )


class RESTCreatedResponse(HeadersResponse):

    def __init__(self, result, http_headers=None, code=201):
        http_headers = {} if http_headers is None else http_headers
        super(RESTCreatedResponse, self).__init__(result=result, http_headers=http_headers, code=code)


class RESTNoContentResponse(NoFieldsetResponse):

    def __init__(self, http_headers=None, code=204):
        http_headers = {} if http_headers is None else http_headers
        super(RESTNoContentResponse, self).__init__(result='', http_headers=http_headers, code=code)


class RESTErrorsResponse(HeadersResponse):

    def __init__(self, msg, http_headers=None, code=400):
        http_headers = {} if http_headers is None else http_headers
        super(RESTErrorsResponse, self).__init__(
            result={'messages': {'errors': msg}}, http_headers=http_headers, code=code
        )


class RESTErrorResponse(NoFieldsetResponse):

    def __init__(self, msg, http_headers=None, code=400):
        http_headers = {} if http_headers is None else http_headers
        super(RESTErrorResponse, self).__init__(
            result={'messages': {'error': msg}}, http_headers=http_headers, code=code
        )


class ResponseFactory(object):

    def __init__(self, response_class):
        self.response_class = response_class

    def get_response_kwargs(self, exception):
        raise NotImplementedError

    def get_response(self, exception):
        return self.response_class(**self.get_response_kwargs(exception))


class ResponseErrorFactory(ResponseFactory):

    def __init__(self, msg, code, response_class=RESTErrorResponse):
        super(ResponseErrorFactory, self).__init__(response_class)
        self.msg = msg
        self.code = code

    def get_response_kwargs(self, exception):
        return {
            'msg': self.msg,
            'code': self.code,
        }


class ResponseExceptionFactory(ResponseFactory):

    def get_response_kwargs(self, exception):
        return {
            'msg': exception.message,
        }
