from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from rich.table import Table
from textual.renderables.digits import Digits
from log import log 
from textual.widgets import Static

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

def create_report_panel(status, report):
    table = Table.grid(padding=1)
    table.add_column(max_width=25, style="blue")
    table.add_column(max_width=25, style="blue")
    table.add_column(max_width=5, justify="right", style="blue")
    sorted_report_items = sorted(report.items(), key=lambda item: item[1]["count"], reverse=True)
    top_report_items = sorted_report_items[:100]  
    for _, data in top_report_items:
        email = data["creator-email"]
        app_title = data["app-title"]
        count = str(data["count"])
        table.add_row(email, app_title, count)

    report_panel = Panel(
        Align(table, align="center", vertical="middle"),
        style="bold green",
        box=box.MINIMAL,
        expand=True,
    )
    return report_panel

def draw_screen(status, report, count):
    number_text = Digits(str(count), style="bold blue on black")
    number_panel = Panel(
        Align(number_text, align="center", vertical="middle"),
        style="bold blue on black",
        box=box.MINIMAL,
        expand=True,
    )
    
    report_panel = create_report_panel(status, report)

    layout = Layout()
    layout.split_row(
        Layout(name="left"),
        Layout(name="right", minimum_size=35),
    )
    layout["left"].update(number_panel)
    layout["right"].update(report_panel)

    console = Console()

    console.print(layout, justify="center")
# rand int 
import random 

# create a report with 25 items 
def create_report():
    report = {}
    for i in range(50):
        report[str(i)] = {"count": i, "creator-email": "a" + str(random.randint(0, 100)), "app-title": "a" + str(i) }
    return report 

report = create_report() 

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll , Middle
from textual.widgets import Input, Markdown, Digits, DataTable
# vertical scroll background should be transparent 

class InstometerApp(App):
    CSS = """
    Screen {
        layout: grid; 
        grid-size: 2;
        grid-columns: auto 1fr;
    }
    #digits {
        padding: 1 3;
    }
    #right { 
        padding: 1;
    }
    #status {  
        text-align: right; 
        padding-bottom: 1;
    }
    #report { 
        scrollbar-size-vertical: 0;
    }
    """

    def compose(self) -> ComposeResult:
        yield Digits("55", id="digits")
        yield Vertical( 
            Static(status_text("connected"), id="status"),
            VerticalScroll(
                Static(create_report_panel("connected", report)), 
                id="report" 
            ), 
            id="right"
        )
if __name__ == "__main__":
    app = InstometerApp()
    app.run()
