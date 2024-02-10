from rich.console import Console, ConsoleOptions, RenderResult
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style, StyleType

DIGITS = " 0123456789+-^x:"
DIGITS3X3 = """\



┏━┓
┃ ┃
┗━┛
 ┓
 ┃
╺┻╸
╺━┓
┏━┛
┗━╸
╺━┓
 ━┫
╺━┛
╻ ╻
┗━┫
  ╹
┏━╸
┗━┓
╺━┛
┏━╸
┣━┓
┗━┛
╺━┓
  ┃
  ╹
┏━┓
┣━┫
┗━┛
┏━┓
┗━┫
╺━┛

╺╋╸


╺━╸

 ^



 ×


 :

""".splitlines()


class Digits:
    """Renders a 3X3 unicode 'font' for numerical values.

    Args:
        text: Text to display.
        style: Style to apply to the digits.

    """

    def __init__(self, text: str, style: StyleType = "") -> None:
        self._text = text
        self._style = style

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        style = console.get_style(self._style)
        yield from self.render(style)

    def render(self, style: Style) -> RenderResult:
        """Render with the given style

        Args:
            style: Rich Style.

        Returns:
            Result of render.
        """
        digit_pieces: list[list[str]] = [[], [], []]
        row1 = digit_pieces[0].append
        row2 = digit_pieces[1].append
        row3 = digit_pieces[2].append

        for character in self._text:
            try:
                position = DIGITS.index(character) * 3
            except ValueError:
                row1(" ")
                row2(" ")
                row3(character)
            else:
                row1(DIGITS3X3[position].ljust(3))
                row2(DIGITS3X3[position + 1].ljust(3))
                row3(DIGITS3X3[position + 2].ljust(3))

        new_line = Segment.line()
        for line in digit_pieces:
            yield Segment("".join(line), style)
            yield new_line

    @classmethod
    def get_width(cls, text: str) -> int:
        """Calculate the width without rendering.

        Args:
            text: Text which may be displayed in the `Digits` widget.

        Returns:
            width of the text (in cells).
        """
        width = sum(3 if character in DIGITS else 1 for character in text)
        return width

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        width = self.get_width(self._text)
        return Measurement(width, width)


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
    number_text = Digits(str(count), style="bold blue on black") 

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

