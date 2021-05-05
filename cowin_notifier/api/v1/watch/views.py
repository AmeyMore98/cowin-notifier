import logging

from fastapi import APIRouter

from cowin_notifier.api.v1.watch.models import District
from cowin_notifier.api.v1.watch.schemas import DistrictIn, DistrictOut
from cowin_notifier.api.v1.watch.service import CowinNotifier

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/districts", response_model=DistrictOut)
async def get_districts() -> DistrictOut:
    """
    Fetch Districts

    Returns:
        DistrictOut: All Districts from DB
    """

    return await DistrictOut.from_queryset(District.all())


@router.post("/districts", response_model=DistrictIn)
async def add_district(params: DistrictIn) -> DistrictIn:
    """
    Add District

    Returns:
        DistrictIn: New District
    """

    await District.create(**params.dict())
    return params


@router.delete("/districts")
async def delete_district(id: int) -> dict:
    """
    Delete District

    Returns:
        dict: id, name of deleted district
    """

    district = await District.get(id=id)
    await district.delete()
    return dict(id=district.id, name=district.name)


@router.get("/test", include_in_schema=False)
async def test():
    """
    !This endpoint is only for testing
    """

    return await CowinNotifier().watch_and_notify()
