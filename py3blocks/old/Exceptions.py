class ExceptionMetaClass(type):
    __exceptions = list()

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if type(name) == str:
            cls.__exceptions.append(name)

    def get_exceptions():
        exceptions = ExceptionMetaClass.__exceptions
        exceptions.sort()
        return exceptions


class Py3BlocksException(Exception, metaclass=ExceptionMetaClass):
    ''''''

    def __init__(self, *args, **kwargs):
        #pylint: disable=E1101
        if 'message' in self.__dict__ and self.message is not None:
            super().__init__(self.message, *args, **kwargs)
        else:
            super().__init__(*args, **kwargs)


class JobNotCallableException(Py3BlocksException):
    message = 'Job actions needs to be callable'
