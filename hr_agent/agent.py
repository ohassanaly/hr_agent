from typing import Annotated

from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from custom_tools import *
from langchain_tavily import TavilySearch

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# from langgraph.types import Command
from langsmith import traceable

from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    "openai:gpt-4.1",
    temperature=0.3,
)

search_tool = TavilySearch(max_results=2)
tools = [cv_info, linkedin_info, personnal_info, search_tool]
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = (
    "You are Olivier Hassanaly, a 3 years experienced Data Scientist. You are answering interview questions for an AI engineer job. "
    "You are given tools to look for your linkedin content if you are asked questions about your professional experience or to your personal expertiences if you are asked questions about your personal life"
)


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


@traceable(name="Olivier")
def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    # Because we will be interrupting during tool execution,
    # we disable parallel tool calling to avoid repeating any
    # tool invocations when we resume.
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}


graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)
