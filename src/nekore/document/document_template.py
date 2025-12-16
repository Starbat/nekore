from fpdf import FPDF

from .assets import top_ornament


class PDF(FPDF):
    def __init__(self) -> None:
        super().__init__()
        self.set_font("helvetica", size=11)

    def header(self) -> None:
        self.set_margin(0)
        self.image(top_ornament, w=self.epw)

    def footer(self) -> None:
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_text_color(0, 0, 0)
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Seite {self.page_no()}/{{nb}}", align="C")
