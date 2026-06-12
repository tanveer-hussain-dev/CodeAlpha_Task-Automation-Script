# ============================================================
#   TASK AUTOMATION TOOLKIT — GUI VERSION
#   CodeAlpha Python Internship — Task 3
#   Author  : [Your Name]
#   Version : 2.0  (Tkinter GUI)
# ============================================================

import os
import re
import shutil
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

# ── Colors ────────────────────────────────────────────────
BG_DARK      = "#0f0f1a"
BG_CARD      = "#1a1a2e"
BG_PANEL     = "#16213e"
ACCENT_BLUE  = "#4cc9f0"
ACCENT_GREEN = "#4ade80"
ACCENT_RED   = "#f72585"
ACCENT_GOLD  = "#fbbf24"
ACCENT_PURP  = "#a78bfa"
TEXT_WHITE   = "#e2e8f0"
TEXT_DIM     = "#64748b"
BTN_BG       = "#1e293b"


# ════════════════════════════════════════════════════════
#  MAIN APP
# ════════════════════════════════════════════════════════

class AutomationApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self._setup_window()
        self._build_ui()

    def _setup_window(self):
        self.root.title("Task Automation Toolkit — CodeAlpha")
        self.root.geometry("900x660")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_DARK)
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 900) // 2
        y = (self.root.winfo_screenheight() - 660) // 2
        self.root.geometry(f"900x660+{x}+{y}")

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg=BG_DARK)
        hdr.pack(fill="x", padx=30, pady=(20, 0))
        tk.Label(hdr, text="🤖  TASK AUTOMATION TOOLKIT",
                 font=("Courier New", 22, "bold"),
                 fg=ACCENT_BLUE, bg=BG_DARK).pack(side="left")
        tk.Label(hdr, text="CodeAlpha  •  Task 3",
                 font=("Courier New", 10), fg=TEXT_DIM, bg=BG_DARK).pack(side="right", pady=8)
        tk.Frame(self.root, bg=ACCENT_BLUE, height=2).pack(fill="x", padx=30, pady=(6, 14))

        # Tab bar (manual tabs for full dark styling)
        self._active_tab = tk.StringVar(value="jpg")
        tab_bar = tk.Frame(self.root, bg=BG_DARK)
        tab_bar.pack(fill="x", padx=30, pady=(0, 10))

        self._tab_buttons = {}
        tabs = [("jpg",   "📁  Move JPG Files"),
                ("email", "📧  Extract Emails"),
                ("scrape","🌐  Scrape Title")]

        for key, label in tabs:
            btn = tk.Button(tab_bar, text=label,
                            font=("Courier New", 10, "bold"),
                            relief="flat", pady=7, padx=14,
                            cursor="hand2",
                            command=lambda k=key: self._switch_tab(k))
            btn.pack(side="left", padx=(0, 4))
            self._tab_buttons[key] = btn

        # Content frames
        self._frames = {}
        container = tk.Frame(self.root, bg=BG_DARK)
        container.pack(fill="both", expand=True, padx=30)

        self._frames["jpg"]    = self._build_jpg_tab(container)
        self._frames["email"]  = self._build_email_tab(container)
        self._frames["scrape"] = self._build_scrape_tab(container)

        # Log area (shared)
        tk.Label(self.root, text="LOG OUTPUT", font=("Courier New", 9, "bold"),
                 fg=TEXT_DIM, bg=BG_DARK).pack(anchor="w", padx=30, pady=(10, 2))

        log_frame = tk.Frame(self.root, bg=BG_DARK)
        log_frame.pack(fill="x", padx=30, pady=(0, 16))

        self.log_text = tk.Text(log_frame, height=7,
                                bg=BG_CARD, fg=ACCENT_GREEN,
                                font=("Courier New", 9),
                                relief="flat", bd=6,
                                insertbackground=ACCENT_BLUE,
                                state="disabled")
        self.log_text.pack(fill="x")

        # Tag colors for log
        self.log_text.tag_config("ok",    foreground=ACCENT_GREEN)
        self.log_text.tag_config("err",   foreground=ACCENT_RED)
        self.log_text.tag_config("info",  foreground=ACCENT_BLUE)
        self.log_text.tag_config("head",  foreground=ACCENT_GOLD)

        self._switch_tab("jpg")

    # ── Tab switcher ──────────────────────────────────────
    def _switch_tab(self, key: str):
        for k, f in self._frames.items():
            f.pack_forget()
        self._frames[key].pack(fill="both", expand=True)
        self._active_tab.set(key)
        for k, btn in self._tab_buttons.items():
            if k == key:
                btn.config(bg=ACCENT_BLUE, fg=BG_DARK)
            else:
                btn.config(bg=BTN_BG, fg=TEXT_DIM)

    # ══════════════════════════════════════════════════════
    #  TAB 1 — Move JPG Files
    # ══════════════════════════════════════════════════════
    def _build_jpg_tab(self, parent) -> tk.Frame:
        f = tk.Frame(parent, bg=BG_CARD)

        tk.Label(f, text="Move all .jpg / .jpeg files from one folder to another.",
                 font=("Courier New", 10), fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w", padx=16, pady=(14, 10))

        # Source folder
        src_row = tk.Frame(f, bg=BG_CARD)
        src_row.pack(fill="x", padx=16, pady=4)
        tk.Label(src_row, text="Source Folder :", font=("Courier New", 10),
                 fg=TEXT_WHITE, bg=BG_CARD, width=18, anchor="w").pack(side="left")
        self.jpg_src = tk.StringVar()
        tk.Entry(src_row, textvariable=self.jpg_src,
                 font=("Courier New", 10), bg=BG_PANEL, fg=TEXT_WHITE,
                 insertbackground=ACCENT_BLUE, relief="flat", bd=4, width=42).pack(side="left", padx=(0,6))
        tk.Button(src_row, text="Browse", font=("Courier New", 9),
                  bg=BTN_BG, fg=ACCENT_BLUE, relief="flat", padx=8,
                  cursor="hand2",
                  command=lambda: self.jpg_src.set(
                      filedialog.askdirectory(title="Select Source Folder") or self.jpg_src.get()
                  )).pack(side="left")

        # Dest folder
        dst_row = tk.Frame(f, bg=BG_CARD)
        dst_row.pack(fill="x", padx=16, pady=4)
        tk.Label(dst_row, text="Destination Folder :", font=("Courier New", 10),
                 fg=TEXT_WHITE, bg=BG_CARD, width=18, anchor="w").pack(side="left")
        self.jpg_dst = tk.StringVar(value="jpg_moved")
        tk.Entry(dst_row, textvariable=self.jpg_dst,
                 font=("Courier New", 10), bg=BG_PANEL, fg=TEXT_WHITE,
                 insertbackground=ACCENT_BLUE, relief="flat", bd=4, width=42).pack(side="left", padx=(0,6))
        tk.Button(dst_row, text="Browse", font=("Courier New", 9),
                  bg=BTN_BG, fg=ACCENT_BLUE, relief="flat", padx=8,
                  cursor="hand2",
                  command=lambda: self.jpg_dst.set(
                      filedialog.askdirectory(title="Select Destination Folder") or self.jpg_dst.get()
                  )).pack(side="left")

        tk.Button(f, text="▶  MOVE JPG FILES",
                  font=("Courier New", 11, "bold"),
                  bg=ACCENT_BLUE, fg=BG_DARK,
                  relief="flat", pady=8, padx=20,
                  cursor="hand2",
                  command=self._run_jpg).pack(pady=(14, 14))
        return f

    def _run_jpg(self):
        src = self.jpg_src.get().strip()
        dst = self.jpg_dst.get().strip()
        if not src:
            messagebox.showerror("Missing", "Please select a source folder.")
            return

        self._log("── Move JPG Files ──────────────────", "head")

        if not os.path.isdir(src):
            self._log(f"✗ Source folder not found: {src}", "err")
            return

        os.makedirs(dst, exist_ok=True)
        files = [f for f in os.listdir(src) if f.lower().endswith((".jpg", ".jpeg"))]

        if not files:
            self._log("⚠ No .jpg/.jpeg files found in source folder.", "info")
            return

        moved = 0
        for fn in files:
            shutil.move(os.path.join(src, fn), os.path.join(dst, fn))
            self._log(f"  ✔ Moved: {fn}", "ok")
            moved += 1

        self._log(f"✔ Done! {moved} file(s) moved → '{dst}'", "ok")

    # ══════════════════════════════════════════════════════
    #  TAB 2 — Extract Emails
    # ══════════════════════════════════════════════════════
    def _build_email_tab(self, parent) -> tk.Frame:
        f = tk.Frame(parent, bg=BG_CARD)

        tk.Label(f, text="Extract all email addresses from a .txt file and save to output.",
                 font=("Courier New", 10), fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w", padx=16, pady=(14, 10))

        # Input file
        in_row = tk.Frame(f, bg=BG_CARD)
        in_row.pack(fill="x", padx=16, pady=4)
        tk.Label(in_row, text="Input .txt File :", font=("Courier New", 10),
                 fg=TEXT_WHITE, bg=BG_CARD, width=18, anchor="w").pack(side="left")
        self.email_in = tk.StringVar()
        tk.Entry(in_row, textvariable=self.email_in,
                 font=("Courier New", 10), bg=BG_PANEL, fg=TEXT_WHITE,
                 insertbackground=ACCENT_BLUE, relief="flat", bd=4, width=42).pack(side="left", padx=(0,6))
        tk.Button(in_row, text="Browse", font=("Courier New", 9),
                  bg=BTN_BG, fg=ACCENT_BLUE, relief="flat", padx=8,
                  cursor="hand2",
                  command=lambda: self.email_in.set(
                      filedialog.askopenfilename(
                          title="Select .txt File",
                          filetypes=[("Text Files", "*.txt"), ("All", "*.*")]
                      ) or self.email_in.get()
                  )).pack(side="left")

        # Output file
        out_row = tk.Frame(f, bg=BG_CARD)
        out_row.pack(fill="x", padx=16, pady=4)
        tk.Label(out_row, text="Output File :", font=("Courier New", 10),
                 fg=TEXT_WHITE, bg=BG_CARD, width=18, anchor="w").pack(side="left")
        self.email_out = tk.StringVar(value="extracted_emails.txt")
        tk.Entry(out_row, textvariable=self.email_out,
                 font=("Courier New", 10), bg=BG_PANEL, fg=TEXT_WHITE,
                 insertbackground=ACCENT_BLUE, relief="flat", bd=4, width=42).pack(side="left", padx=(0,6))
        tk.Button(out_row, text="Browse", font=("Courier New", 9),
                  bg=BTN_BG, fg=ACCENT_BLUE, relief="flat", padx=8,
                  cursor="hand2",
                  command=lambda: self.email_out.set(
                      filedialog.asksaveasfilename(
                          title="Save Output As",
                          defaultextension=".txt",
                          filetypes=[("Text Files", "*.txt")]
                      ) or self.email_out.get()
                  )).pack(side="left")

        tk.Button(f, text="▶  EXTRACT EMAILS",
                  font=("Courier New", 11, "bold"),
                  bg=ACCENT_PURP, fg=BG_DARK,
                  relief="flat", pady=8, padx=20,
                  cursor="hand2",
                  command=self._run_email).pack(pady=(14, 14))
        return f

    def _run_email(self):
        inp = self.email_in.get().strip()
        out = self.email_out.get().strip()
        self._log("── Extract Emails ──────────────────", "head")

        if not inp or not os.path.isfile(inp):
            self._log("✗ Input file not found. Please select a valid .txt file.", "err")
            return

        pattern = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
        with open(inp, "r", encoding="utf-8") as f:
            content = f.read()

        emails = sorted(set(pattern.findall(content)))

        if not emails:
            self._log("⚠ No email addresses found in the file.", "info")
            return

        with open(out, "w", encoding="utf-8") as f:
            f.write(f"Extracted Emails — Total: {len(emails)}\n")
            f.write("=" * 40 + "\n")
            for e in emails:
                f.write(e + "\n")

        self._log(f"✔ Found {len(emails)} unique email(s):", "ok")
        for e in emails[:8]:
            self._log(f"   • {e}", "ok")
        if len(emails) > 8:
            self._log(f"   ... and {len(emails)-8} more.", "info")
        self._log(f"✔ Saved to '{out}'", "ok")

    # ══════════════════════════════════════════════════════
    #  TAB 3 — Scrape Webpage Title
    # ══════════════════════════════════════════════════════
    def _build_scrape_tab(self, parent) -> tk.Frame:
        f = tk.Frame(parent, bg=BG_CARD)

        tk.Label(f, text="Fetch any webpage URL and extract its <title> tag, then save.",
                 font=("Courier New", 10), fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w", padx=16, pady=(14, 10))

        url_row = tk.Frame(f, bg=BG_CARD)
        url_row.pack(fill="x", padx=16, pady=4)
        tk.Label(url_row, text="Webpage URL :", font=("Courier New", 10),
                 fg=TEXT_WHITE, bg=BG_CARD, width=18, anchor="w").pack(side="left")
        self.scrape_url = tk.StringVar(value="https://www.python.org")
        tk.Entry(url_row, textvariable=self.scrape_url,
                 font=("Courier New", 10), bg=BG_PANEL, fg=TEXT_WHITE,
                 insertbackground=ACCENT_BLUE, relief="flat", bd=4, width=50).pack(side="left")

        out_row = tk.Frame(f, bg=BG_CARD)
        out_row.pack(fill="x", padx=16, pady=4)
        tk.Label(out_row, text="Output File :", font=("Courier New", 10),
                 fg=TEXT_WHITE, bg=BG_CARD, width=18, anchor="w").pack(side="left")
        self.scrape_out = tk.StringVar(value="webpage_title.txt")
        tk.Entry(out_row, textvariable=self.scrape_out,
                 font=("Courier New", 10), bg=BG_PANEL, fg=TEXT_WHITE,
                 insertbackground=ACCENT_BLUE, relief="flat", bd=4, width=42).pack(side="left", padx=(0,6))
        tk.Button(out_row, text="Browse", font=("Courier New", 9),
                  bg=BTN_BG, fg=ACCENT_BLUE, relief="flat", padx=8,
                  cursor="hand2",
                  command=lambda: self.scrape_out.set(
                      filedialog.asksaveasfilename(
                          title="Save Output As",
                          defaultextension=".txt",
                          filetypes=[("Text Files", "*.txt")]
                      ) or self.scrape_out.get()
                  )).pack(side="left")

        # Result label
        self.title_result = tk.Label(f, text="",
                                     font=("Courier New", 11, "bold"),
                                     fg=ACCENT_GOLD, bg=BG_CARD,
                                     wraplength=820, justify="left")
        self.title_result.pack(anchor="w", padx=16, pady=(8, 0))

        tk.Button(f, text="▶  SCRAPE TITLE",
                  font=("Courier New", 11, "bold"),
                  bg=ACCENT_GOLD, fg=BG_DARK,
                  relief="flat", pady=8, padx=20,
                  cursor="hand2",
                  command=self._run_scrape).pack(pady=(10, 14))
        return f

    def _run_scrape(self):
        self._log("── Scrape Webpage Title ────────────", "head")
        try:
            import requests
        except ImportError:
            self._log("✗ 'requests' not installed. Run: pip install requests", "err")
            return

        url = self.scrape_url.get().strip()
        out = self.scrape_out.get().strip()
        if not url:
            self._log("✗ Please enter a URL.", "err")
            return

        self._log(f"  Fetching: {url}", "info")
        self.title_result.config(text="Fetching...")

        def fetch():
            try:
                r = requests.get(url, timeout=10)
                r.raise_for_status()
                match = re.search(r"<title[^>]*>(.*?)</title>",
                                  r.text, re.IGNORECASE | re.DOTALL)
                if not match:
                    self.root.after(0, lambda: self._log("⚠ No <title> tag found.", "info"))
                    self.root.after(0, lambda: self.title_result.config(text="No title found."))
                    return

                title = match.group(1).strip()
                title = title.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")

                with open(out, "w", encoding="utf-8") as f:
                    f.write(f"URL   : {url}\n")
                    f.write(f"Title : {title}\n")
                    f.write(f"Saved : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

                self.root.after(0, lambda: self._log(f"✔ Title: {title}", "ok"))
                self.root.after(0, lambda: self._log(f"✔ Saved to '{out}'", "ok"))
                self.root.after(0, lambda: self.title_result.config(text=f"Title: {title}"))

            except Exception as e:
                self.root.after(0, lambda: self._log(f"✗ Error: {e}", "err"))
                self.root.after(0, lambda: self.title_result.config(text="Error fetching page."))

        threading.Thread(target=fetch, daemon=True).start()

    # ── Log helper ────────────────────────────────────────
    def _log(self, msg: str, tag: str = "ok"):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n", tag)
        self.log_text.see("end")
        self.log_text.config(state="disabled")


# ════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app  = AutomationApp(root)
    root.mainloop()
