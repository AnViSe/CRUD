from fastapi import HTTPException, status


class ProjectException(Exception):
    def __init__(self, status_code: int, detail: str, headers: str = None):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers


class NotExistException(ProjectException):
    def __init__(self, message: str = None):
        if not message:
            message = 'Object not exist.'
        super().__init__(status_code=404, detail=message)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},)

invoice_change_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Invoice cannot be changed',)


login_invalid_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Incorrect username or password',)


user_already_exist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='User with this username already exist.',
)

email_already_exist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='User with this e-mail already exist.',
)

user_or_email_already_exist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='User with this name or e-mail already exist.',
)

email_not_exist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='This e-mail not exist.',
)

user_not_exist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='This user not exist.',
)


class DuplicatedEntryError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=422, detail=message)


class DBOperationError(HTTPException):
    def __init__(self, e: Exception):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.args)
