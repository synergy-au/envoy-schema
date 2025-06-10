from pydantic import BaseModel
from datetime import datetime


class BasePageModel(BaseModel):
    total_count: int  # The total number of objects (independent of this page of results)
    limit: int  # The maximum number of objects that could've been returned (the limit set by the query)
    start: int  # The number of objects that have been skipped as part of this query (the start set by the query)


class CertificateResponse(BaseModel):
    """Represents a specific certificate registered in the utility server"""

    certificate_id: int
    created: datetime
    lfdi: str
    expiry: datetime


class CertificatePageResponse(BasePageModel):
    """Represents a paginated response of certificates"""

    certificates: list[CertificateResponse]
