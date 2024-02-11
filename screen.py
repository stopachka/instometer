from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from textual.renderables.digits import Digits

def draw_screen(count):
    console = Console()
    layout = Layout()

    number_text = Digits(str(count), style="bold blue on black") 

    number_panel = Panel(
        Align(number_text, align="center", vertical="middle"),
        style="bold blue on black", 
        box=box.MINIMAL, 
        expand=True,
    )
    layout.update(number_panel) 
    console.print(layout, justify="center")

