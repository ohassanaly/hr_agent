from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver
from build import *
from dotenv import load_dotenv

load_dotenv()

graph_builder = StateGraph(State)

tool = TavilySearch(max_results=2)
tools = [tool]

llm = init_chat_model(
    "openai:gpt-4.1",
    temperature=0.3,
)

SYSTEM_PROMPT = "You are Olivier Hassanaly, a 3 years experienced Data Scientist. You are answering interview questions for an AI engineer job"

# tell the LLM which tools it can call
llm_with_tools = llm.bind_tools(tools)

memory = InMemorySaver()

@traceable(name="Chatbot Node")
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}
graph_builder.add_node("chatbot", chatbot)

tool_node = BasicToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", END: END}, #By default, the return value routing_function is used as the name of the node (or list of nodes) to send the state to next. All those nodes will be run in parallel as a part of the next superstep.
#You can optionally provide a dictionary that maps the routing_function's output to the name of the next node.
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile(checkpointer=memory)

def stream_graph_updates(user_input: str):
    
    config = {"configurable": {"thread_id": "1"}} #any thread id value works here
    for event in graph.stream({"messages": [{"role": "system", "content": SYSTEM_PROMPT},
                                            {"role": "user", "content": user_input}]},     
                                            config,
                              ):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

if __name__ == "__main__":

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_graph_updates(user_input)
        except Exception as e:
            print(e, "somehting went wrong")
            break