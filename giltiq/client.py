from __future__ import annotations

import time
from typing import Any, Optional
from urllib.parse import quote

import httpx

from .models import StatusResult, UsageResult, ValidateOptions, ValidationResult


class GiltiqApiError(Exception):
    def __init__(self, status: int, code: str, message: str, request_id: Optional[str] = None):
        super().__init__(message)
        self.status = status
        self.code = code
        self.request_id = request_id


class Giltiq:
    """Synchronous Giltiq API client."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.giltiq.de",
        timeout: float = 15.0,
        retries: int = 2,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"X-API-Key": self.api_key},
            timeout=self.timeout,
        )

    def validate(self, vat_id: str, options: Optional[ValidateOptions] = None) -> ValidationResult:
        params: dict[str, str] = {}
        if options:
            if options.requester_vat_id:
                params["requester_vat_id"] = options.requester_vat_id
            if options.company_name:
                params["company_name"] = options.company_name
            if options.company_city:
                params["company_city"] = options.company_city
            if options.company_zip:
                params["company_zip"] = options.company_zip
            if options.force_live:
                params["force_live"] = "true"

        data = self._request("GET", f"/v1/validate/{quote(vat_id)}", params=params)
        return ValidationResult.from_dict(data)

    def usage(self) -> UsageResult:
        data = self._request("GET", "/v1/usage")
        return UsageResult.from_dict(data)

    def status(self) -> StatusResult:
        data = self._request("GET", "/v1/status")
        return StatusResult.from_dict(data)

    def _request(self, method: str, path: str, **kwargs: Any) -> dict:
        for attempt in range(self.retries + 1):
            try:
                response = self._client.request(method, path, **kwargs)
                if response.status_code >= 500 and attempt < self.retries:
                    time.sleep(min(1 * 2**attempt, 10))
                    continue
                if not response.is_success:
                    error = response.json().get("error", {})
                    raise GiltiqApiError(
                        response.status_code,
                        error.get("code", "UNKNOWN"),
                        error.get("message", response.reason_phrase or "Unknown error"),
                        error.get("request_id"),
                    )
                return response.json()
            except httpx.TimeoutException:
                if attempt < self.retries:
                    continue
                raise GiltiqApiError(0, "TIMEOUT", "Request timed out")
        raise GiltiqApiError(0, "UNKNOWN", "Request failed after retries")

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Giltiq:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncGiltiq:
    """Asynchronous Giltiq API client."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.giltiq.de",
        timeout: float = 15.0,
        retries: int = 2,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"X-API-Key": self.api_key},
            timeout=self.timeout,
        )

    async def validate(self, vat_id: str, options: Optional[ValidateOptions] = None) -> ValidationResult:
        params: dict[str, str] = {}
        if options:
            if options.requester_vat_id:
                params["requester_vat_id"] = options.requester_vat_id
            if options.company_name:
                params["company_name"] = options.company_name
            if options.company_city:
                params["company_city"] = options.company_city
            if options.company_zip:
                params["company_zip"] = options.company_zip
            if options.force_live:
                params["force_live"] = "true"

        data = await self._request("GET", f"/v1/validate/{quote(vat_id)}", params=params)
        return ValidationResult.from_dict(data)

    async def usage(self) -> UsageResult:
        data = await self._request("GET", "/v1/usage")
        return UsageResult.from_dict(data)

    async def status(self) -> StatusResult:
        data = await self._request("GET", "/v1/status")
        return StatusResult.from_dict(data)

    async def _request(self, method: str, path: str, **kwargs: Any) -> dict:
        import asyncio

        for attempt in range(self.retries + 1):
            try:
                response = await self._client.request(method, path, **kwargs)
                if response.status_code >= 500 and attempt < self.retries:
                    await asyncio.sleep(min(1 * 2**attempt, 10))
                    continue
                if not response.is_success:
                    error = response.json().get("error", {})
                    raise GiltiqApiError(
                        response.status_code,
                        error.get("code", "UNKNOWN"),
                        error.get("message", response.reason_phrase or "Unknown error"),
                        error.get("request_id"),
                    )
                return response.json()
            except httpx.TimeoutException:
                if attempt < self.retries:
                    continue
                raise GiltiqApiError(0, "TIMEOUT", "Request timed out")
        raise GiltiqApiError(0, "UNKNOWN", "Request failed after retries")

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncGiltiq:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
