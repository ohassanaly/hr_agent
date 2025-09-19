from agent import *
from langchain_core.messages import AIMessage


def is_final_ai(msg) -> bool:
    if not isinstance(msg, AIMessage):
        return False
    # Skip assistant messages that are tool calls or have no content
    has_tool_calls = bool(getattr(msg, "tool_calls", None)) or bool(
        getattr(msg, "additional_kwargs", {}).get("tool_calls")
    )
    has_text = bool(getattr(msg, "content", None) and msg.content.strip())
    return (not has_tool_calls) and has_text


def stream_graph_updates(user_input: str):
    config = {"configurable": {"thread_id": "1"}}  # any thread id value works here
    for event in graph.stream(
        {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ]
        },
        config,
    ):
        for value in event.values():
            msgs = value["messages"]
            # Only pick AI messages (the model's replies)
            ai_msgs = [m for m in msgs if is_final_ai(m)]
            if ai_msgs:
                print("Olivier:", ai_msgs[-1].content)

            # print("Olivier:", value["messages"][-1].content)


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
