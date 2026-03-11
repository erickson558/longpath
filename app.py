from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


def read_version() -> str:
    """Read version from VERSION file and use a safe default if missing."""
    version_file = Path(__file__).with_name("VERSION")
    if not version_file.exists():
        return "V0.0.0"
    return version_file.read_text(encoding="utf-8").strip() or "V0.0.0"


def sample_long_paths() -> list[str]:
    """Return sample deep file paths to validate line wrapping in the popup."""
    base = "docs/design/coreclr/botr/images"
    return [
        f"{base}/profiling-gc.png",
        f"{base}/profiling-overview.png",
        f"{base}/simple-dependency-graph.gv",
        f"{base}/simple-dependency-graph.svg",
        f"{base}/stack.png",
        f"{base}/type-system-dependencies.png",
        "src/coreclr/nugen/ILCompiler.Reflection.ReadyToRun.Experimental/"
        "ILCompiler.Reflection.ReadyToRun.Experimental.Very.Long.File.Name."
        "That.Should.Wrap.Correctly.And.Not.Create.Horizontal.Scroll.png",
    ]


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

        ttk.Label(
            root,
            text=f"Version actual: {self.version}",
        ).pack(anchor=tk.W, pady=(20, 0))

    def open_import_popup(self) -> None:
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

        for path in sample_long_paths():
            text.insert(tk.END, path + "\n")

        text.configure(state=tk.DISABLED)

        ttk.Button(wrapper, text="Close", command=dialog.destroy).pack(anchor=tk.E, pady=(10, 0))


if __name__ == "__main__":
    LongPathApp().mainloop()
