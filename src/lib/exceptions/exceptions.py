class ServiceError(Exception):
    pass


class RequestError(ServiceError):
    pass


class FileSystemError(ServiceError):
    pass
