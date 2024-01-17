from fastapi import APIRouter, Depends, Request

from src.core.repository import FormRepo
from src.core.schemas import MatchingTemplate
from src.deps import form_repo as deps_form_repo

router = APIRouter()


@router.get("/get_form", status_code=200, response_model=MatchingTemplate | dict)
async def get_form(
    *,
    request: Request,
    form_repo: FormRepo = Depends(deps_form_repo),
) -> MatchingTemplate | dict:
    """
    Get the matching template or return the typed form data.

    Args:
        request: Request
        form_repo: FormRepo

    Returns:
        MatchingTemplate | dict: Matching template or typed form data.
    """
    return await form_repo.get_form(form_data=dict(request.query_params))


@router.post("/get_form", status_code=200, response_model=MatchingTemplate | dict)
async def get_form(
    *,
    form_data: dict,
    form_repo: FormRepo = Depends(deps_form_repo),
) -> MatchingTemplate | dict:
    """
    Get the matching template or return the typed form data.

    Args:
        form_data: dict
        form_repo: FormRepo

    Returns:
        MatchingTemplate | dict: Matching template or typed form data.
    """
    return await form_repo.get_form(form_data=form_data)
