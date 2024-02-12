from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from rich.table import Table
from textual.renderables.digits import Digits

def create_report_panel(report):
    table = Table.grid(padding=1)
    table.add_column(max_width=25, style="blue on black")
    table.add_column(max_width=25, style="blue on black")
    table.add_column(max_width=5, justify="right", style="blue on black")

    # Add rows to the table
    for _, data in report.items():
        email = data["creator-email"]
        app_title = data["app-title"]
        count = str(data["count"])
        table.add_row(email, app_title, count)

    # Create a panel for the table
    report_panel = Panel(
        table,
        style="bold green on black",
        box=box.MINIMAL,
        expand=True,
    )
    return report_panel

def draw_screen(report, count):
    number_text = Digits(str(count), style="bold blue on black")
    number_panel = Panel(
        Align(number_text, align="center", vertical="middle"),
        title="Total Count",
        style="bold blue on black",
        box=box.MINIMAL,
        expand=True,
    )
    
    report_panel = create_report_panel(report)
    
    layout = Layout()
    layout.split_row(
        Layout(name="left"),
        Layout(name="right", minimum_size=35)
    )
    layout["left"].update(number_panel)
    layout["right"].update(report_panel)
    console = Console()

    console.print(layout, justify="center")

