"""JSON-RPC 2.0 request/response wrappers."""

from typing import Annotated, Literal
from pydantic import BaseModel, Field

# === JSON-RPC Wrappers ===

class JSONRPCRequest(BaseModel):
    """Standard JSON-RPC 2.0 request wrapper."""

    jsonrpc: Literal["2.0"]
    id: Annotated[int | str, Field(..., description="Unique call ID")]
    method: Annotated[str, Field(..., description="Name of method")]
    params: Annotated[dict, Field(..., description="Method arguments")]


class JSONRPCError(BaseModel):
    """Error returned by failed JSON-RPC calls."""

    code: Annotated[int, Field(..., description="Standard JSON-RPC error code")]
    message: Annotated[str, Field(..., description="Human-readable message")]
    data: Annotated[dict | None, Field(default=None, description="Additional diagnostic info")]


class JSONRPCResponse(BaseModel):
    """JSON-RPC response wrapper."""

    jsonrpc: Literal["2.0"]
    id: Annotated[int | str, Field(..., description="Corresponding request ID")]
    result: Annotated[dict | None, Field(default=None, description="Result if success")]
    error: Annotated[JSONRPCError | None, Field(default=None, description="Error object if failed")]