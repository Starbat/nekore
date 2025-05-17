import datetime as dt
from dataclasses import dataclass
from typing import Final

from fpdf import FPDF

from nekore.models import Accounting, Contact

from .document_template import PDF


@dataclass(frozen=True, slots=True)
class FontSize:
    TEXT = 11
    TABLE = 10
    H1 = 16
    H2 = 14


@dataclass(frozen=True, slots=True)
class Color:
    DARKGREEN = {"r": 70, "g": 138, "b": 26}
    BLACK = {"r": 0, "g": 0, "b": 0}
    DARKRED = {"r": 200, "g": 0, "b": 0}
    GRAY = {"r": 220, "g": 220, "b": 220}


class DocumentGenerator:
    def create_documents(self, directory: str, accountings: list[Accounting]) -> None:
        for n, accounting in enumerate(accountings):
            doc = self.create_document(accounting)
            datestr = accounting.date.strftime("%Y-%m-%d")
            file = f"{datestr}_Abrechnung_{n + 1}_{accounting.recipient.name}.pdf"
            doc.output(f"{directory}/{file}")

    def format_address(self, issuer: Contact, separator: str) -> str:
        sections: Final = (
            issuer.name,
            f"{issuer.street} {issuer.house_number}",
            f"{issuer.zip_code} {issuer.city}",
        )
        return separator.join(sections)

    def create_document(self, accounting: Accounting) -> PDF:
        pdf = PDF()
        pdf.add_page()
        pdf.set_margin(10)
        # Accounting issuer
        pdf.cell(w=None, h=20, text=self.format_address(accounting.issuer, " | "))
        # Accounting date
        pdf.cell(0, 20, dt.date.today().strftime("%d.%m.%Y"), align="R")
        pdf.ln()

        pdf.multi_cell(0, 6, self.format_address(accounting.recipient, "\n"))
        pdf.ln()

        self.create_h1(
            pdf,
            "Betriebskostenabrechnung "
            + f"{accounting.accounting_period.start.strftime('%d.%m.%Y')} - "
            + accounting.accounting_period.end.strftime("%d.%m.%Y"),
        )

        self.basic_data_table(pdf, accounting)

        self.create_h2(pdf, "Umlageschlüssel")

        self.name_value_table(
            pdf,
            STK="Nach Anzahl der Wohneinheiten",
            PNZ="Nach Personenanzahl und Nutzungszeitraum",
            NHN="Nach Nutzfläche der Wohneinheiten",
        )

        self.create_h2(pdf, "Zusammenfassung")

        pdf.set_font("helvetica", "", FontSize.TEXT)
        pdf.set_text_color(**Color.BLACK)

        third_width = pdf.epw / 3
        pdf.cell(third_width, 8, "Ihre Betriebskosten", align="L")
        pdf.cell(third_width, 8, "(inkl. ges. MwSt.)", align="C")
        pdf.cell(
            third_width,
            8,
            f"{accounting.gross_total:.2f} EUR".replace(".", ","),
            align="R",
        )
        pdf.ln()

        pdf.cell(third_width, 8, "Ihre Vorauszahlung", align="L")
        pdf.cell(third_width, 8, "(inkl. ges. MwSt.)", align="C")
        pdf.cell(
            third_width, 8, f"{accounting.prepaid:.2f} EUR".replace(".", ","), align="R"
        )
        pdf.ln()

        pdf.set_fill_color(**Color.GRAY)
        pdf.set_text_color(
            **Color.DARKGREEN if accounting.has_refund else Color.DARKRED
        )
        pdf.set_font("helvetica", "B", FontSize.TEXT)
        pdf.cell(
            third_width,
            8,
            "Ihre Rückzahlung" if accounting.has_refund else "Ihre Nachzahlung",
            fill=True,
        )
        pdf.cell(
            third_width,
            8,
            "(inkl. ges. MwSt.)",
            fill=True,
            align="C",
        )
        pdf.cell(
            third_width,
            8,
            f"{abs(accounting.refund):.2f} EUR".replace(".", ","),
            fill=True,
            align="R",
        )
        pdf.ln()

        pdf.set_font("helvetica", "", FontSize.TEXT)
        pdf.set_text_color(**Color.BLACK)
        if accounting.has_refund:
            pdf.cell(
                0,
                15,
                "Sie erhalten Ihre Rückzahlung innerhalb der nächsten 28 Tage als "
                "Überweisung auf Ihr Konto.",
            )
        else:
            pdf.cell(
                0,
                15,
                "Bitte überweisen Sie den Nachzahlungsbetrag innerhalb der "
                "nächsten 28 Tage.",
            )
            pdf.ln()
            if accounting.issuer.bank_account is not None:
                pdf.cell(40, 8, f"{accounting.issuer.name}")
                pdf.cell(40, 8, f"{accounting.issuer.bank_account.bank}")
                pdf.cell(60, 8, f"{accounting.issuer.bank_account.iban}")
                pdf.cell(0, 8, f"{accounting.issuer.bank_account.bic}")

        pdf.add_page()
        pdf.set_margin(10)
        self.create_h2(pdf, "Umlage Nebenkosten")
        self.create_allocation_table(pdf, accounting)

        self.create_h2(pdf, "Ausweis von Arbeitskosten nach § 35a EStG")
        self.create_labor_cost_table(pdf, accounting)
        return pdf

    def create_h1(self, pdf: FPDF, text: str) -> None:
        pdf.set_fill_color(**Color.DARKGREEN)
        pdf.cell(pdf.epw, 0.7, "", new_y="NEXT", new_x="LMARGIN", fill=True)
        pdf.ln()
        pdf.set_font("helvetica", "B", FontSize.H1)
        pdf.set_text_color(**Color.DARKGREEN)
        pdf.set_draw_color(**Color.DARKGREEN)
        pdf.cell(0, 15, text, border="T")
        pdf.ln()

    def create_h2(self, pdf: FPDF, text: str) -> None:
        pdf.set_font("helvetica", "B", FontSize.H2)
        pdf.set_text_color(**Color.DARKGREEN)
        pdf.cell(0, 12, text, new_y="NEXT", new_x="LMARGIN")

    def basic_data_table(self, pdf: FPDF, accounting: Accounting) -> None:
        basic_data: Final = {
            "Lage": accounting.apartment_name,
            "Nutzfläche": f"{accounting.floor_space:.2f} m²".replace(".", ","),
            "Personen": str(accounting.number_of_people),
            "Abrechnungszeitraum": (
                f"{accounting.accounting_period.start.strftime('%d.%m.%Y')} - "
                + accounting.accounting_period.end.strftime("%d.%m.%Y")
                + f", {accounting.accounting_period.duration.days} Tage"
            ),
            "Nutzungszeitraum": (
                f"{accounting.usage_period.start.strftime('%d.%m.%Y')} - "
                + accounting.usage_period.end.strftime("%d.%m.%Y")
                + f", {accounting.usage_period.duration.days} Tage"
            ),
        }
        self.name_value_table(pdf, **basic_data)

    def name_value_table(self, pdf: FPDF, **kwargs: str) -> None:
        pdf.set_font("helvetica", "", FontSize.TEXT)
        pdf.set_text_color(**Color.BLACK)
        for key, value in kwargs.items():
            pdf.cell(70, 6, key, align="L")
            pdf.cell(
                30,
                6,
                value,
                align="L",
                new_y="NEXT",
                new_x="LMARGIN",
            )
        pdf.ln()

    def create_allocation_table(self, pdf: FPDF, accounting: Accounting) -> None:
        # Table header
        pdf.set_text_color(**Color.BLACK)
        pdf.set_draw_color(**Color.BLACK)
        pdf.set_font("helvetica", "B", FontSize.TABLE)
        header_align = "L"
        pdf.epw
        col_w: list[int] = [55, 20, 30, 24, 30, 0]
        pdf.cell(col_w[0], 6, "Kategorie", border="B", align=header_align)
        pdf.cell(col_w[1], 6, "Schlüssel", border="B", align=header_align)
        pdf.cell(col_w[2], 6, "Anteile gesamt", border="B", align=header_align)
        pdf.cell(col_w[3], 6, "Ihre Anteile", border="B", align=header_align)
        pdf.cell(col_w[4], 6, "Gesamtkosten", border="B", align=header_align)
        pdf.cell(col_w[5], 6, "Ihr Kostenanteil", border="B", align=header_align)
        pdf.ln()
        # Table content
        pdf.set_font("helvetica", "", FontSize.TABLE)
        for n, ai in enumerate(accounting.allocation_items):
            last_row = n == len(accounting.allocation_items) - 1
            border = "B" if last_row else ""

            pdf.cell(col_w[0], 6, ai.name, border=border)
            pdf.cell(col_w[1], 6, ai.allocation_name, border=border)
            pdf.cell(
                col_w[2],
                6,
                f"{ai.shares_total:.2f}".replace(".", ","),
                border=border,
                align="R",
            )
            pdf.cell(
                col_w[3],
                6,
                f"{ai.shares_allocated:.2f}".replace(".", ","),
                border=border,
                align="R",
            )
            pdf.cell(
                col_w[4],
                6,
                f"{ai.gross_total:.2f} EUR".replace(".", ","),
                border=border,
                align="R",
            )
            pdf.cell(
                col_w[5],
                6,
                f"{ai.gross_share:.2f} EUR".replace(".", ","),
                border=border,
                align="R",
            )
            pdf.ln()
        pdf.set_font("helvetica", "", FontSize.TEXT)
        pdf.cell(
            0,
            8,
            f"Summe: {accounting.gross_total:.2f} EUR".replace(".", ","),
            align="R",
        )
        pdf.ln()
        pdf.cell(
            0,
            8,
            f"Vorauszahlung: {accounting.prepaid:.2f} EUR".replace(".", ","),
            align="R",
        )
        pdf.ln()
        pdf.set_text_color(
            **Color.DARKGREEN if accounting.has_refund else Color.DARKRED
        )
        pdf.cell(
            0,
            8,
            f"{'Ihre Rückzahlung' if accounting.has_refund else 'Ihre Nachzahlung'}: "
            f"{abs(accounting.refund):.2f} EUR".replace(".", ","),
            align="R",
        )
        pdf.ln()

    def create_labor_cost_table(self, pdf: FPDF, accounting: Accounting) -> None:
        pdf.set_text_color(**Color.BLACK)
        pdf.set_draw_color(**Color.BLACK)
        pdf.set_font("helvetica", "B", FontSize.TABLE)
        col_w: list[int] = [55, 40, 27, 27, 15, 0]
        # Table header
        header_align = "L"
        pdf.cell(col_w[0], 6, "Kategorie", border="B", align=header_align)
        pdf.cell(col_w[1], 6, "Dienstleister", border="B", align=header_align)
        pdf.cell(col_w[2], 6, "Kosten", border="B", align=header_align)
        pdf.cell(col_w[3], 6, "begünstigt", border="B", align=header_align)
        pdf.cell(col_w[4], 6, "Faktor", border="B", align=header_align)
        pdf.cell(col_w[5], 6, "Anteil", border="B", align=header_align)
        pdf.ln()
        # Table content
        pdf.set_font("helvetica", "", FontSize.TABLE)
        for n, lci in enumerate(accounting.labor_cost_items):
            last_row = n == len(accounting.labor_cost_items) - 1
            border = "B" if last_row else ""

            pdf.cell(col_w[0], 6, lci.collection_name, border=border)
            pdf.cell(col_w[1], 6, lci.issuer_name, border=border, align="R")
            pdf.cell(
                col_w[2],
                6,
                f"{lci.gross_amount:.2f} EUR".replace(".", ","),
                border=border,
                align="R",
            )
            pdf.cell(
                col_w[3],
                6,
                f"{lci.privileged_amount:.2f} EUR".replace(".", ","),
                border=border,
                align="R",
            )
            pdf.cell(
                col_w[4],
                6,
                f"{lci.factor:.2f}".replace(".", ","),
                border=border,
                align="R",
            )
            pdf.cell(
                col_w[5],
                6,
                f"{lci.share_amount:.2f} EUR".replace(".", ","),
                border=border,
                align="R",
            )
            pdf.ln()
        pdf.cell(
            0,
            8,
            f"Summe: {accounting.labor_costs_total:.2f} EUR".replace(".", ","),
            align="R",
        )
