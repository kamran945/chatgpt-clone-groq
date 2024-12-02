from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage

from langgraph.graph.message import AnyMessage, add_messages


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
