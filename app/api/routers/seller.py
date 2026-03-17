from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from app.core.security import oauth2_scheme
from app.database.models import Seller
from app.utils import decode_access_token

from ..dependencies import SellerServiceDep, SessionDep
from ..schemas.seller import SellerCreate, SellerRead

router = APIRouter(prefix="/seller", tags=["Seller"])


@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    return await service.add(seller)


@router.post("/login")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.authenticate(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt",
    }
