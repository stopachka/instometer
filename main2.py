from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from art import text2art 

def render_full_screen_count(count):
    console = Console()
    layout = Layout()

    # Create a Text object for the number, styled to be large
    art = text2art(str(count)) 
    number_text = Text(art, style="bold blue on black")
    number_text.stylize("bold", 0, len(str(count)))

    # Create another Text object for the subtitle
    subtitle_text = Text("instant users", style="bold blue on black")

    # Center the number text vertically and horizontally
    number_panel = Panel(
        Align(number_text, align="center", vertical="middle"), 
        box=box.MINIMAL
    )
    
    # Center the subtitle text horizontally
    subtitle_panel = Panel(
        Align(subtitle_text, align="center", vertical="middle"), 
        box=box.MINIMAL
    )

    # Update the layout with the panels
    layout.update(number_panel)

    # Use console height to add padding for vertical centering
    console_height = console.size.height
    top_padding = (console_height - 3) // 2  # 3 is approximate height of text
    bottom_padding = top_padding

    # Print the panels to the console, with padding to center them
    console.print(Panel("", height=top_padding, style="on black", expand=False, box=box.MINIMAL))
    console.print(number_panel)
    console.print(subtitle_panel)
    console.print(Panel("", height=bottom_padding, style="on black", expand=False, box=box.MINIMAL))

# Example usage:
render_full_screen_count(300)

