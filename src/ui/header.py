from rich.align import Align
from rich.panel import Panel

ASCII_ART: str = """
    Art by Joan Stark
          ,_     _,       _     /)---(\\            /~~~\\
          |\\\___//|       \\\   (/ . . \\)          /  .. \\
          |=6   6=|        \\\__)-\\(.)/           (_,\\  |_)
          \\=._Y_.=/        \\_       (_           /   \\@/     /^^^\\
           )  `  (    ,    (___/-(____)   _     /      \\    / . . \\
          /       \\  ((                   \\\   /  `    |    V\\ Y /V
          |       |   ))     WELCOME TO    \\\/  \\   | _\\     / - \\
         /| |   | |\\_//    Pet Adoption!    \\   /__'|| \\\_   |    \\
    jgs  \\| |._.| |/-`                       \\_____)|_).\\_). ||(__v
          '"'   '"'
"""


def header(title: str) -> Panel:
    return Panel(Align.center(ASCII_ART),
                 title=title, style="violet")
