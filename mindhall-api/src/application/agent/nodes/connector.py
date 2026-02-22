"""Connector node: no-op routing. Next step determined by conditional_edges (should_summarize_conversation)."""

from typing import Any

from src.application.agent.states.agent_state import AgentState


class ConnectorNode:
    """Pure routing node. Returns empty state delta; edges determine next node."""

    def __call__(self, state: AgentState) -> dict[str, Any]:
        return {}
