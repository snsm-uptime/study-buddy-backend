from datetime import datetime, timezone
from typing import Annotated

from sqlalchemy import TIMESTAMP, func, null
from sqlalchemy.orm import mapped_column

# -- Semantic timestamp aliases for clarity & intent --
CreatedAt = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    ),
]

UpdatedAt = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        server_onupdate=func.now(),  # ✅ updates on modification
    ),
]

DeletedAt = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        default=None,
        server_default=null(),
    ),
]
