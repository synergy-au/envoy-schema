from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from envoy_schema.server.schema.sep2.types import DeviceCategory


class SiteGroup(BaseModel):
    """Represents a named group that a site might belong to"""

    site_group_id: int
    name: str
    changed_time: datetime


class SiteResponse(BaseModel):
    """Response model for Site - includes the common details"""

    aggregator_id: int
    site_id: int
    nmi: Optional[str]
    timezone_id: str
    changed_time: datetime
    lfdi: str
    sfdi: int
    device_category: DeviceCategory

    groups: list[SiteGroup]


class SitePageResponse(BaseModel):
    """Represents a paginated response of Site"""

    total_count: int  # The total number of sites (independent of this page of results)
    limit: int  # The maximum number of sites that could've been returned (the limit set by the query)
    start: int  # The number of sites that have been skipped as part of this query (the start set by the query)
    sites: list[SiteResponse]  # The site models in this page
