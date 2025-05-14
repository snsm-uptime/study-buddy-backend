from datetime import datetime, timezone
from typing import Annotated

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import mapped_column

# -- Base shared timestamp column type --
Timestamp = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    ),
]

# -- Semantic timestamp aliases for clarity & intent --
CreatedAt = Timestamp
DeletedAt = Timestamp

UpdatedAt = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        server_onupdate=func.now(),  # ✅ updates on modification
    ),
]
