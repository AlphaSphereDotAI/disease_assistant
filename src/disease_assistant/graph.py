from typing import Any, Callable, Sequence

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import Runnable
from langchain_groq.chat_models import ChatGroq
from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import CachePolicy

from disease_assistant.state import State


class Graph:
    react_graph: CompiledStateGraph
    llm_with_tools: Runnable[
        PromptValue
        | str
        | Sequence[BaseMessage | list[str] | tuple[str, str] | str | dict[str, Any]],
        BaseMessage,
    ]
    sys_msg: SystemMessage
    tools: list[Callable[[int, int], int | float]]

    def __init__(self, system_message: SystemMessage) -> None:
        self.sys_msg = system_message
        self.tools = [self.multiply, self.add, self.divide]
        self.llm_with_tools = ChatGroq(
            model="llama3-70b-8192", temperature=0
        ).bind_tools(self.tools, parallel_tool_calls=False)
        _builder: StateGraph = StateGraph(State)
        _builder.add_node(
            "assistant", self.assistant, cache_policy=CachePolicy(ttl=120)
        )
        _builder.add_node(
            "tools", ToolNode(self.tools), cache_policy=CachePolicy(ttl=120)
        )
        _builder.add_edge(START, "assistant")
        _builder.add_conditional_edges(
            "assistant",
            # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
            # If the latest message (result) from assistant is not a tool call -> tools_condition routes to END
            tools_condition,
        )
        _builder.add_edge("tools", "assistant")
        self.react_graph = _builder.compile()

    def assistant(self, state: State) -> dict[str, list[BaseMessage]]:
        return {
            "messages": [self.llm_with_tools.invoke([self.sys_msg] + state.messages)]
        }

    # def png(self) -> bytes:
    #     return self.react_graph.get_graph(xray=True).draw_png(output_file_path=None)

    def multiply(self, a: int, b: int) -> int:
        """Multiply a and b.
        :param a:
        :param b:
        :return:
        """
        return a * b

    def add(self, a: int, b: int) -> int:
        """Adds a and b.

        Args:
            a: first int
            b: second int
        """
        return a + b

    def divide(self, a: int, b: int) -> float:
        """Divide a and b.

        Args:
            a: first int
            b: second int
        """
        return a / b


if __name__ == "__main__":
    sys_msg: SystemMessage = SystemMessage(
        content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
    )
    graph: Graph = Graph(sys_msg)
    user_messages: list[HumanMessage] = [
        HumanMessage(
            content="Add 3 and 4. Multiply the output by 2. Divide the output by 5"
        )
    ]
    messages: dict[str, Any] | Any = graph.react_graph.invoke(
        {"messages": user_messages}
    )
    for m in messages["messages"]:
        m.pretty_print()
