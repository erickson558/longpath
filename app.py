from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


def read_version() -> str:
    """Read version from VERSION file and use a safe default if missing."""
    version_file = Path(__file__).with_name("VERSION")
    if not version_file.exists():
        return "V0.0.0"
    return version_file.read_text(encoding="utf-8").strip() or "V0.0.0"


def sample_long_paths(total: int) -> list[str]:
    """Build many deep and long file paths to stress line wrapping behavior."""
    paths: list[str] = []
    for i in range(total):
        paths.append(
            "src/coreclr/runtime/subdir-{:03d}/component-{:03d}/feature-{:03d}/"
            "very-long-file-name-for-line-break-validation-{:05d}.png".format(
                i % 97,
                i % 53,
                i % 29,
                i,
            )
        )

    # Include extra-long examples similar to the reported issue.
    paths.extend(
        [
            "src/coreclr/nugen/ILCompiler.Reflection.ReadyToRun.Experimental/"
            "ILCompiler.Reflection.ReadyToRun.Experimental.Very.Long.File.Name."
            "That.Should.Wrap.Correctly.And.Not.Create.Horizontal.Scroll.png",
            "https://github.com/dotnet/runtime/aekoniginger-patch-1/subdir/another/"
            "subdir/yet/another/deep/path/that/keeps/growing/for/layout-validation/"
            "and-should-wrap-without-any-sideways-scroll-behavior.txt",
        ]
    )
    return paths


class LongPathApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.version = read_version()
        self.title(f"LongPath Popup Tester {self.version}")
        self.geometry("740x420")
        self.minsize(620, 360)

        root = ttk.Frame(self, padding=20)
        root.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            root,
            text="No line breaks for very long filepaths - Test App",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor=tk.W)

        ttk.Label(
            root,
            text=(
                "Abre el popup y valida que los paths largos hagan line break "
                "sin scroll horizontal."
            ),
            wraplength=680,
        ).pack(anchor=tk.W, pady=(8, 18))

        ttk.Button(
            root,
            text="Abrir popup de import",
            command=self.open_import_popup,
        ).pack(anchor=tk.W)

        self.path_count = tk.StringVar(value="39090")
        count_row = ttk.Frame(root)
        count_row.pack(anchor=tk.W, pady=(14, 0))
        ttk.Label(count_row, text="Cantidad de paths a generar:").pack(side=tk.LEFT)
        ttk.Entry(count_row, width=10, textvariable=self.path_count).pack(side=tk.LEFT, padx=(8, 0))

        ttk.Label(
            root,
            text=f"Version actual: {self.version}",
        ).pack(anchor=tk.W, pady=(20, 0))

    def open_import_popup(self) -> None:
        try:
            total = int(self.path_count.get().strip())
            if total <= 0:
                raise ValueError
            if total > 120000:
                messagebox.showwarning(
                    "Valor alto",
                    "Se recomienda usar <= 120000 para evitar lentitud extrema.",
                )
        except ValueError:
            messagebox.showerror("Valor invalido", "Ingresa un numero entero mayor a cero.")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Ready to Import")
        dialog.geometry("720x420")
        dialog.transient(self)
        dialog.grab_set()

        wrapper = ttk.Frame(dialog, padding=12)
        wrapper.pack(fill=tk.BOTH, expand=True)

        title = (
            "https://github.com/dotnet/runtime "
            "aekoniginger-patch-1/subdir/another/subdir/yet/another/deep/path"
        )
        ttk.Label(wrapper, text=title, wraplength=680).pack(anchor=tk.W, pady=(0, 8))

        text = ScrolledText(
            wrapper,
            wrap=tk.WORD,
            height=16,
            font=("Consolas", 10),
            state=tk.NORMAL,
        )
        text.pack(fill=tk.BOTH, expand=True)

        paths = sample_long_paths(total)
        text.insert(tk.END, "\n".join(paths) + "\n")

        text.configure(state=tk.DISABLED)

        ttk.Button(wrapper, text="Close", command=dialog.destroy).pack(anchor=tk.E, pady=(10, 0))


if __name__ == "__main__":
    LongPathApp().mainloop()
