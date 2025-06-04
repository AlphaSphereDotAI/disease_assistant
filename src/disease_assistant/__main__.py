from gradio import TabbedInterface

from disease_assistant import DEBUG, SERVER_NAME, SERVER_PORT
from disease_assistant.gui import app_block, debug_block


def main() -> None:
    """Launch the Gradio voice generation web application."""
    app = TabbedInterface([app_block(), debug_block()], ["App", "Debug"])
    app.queue(api_open=True).launch(
        server_name=SERVER_NAME,
        server_port=SERVER_PORT,
        debug=DEBUG,
        mcp_server=True,
        show_api=True,
        enable_monitoring=True,
        show_error=True,
    )


if __name__ == "__main__":
    main()
