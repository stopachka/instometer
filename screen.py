from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from rich.table import Table
from textual.renderables.digits import Digits

def create_report_panel(report):
    table = Table(show_header=False, style="blue on black")
    table.add_column(max_width=10, style="blue on black")
    table.add_column(max_width=10, style="blue on black")
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
    console = Console()
    layout = Layout()

    # Create the total count panel
    number_text = Digits(str(count), style="bold blue on black")
    number_panel = Panel(
        Align(number_text, align="center", vertical="middle"),
        title="Total Count",
        style="bold blue on black",
        box=box.MINIMAL,
        expand=True,
    )

    # Create the report panel
    report_panel = create_report_panel(report)

    # Split the layout into two parts
    layout.split_row(
        Layout(name="left"),
        Layout(name="right")
    )

    # Update the left and right parts of the layout
    layout["left"].update(number_panel)
    layout["right"].update(report_panel)

    # Print the layout
    console.print(layout, justify="center")

