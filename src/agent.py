from langgraph.graph import START, StateGraph, END
from langchain_core.messages import HumanMessage
from typing import Generator

from src.state import State
from src.llm import llm


def stream_values(response) -> Generator[str, None, None]:
    for msg, metadata in response:
        if (
            msg.content
            and not isinstance(msg, HumanMessage)
            and metadata["langgraph_node"] == "generate"
        ):
            # print(msg.content, end="|", flush=True)
            # print(msg.content, end="", flush=True)
            yield msg.content


def generate(state: State):
    messages = state["messages"]
    response = llm.invoke(messages)
    # print(f"AGENT RESPONSE TO HUMAN MSG: {response.content}")

    return {"messages": response}


def get_graph():
    workflow = StateGraph(State)

    workflow.add_node("generate", generate)
    workflow.set_entry_point("generate")
    workflow.add_edge("generate", END)

    graph = workflow.compile()

    return graph
