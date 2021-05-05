from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from cowin_notifier.api.v1.watch.models import District

DistrictIn = pydantic_model_creator(District)
DistrictOut = pydantic_queryset_creator(District)
