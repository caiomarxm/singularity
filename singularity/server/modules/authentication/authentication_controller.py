from fastapi import APIRouter


router = APIRouter()


@router.get("/login")
def login_with_username_and_password():
    pass
