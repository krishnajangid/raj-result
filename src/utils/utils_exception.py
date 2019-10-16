#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


class DataValidation(Exception):
    pass


class ConnectionTimeOut(Exception):
    def __init__(self, *args, **kwargs):
        pass


class BaseUrlNotFound(Exception):

    def __init__(self, *args, **kwargs):
        pass


class CaseKeyNotFound(Exception):

    def __init__(self, *args, **kwargs):
        pass


class RequestDataValidationFailed(Exception):

    def __init__(self, *args, **kwargs):
        pass


class UnSuportedService(Exception):
    def __init__(self, *args, **kw):
        pass


class InvalidFilterOption(Exception):
    def __init__(self, *args):
        super().__init__(self, *args)


class SearchTermOperatorNotAllowed(Exception):
    def __init__(self, *args):
        super().__init__(self, *args)


class InvalidLoadBalancer(Exception):
    def __init__(self, *args):
        super().__init__(self, *args)


class ResponseFailureException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class ResponseCodeException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class MappedCaseNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class DocXtractFailureException(Exception):
    def __init__(self, *args, **kwargs):
        pass


class APICallFailed(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class FolderNotFound(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class FileNotFound(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class FileAlreadyPresent(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class ConnectionNotEstablished(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class JsonSchemaValidationFailed(Exception):

    def __init__(self, *args, **kwargs):
        pass


class UnExpectedError(Exception):

    def __init__(self, *args, **kwargs):
        pass


class ArgParserExpectationFailed(Exception):

    def __init__(self, *args, **kwargs):
        pass


class JsonDecodeError(Exception):

    def __init__(self, *args, **kwargs):
        pass
