import tkinter as tk
from tkinter import ttk, messagebox

PRIMARY = "#0f766e"
ACCENT = "#0ea5e9"
BG = "#f5f7fb"
PANEL = "#ffffff"
TEXT = "#0f172a"
BORDER = "#e2e8f0"

class HelpDeskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PulseDesk | New Ticket")
        self.configure(bg=BG)
        self.geometry("720x720")
        self._build_styles()
        self._build_layout()

    def _build_styles(self):
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TFrame", background=BG)
        style.configure("Card.TFrame", background=PANEL, relief="flat")
        style.configure("TLabel", background=PANEL, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Lead.TLabel", foreground="#475569")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.map("TButton",
                  background=[("!active", PRIMARY), ("active", ACCENT)],
                  foreground=[("!active", "white"), ("active", "white")])
        style.configure("TEntry", padding=6)
        style.configure("TCombobox", padding=6)

    def _build_layout(self):
        container = ttk.Frame(self, padding=16, style="TFrame")
        container.pack(fill="both", expand=True)

        card = ttk.Frame(container, style="Card.TFrame")
        card.pack(fill="both", expand=True)
        card.configure(borderwidth=1, relief="solid")

        # Header
        header = ttk.Frame(card, padding=16, style="Card.TFrame")
        header.pack(fill="x")
        ttk.Label(header, text="New ticket", style="Lead.TLabel", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ttk.Label(header, text="Create a support request", style="Header.TLabel").pack(anchor="w", pady=(6, 0))
        ttk.Label(header, text="Describe the issue so we can route it.", style="Lead.TLabel").pack(anchor="w", pady=(4, 0))

        form = ttk.Frame(card, padding=16, style="Card.TFrame")
        form.pack(fill="both", expand=True)
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        self._add_field(form, "Full name", 0, columnspan=1, placeholder="Jane Doe")
        self._add_field(form, "Email", 0, column=1, placeholder="you@company.com")

        priorities = ["Choose priority", "P1 - Critical", "P2 - High", "P3 - Normal"]
        categories = ["Access & Accounts", "Hardware", "Network", "Software", "Other"]
        self._add_combo(form, "Priority", priorities, 1)
        self._add_combo(form, "Category", categories, 1, column=1)

        self._add_field(form, "Subject", 2, columnspan=2, placeholder="VPN client fails to connect")
        self._add_text(form, "Description", 3, columnspan=2, height=6)

        # Actions
        actions = ttk.Frame(card, padding=16, style="Card.TFrame")
        actions.pack(fill="x")
        submit = ttk.Button(actions, text="Submit ticket", command=self._submit)
        submit.pack(side="left", padx=(0, 10))
        cancel = ttk.Button(actions, text="Clear", command=self._clear, style="TButton")
        cancel.pack(side="left")

    def _add_field(self, parent, label, row, column=0, columnspan=1, placeholder=""):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.grid(row=row, column=column, columnspan=columnspan, sticky="nsew", padx=6, pady=6)
        ttk.Label(frame, text=label).pack(anchor="w")
        entry = ttk.Entry(frame)
        entry.pack(fill="x")
        entry.insert(0, placeholder)
        if not hasattr(self, "fields"):
            self.fields = {}
        self.fields[label] = entry

    def _add_combo(self, parent, label, options, row, column=0):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.grid(row=row, column=column, sticky="nsew", padx=6, pady=6)
        ttk.Label(frame, text=label).pack(anchor="w")
        combo = ttk.Combobox(frame, values=options, state="readonly")
        combo.current(0)
        combo.pack(fill="x")
        if not hasattr(self, "fields"):
            self.fields = {}
        self.fields[label] = combo

    def _add_text(self, parent, label, row, column=0, columnspan=1, height=6):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.grid(row=row, column=column, columnspan=columnspan, sticky="nsew", padx=6, pady=6)
        ttk.Label(frame, text=label).pack(anchor="w")
        text = tk.Text(frame, height=height, wrap="word", relief="flat", bd=1, highlightbackground=BORDER)
        text.pack(fill="both", expand=True)
        if not hasattr(self, "fields"):
            self.fields = {}
        self.fields[label] = text

    def _submit(self):
        # Simple popup to simulate submission
        values = {}
        for key, widget in self.fields.items():
            if isinstance(widget, tk.Text):
                values[key] = widget.get("1.0", "end").strip()
            else:
                values[key] = widget.get().strip()
        summary = "\n".join(f"{k}: {v}" for k, v in values.items())
        messagebox.showinfo("Ticket captured", f"Captured values:\n\n{summary}\n\nWire this to your backend.")

    def _clear(self):
        for widget in self.fields.values():
            if isinstance(widget, tk.Text):
                widget.delete("1.0", "end")
            else:
                widget.delete(0, "end")


if __name__ == "__main__":
    app = HelpDeskApp()
    app.mainloop()
