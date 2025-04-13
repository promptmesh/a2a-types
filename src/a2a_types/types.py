"""A2A-compatible message types exposed as Pydantic models."""

from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field


# === Agent Metadata ===

class AgentAuthentication(BaseModel):
    """Describes how an agent authenticates itself."""

    schemes: Annotated[list[str], Field(..., description="Supported auth schemes (e.g. bearer, basic)")]
    credentials: Annotated[str | None, Field(default=None, description="Credentials if statically defined")]


class AgentCapabilities(BaseModel):
    """Describes runtime features supported by an agent."""

    streaming: Annotated[bool, Field(default=False, description="Supports streaming content responses")]
    pushNotifications: Annotated[bool, Field(default=False, description="Agent can push async updates")]
    stateTransitionHistory: Annotated[bool, Field(default=False, description="Agent tracks full task history")]


class AgentProvider(BaseModel):
    """Metadata about the agent's providing organization."""

    organization: Annotated[str, Field(..., description="Name of the providing organization")]


class AgentSkill(BaseModel):
    """Describes a skill or intent that the agent supports."""

    id: Annotated[str, Field(..., description="Unique identifier for the skill")]
    name: Annotated[str, Field(..., description="Human-readable name for the skill")]
    description: Annotated[str | None, Field(default=None, description="Optional skill description")]
    tags: Annotated[list[str] | None, Field(default=None, description="Optional skill tags")]
    examples: Annotated[list[str] | None, Field(default=None, description="Sample inputs or use cases")]
    inputModes: Annotated[list[str] | None, Field(default=None, description="Supported input modes")]
    outputModes: Annotated[list[str] | None, Field(default=None, description="Supported output modes")]


class AgentCard(BaseModel):
    """Top-level declaration of an A2A-compatible agent."""

    name: Annotated[str, Field(..., description="Name of the agent")]
    description: Annotated[str | None, Field(default=None, description="Description of the agent")]
    url: Annotated[str, Field(..., description="Base URL for agent API")]
    provider: Annotated[AgentProvider | None, Field(default=None, description="Optional provider metadata")]
    version: Annotated[str, Field(..., description="Semantic version of the agent interface")]
    documentationUrl: Annotated[str | None, Field(default=None, description="URL to human-readable docs")]
    capabilities: Annotated[AgentCapabilities, Field(..., description="Runtime capabilities of the agent")]
    authentication: Annotated[AgentAuthentication | None, Field(default=None, description="Authentication config")]
    defaultInputModes: Annotated[list[str], Field(default_factory=lambda: ["text"], description="Preferred input modes")]
    defaultOutputModes: Annotated[list[str], Field(default_factory=lambda: ["text"], description="Preferred output modes")]
    skills: Annotated[list[AgentSkill], Field(default_factory=list, description="Declared agent skills")]


# === Content Types ===

class TextPart(BaseModel):
    """Represents a plain text content part."""
    type: Literal["text"] = "text"
    text: Annotated[str, Field(..., description="The text content")]


class FilePart(BaseModel):
    """Represents a file-like object."""
    type: Literal["file"] = "file"
    mimeType: Annotated[str | None, Field(default=None, description="MIME type of the file")]
    bytes: Annotated[str | None, Field(default=None, description="Base64-encoded file content")]
    uri: Annotated[str | None, Field(default=None, description="External URI to the file")]


class DataPart(BaseModel):
    """Represents structured, non-textual data."""
    type: Literal["data"] = "data"
    data: Annotated[dict, Field(..., description="Arbitrary JSON structure")]


Part = Union[TextPart, FilePart, DataPart]


# === Message & Artifact ===

class Message(BaseModel):
    """A message in a conversation or task."""

    role: Annotated[Literal["user", "agent"], Field(..., description="Who authored the message")]
    parts: Annotated[list[Part], Field(..., description="Multi-part structured message")]


class Artifact(BaseModel):
    """Represents output associated with a task."""

    name: Annotated[str | None, Field(default=None, description="Optional artifact name")]
    description: Annotated[str | None, Field(default=None, description="Optional description")]
    parts: Annotated[list[Part], Field(..., description="Content payload")]
    index: Annotated[int, Field(..., description="Order of artifact among results")]
    append: Annotated[bool | None, Field(default=None, description="Whether to append to previous artifact")]
    lastChunk: Annotated[bool | None, Field(default=None, description="Is this the final chunk?")]
    metadata: Annotated[dict | None, Field(default=None, description="Optional extra metadata")]


# === Task ===

class TaskStatus(BaseModel):
    """Encapsulates the lifecycle state of a task."""

    state: Annotated[
        Literal["submitted", "working", "input-required", "completed", "failed", "canceled"],
        Field(..., description="Task state enum"),
    ]
    message: Annotated[Message | None, Field(default=None, description="Optional message explaining state")]
    timestamp: Annotated[str | None, Field(default=None, description="ISO 8601 timestamp of transition")]


class Task(BaseModel):
    """Describes a unit of work tracked by the protocol."""

    id: Annotated[str, Field(..., description="Unique task ID")]
    sessionId: Annotated[str | None, Field(default=None, description="Optional client session grouping")]
    status: Annotated[TaskStatus, Field(..., description="Current status")]
    artifacts: Annotated[list[Artifact] | None, Field(default=None, description="Output artifacts")]
    history: Annotated[list[Message] | None, Field(default=None, description="Historical messages")]
    metadata: Annotated[dict | None, Field(default=None, description="Custom data attached to the task")]


# === Notification Config ===

class PushNotificationConfig(BaseModel):
    """Describes where the agent should send updates."""

    url: Annotated[str, Field(..., description="Callback endpoint")]
    token: Annotated[str | None, Field(default=None, description="Optional auth token")]
    authentication: Annotated[AgentAuthentication | None, Field(default=None, description="Push-specific auth")]


class TaskPushNotificationConfig(BaseModel):
    """Binds a task ID to a push notification target."""

    id: Annotated[str, Field(..., description="Task ID")]
    pushNotification: Annotated[PushNotificationConfig, Field(..., description="Notification configuration")]

# === Streaming Events ===

class TaskStatusUpdateEvent(BaseModel):
    """Describes a live update to task status."""

    id: Annotated[str, Field(..., description="Task ID")]
    status: Annotated[TaskStatus, Field(..., description="New status object")]
    final: Annotated[bool, Field(..., description="Is this the terminal state?")]
    metadata: Annotated[dict | None, Field(default=None, description="Additional event data")]


class TaskArtifactUpdateEvent(BaseModel):
    """Describes streamed artifact updates."""

    id: Annotated[str, Field(..., description="Task ID")]
    artifact: Annotated[Artifact, Field(..., description="Partial or full artifact")]
    final: Annotated[bool | None, Field(default=None, description="Is this the final update?")]
    metadata: Annotated[dict | None, Field(default=None, description="Event-level metadata")]