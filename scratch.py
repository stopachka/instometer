from __future__ import annotations

from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Markdown, Digits, DataTable

def status_color(status): 
    if status == 'connected':
        return "green"
    elif status == 'disconnected':
        return "red"
    else: 
        return "grey82" 

def status_text(status):
    color = status_color(status)
    status_text = Text("●", style=color)
    return status_text

class InstometerApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    #pi {
        border: double green;
        width: auto;
    }
    """

    def compose(self) -> ComposeResult:
        yield Digits("5", id="digits") 

if __name__ == "__main__":
    app = InstometerApp()
    app.run()
