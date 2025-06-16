from typing import Self

import pydantic
import datetime as dt

from . import base


class CertificateResponse(pydantic.BaseModel):
    """Represents a specific certificate registered in the utility server"""

    certificate_id: int
    created: dt.datetime
    lfdi: str
    expiry: dt.datetime


class CertificatePageResponse(base.BasePageModel):
    """Represents a paginated response of certificates"""

    certificates: list[CertificateResponse]


class CertificateRequest(pydantic.BaseModel):
    """Represents a specific certificate to be created by the utility server"""

    lfdi: str
    expiry: dt.datetime


class CertificateAssignmentRequest(pydantic.BaseModel):
    """Represents a single assignment of a certificate to another entity

    The intent is that the certificate can be created from the model or simply assigned e.g. to an aggregator
    """

    certificate_id: str | None
    lfdi: str | None
    expiry: dt.datetime | None

    @pydantic.model_validator(mode="after")
    def either_id_or_lfdi_provided(self) -> Self:
        """Validates either id or lfdi was provided

        Raises:
            ValueError if neither id or lfdi provided
        """
        if self.certificate_id is None and self.lfdi is None:
            raise ValueError("Either lfdi or id needs to be provided")
        return self
