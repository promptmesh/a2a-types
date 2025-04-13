# a2a-types

A2A-compatible message types exposed as Pydantic models.

## Installation

```bash
uv add a2a-types
```

## Usage

```python
from a2a_types.types import AgentCard

card = AgentCard(
    name="My Agent",
    description="This is my agent.",
    url="https://example.com/api",
    provider=AgentProvider(organization="My Organization"),
    version="1.0.0",
    documentationUrl="https://example.com/docs",
    capabilities=AgentCapabilities(streaming=True, pushNotifications=True, stateTransitionHistory=True),
    authentication=AgentAuthentication(schemes=["bearer"], credentials="secret"),
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    skills=[
        AgentSkill(id="my-skill", name="My Skill", description="This is my skill.", tags=["tag1", "tag2"], examples=["example1", "example2"], inputModes=["text", "code"], outputModes=["text", "code"]),
    ],
)
```