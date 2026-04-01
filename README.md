# giltiq

Python SDK for the [Giltiq VAT Validation API](https://giltiq.de).

## Installation

```bash
pip install giltiq
```

## Usage

### Synchronous

```python
from giltiq import Giltiq

with Giltiq(api_key="your-api-key") as client:
    # Validate a VAT ID
    result = client.validate("DE123456789")
    print(result.valid, result.company_name)

    # Check usage
    usage = client.usage()
    print(usage.used, usage.remaining)

    # Check API status
    status = client.status()
    print(status.vies_status, status.bzst_status)
```

### Async

```python
from giltiq import AsyncGiltiq

async with AsyncGiltiq(api_key="your-api-key") as client:
    result = await client.validate("DE123456789")
    print(result.valid)
```

### Qualified Confirmation (German BZSt)

```python
from giltiq import Giltiq, ValidateOptions

with Giltiq(api_key="your-api-key") as client:
    result = client.validate(
        "DE123456789",
        options=ValidateOptions(
            requester_vat_id="DE987654321",
            company_name="Example GmbH",
            company_city="Berlin",
            company_zip="10115",
        ),
    )
    if result.qualified_confirmation:
        print(result.qualified_confirmation.company_name)
```

### Error Handling

```python
from giltiq import Giltiq, GiltiqApiError

with Giltiq(api_key="your-api-key") as client:
    try:
        result = client.validate("INVALID")
    except GiltiqApiError as e:
        print(e.code, e.status, str(e))
```

## Configuration

```python
client = Giltiq(
    api_key="your-api-key",
    base_url="https://api.giltiq.de",  # default
    timeout=15.0,  # seconds, default
    retries=2,  # default
)
```

## Documentation

Full API documentation at [giltiq.de/docs](https://giltiq.de/docs).

## License

MIT
