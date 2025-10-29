class ServiceError(Exception): pass
class NotFoundError(ServiceError): pass
class ValidationError(ServiceError): pass
class AuthError(ServiceError): pass
class ConflictError(ServiceError): pass
