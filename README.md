# Pilot Python SDK

```bash
pip install pilot-sdk
```

## Usage

```python
from pilot_sdk import Pilot

pilot = Pilot("pk_your_api_key")
pilot.send("prod_errors", "Deploy failed on server 3")
```

## Error handling

```python
from pilot_sdk import Pilot, AuthError, RateLimitError, PaymentRequiredError, PilotError

pilot = Pilot("pk_your_api_key")

try:
    pilot.send("prod_errors", "Deploy failed")
except AuthError:
    print("Invalid API key")
except RateLimitError:
    print("Slow down — max 20 msg/sec per destination")
except PaymentRequiredError:
    print("Trial limit reached or subscription cancelled")
except PilotError as e:
    print(f"Error {e.status_code}: {e}")
```
