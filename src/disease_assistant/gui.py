from gradio import (
    JSON,
    Accordion,
    Audio,
    Blocks,
    Button,
    Chatbot,
    ChatInterface,
    Checkbox,
    Column,
    Dataframe,
    Dataset,
    Dropdown,
    File,
    Gallery,
    Group,
    HighlightedText,
    Image,
    Interface,
    Label,
    Model3D,
    Plot,
    Radio,
    Row,
    Slider,
    Tab,
    TabbedInterface,
    Textbox,
    Video,
)

from disease_assistant import graph


def debug_block() -> Blocks:
    with Blocks() as app:
        graph = Image(label="Graph")
        submit_button = Button("Submit")
        submit_button.click(graph.get_graph, None, graph)
    return app


def app_block() -> Blocks:
    with Blocks() as app:
        image = Image(label="Upload Image")
        text = Textbox(label="Enter text")
        with Row():
            with Column():
                submit_button = Button("Submit")
                chatbot = Chatbot(label="AI Response")
    # submit_button.click(process_input, inputs=[image, text], outputs=chatbot)
    return app
