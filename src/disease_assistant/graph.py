from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq.chat_models import ChatGroq
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from matplotlib.pyplot import savefig


class Graph:
    def __init__(self, sys_msg: str):
        self.sys_msg = sys_msg
        self.tools = [self.multiply, self.add, self.divide]
        self.llm_with_tools = ChatGroq(
            model="llama3-70b-8192",
            temperature=0,
            api_key="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",
        ).bind_tools(
            self.tools,
            parallel_tool_calls=False,
        )
        _builder = StateGraph(MessagesState)
        _builder.add_node("assistant", self.assistant)
        _builder.add_node("tools", ToolNode(self.tools))
        _builder.add_edge(START, "assistant")
        _builder.add_conditional_edges(
            "assistant",
            # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
            # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
            tools_condition,
        )
        _builder.add_edge("tools", "assistant")
        self.react_graph = _builder.compile()

    def assistant(self, state: MessagesState):
        return {
            "messages": [self.llm_with_tools.invoke([self.sys_msg] + state["messages"])]
        }

    def get_graph(self):
        return self.react_graph.get_graph(xray=True).draw_ascii()

    def multiply(self, a: int, b: int) -> int:
        """Multiply a and b.

        Args:
            a: first int
            b: second int
        """
        return a * b

    # This will be a tool
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
    sys_msg = SystemMessage(
        content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
    )
    graph = Graph(sys_msg)
    print(graph.get_graph())
    messages = [
        HumanMessage(
            content="Add 3 and 4. Multiply the output by 2. Divide the output by 5"
        )
    ]
    messages = graph.react_graph.invoke({"messages": messages})
    for m in messages["messages"]:
        m.pretty_print()
