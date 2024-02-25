from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from rich.table import Table
from textual.renderables.digits import Digits
from log import log 

def create_report_panel(report):
    table = Table.grid(padding=1)
    table.add_column(max_width=25, style="blue on black")
    table.add_column(max_width=25, style="blue on black")
    table.add_column(max_width=5, justify="right", style="blue on black")

    sorted_report_items = sorted(report.items(), key=lambda item: item[1]["count"], reverse=True)
    top_report_items = sorted_report_items[:4]  
    for _, data in top_report_items:
        email = data["creator-email"]
        app_title = data["app-title"]
        count = str(data["count"])
        table.add_row(email, app_title, count)

    report_panel = Panel(
        Align(table, align="center", vertical="middle"),
        style="bold green on black",
        box=box.MINIMAL,
        expand=True,
    )
    return report_panel

def status_color(status): 
    if status == 'connected':
        return "green"
    elif status == 'disconnected':
        return "red"
    else: 
        return "grey82" 

def create_status_panel(status):
    color = status_color(status)
    status_text = Text("●", style=color)
    status_panel = Panel(
        Align(status_text, align="center", vertical="top"),
        style=f"bold {color} on black",
        box=box.MINIMAL,
        expand=True,
    )
    return status_panel

def draw_screen(status, report, count):
    number_text = Digits(str(count), style="bold blue on black")
    number_panel = Panel(
        Align(number_text, align="center", vertical="middle"),
        style="bold blue on black",
        box=box.MINIMAL,
        expand=True,
    )
    
    report_panel = create_report_panel(report)
    
    status_panel = create_status_panel(status) 

    layout = Layout()
    layout.split_row(
        Layout(name="left"),
        Layout(name="right", minimum_size=35),
    )
    layout["left"].update(number_panel)
    layout["right"].update(report_panel)

    console = Console()

    console.print(layout, justify="center")

