from typing import Optional

from pydantic import BaseModel, StrictStr, StrictInt


class TokenPayload(BaseModel):
    sub: StrictStr
    exp: Optional[StrictInt] = None
