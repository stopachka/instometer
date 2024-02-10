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

