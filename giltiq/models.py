from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class QualifiedConfirmation:
    company_name: str
    company_city: str
    company_zip: str
    company_street: str


@dataclass
class ValidationResult:
    valid: Optional[bool]
    vat_id: str
    country_code: str
    vat_number: str
    company_name: Optional[str]
    company_address: Optional[str]
    source: str
    source_timestamp: str
    cache: bool
    qualified_confirmation: Optional[QualifiedConfirmation]
    request_id: str
    requested_at: str

    @classmethod
    def from_dict(cls, data: dict) -> ValidationResult:
        qc = data.get("qualified_confirmation")
        return cls(
            valid=data.get("valid"),
            vat_id=data["vat_id"],
            country_code=data["country_code"],
            vat_number=data["vat_number"],
            company_name=data.get("company_name"),
            company_address=data.get("company_address"),
            source=data["source"],
            source_timestamp=data["source_timestamp"],
            cache=data["cache"],
            qualified_confirmation=QualifiedConfirmation(**qc) if qc else None,
            request_id=data["request_id"],
            requested_at=data["requested_at"],
        )


@dataclass
class UsageResult:
    plan: str
    period_start: str
    period_end: str
    used: int
    remaining: int
    limit: int

    @classmethod
    def from_dict(cls, data: dict) -> UsageResult:
        return cls(
            plan=data["plan"],
            period_start=data["period"]["start"],
            period_end=data["period"]["end"],
            used=data["requests"]["used"],
            remaining=data["requests"]["remaining"],
            limit=data["requests"]["limit"],
        )


@dataclass
class StatusResult:
    status: str
    vies_status: str
    bzst_status: str
    timestamp: str

    @classmethod
    def from_dict(cls, data: dict) -> StatusResult:
        return cls(
            status=data["status"],
            vies_status=data["sources"]["vies"]["status"],
            bzst_status=data["sources"]["bzst"]["status"],
            timestamp=data["timestamp"],
        )


@dataclass
class ValidateOptions:
    requester_vat_id: Optional[str] = None
    company_name: Optional[str] = None
    company_city: Optional[str] = None
    company_zip: Optional[str] = None
    force_live: bool = False
