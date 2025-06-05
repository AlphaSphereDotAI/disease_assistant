from gradio import (
    Blocks,
    Button,
    Chatbot,
    Column,
    Image,
    Row,
    Textbox,
)

from disease_assistant import graph


def debug_block() -> Blocks:
    with Blocks() as app:
        graph_img: Image = Image(label="Graph")
        submit_button: Button = Button("Submit")
        submit_button.click(graph.png, None, graph_img)
    return app


def app_block() -> Blocks:
    with Blocks() as app:
        image: Image = Image(label="Upload Image")
        text: Textbox = Textbox(label="Enter text")
        with Row():
            with Column():
                submit_button: Button = Button("Submit")
                chatbot: Chatbot = Chatbot(label="AI Response")
    # submit_button.click(process_input, inputs=[image, text], outputs=chatbot)
    return app
