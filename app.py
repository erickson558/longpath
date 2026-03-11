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


def sample_long_paths(base_dir: Path, total: int) -> tuple[list[str], int, int]:
    """Create recursive long-path folders/files under project dir."""
    output_dir = base_dir / "generated_long_paths"
    output_dir.mkdir(parents=True, exist_ok=True)

    paths: list[str] = []
    directories_created = 0
    failures = 0
    max_depth = 6
    branch_factor = 3

    def ensure_directory(target: Path) -> bool:
        nonlocal directories_created, failures
        try:
            if not target.exists():
                target.mkdir(parents=True, exist_ok=True)
                directories_created += 1
            return True
        except OSError:
            failures += 1
            return False

    def write_file(target: Path, idx: int, level: int) -> bool:
        nonlocal failures
        try:
            target.write_text(
                f"generated file index={idx} depth={level} for long path test\n",
                encoding="utf-8",
            )
            paths.append(str(target.relative_to(base_dir)).replace("\\", "/"))
            return True
        except OSError:
            failures += 1
            return False

    def build_tree(current_dir: Path, level: int, index_start: int, remaining: int) -> tuple[int, int]:
        if remaining <= 0:
            return index_start, 0

        created_here = 0
        for branch in range(branch_factor):
            if created_here >= remaining:
                break

            folder_name = (
                "lvl-{:02d}-node-{:02d}-long-folder-name-for-recursive-path-"
                "stress-validation-and-ticket-reproduction"
            ).format(level, branch)
            branch_dir = current_dir / folder_name
            if not ensure_directory(branch_dir):
                continue

            file_target = branch_dir / (
                "very-long-file-name-to-validate-line-break-behavior-without-"
                "horizontal-scroll-regression-{:06d}.txt".format(index_start)
            )
            if write_file(file_target, index_start, level):
                created_here += 1
            index_start += 1

            can_go_deeper = level < max_depth and created_here < remaining
            if can_go_deeper:
                index_start, nested_created = build_tree(
                    branch_dir,
                    level + 1,
                    index_start,
                    remaining - created_here,
                )
                created_here += nested_created

        return index_start, created_here

    next_index, _ = build_tree(output_dir, 1, 0, total)

    # Fallback in case recursion stops early because of filesystem limits.
    fallback_dir = output_dir / "fallback-path-segment-with-long-name"
    while len(paths) < total:
        idx = next_index
        next_index += 1
        fallback = fallback_dir / (
            "fallback-file-name-for-longpath-validation-{:06d}.txt".format(idx)
        )
        if not ensure_directory(fallback.parent):
            break
        if not write_file(fallback, idx, 0):
            break

    # Include extra-long examples similar to the reported issue.
    extra_relative = Path(
        "coreclr/nugen/ILCompiler.Reflection.ReadyToRun.Experimental/"
        "ILCompiler.Reflection.ReadyToRun.Experimental.Very.Long.File.Name."
        "That.Should.Wrap.Correctly.And.Not.Create.Horizontal.Scroll.txt"
    )
    extra_absolute = output_dir / extra_relative
    try:
        if ensure_directory(extra_absolute.parent):
            extra_absolute.write_text("extra long path sample\n", encoding="utf-8")
            paths.append(str(extra_absolute.relative_to(base_dir)).replace("\\", "/"))
    except OSError:
        failures += 1

    return paths, directories_created, failures


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

        base_dir = Path(__file__).resolve().parent
        paths, directories_created, failures = sample_long_paths(base_dir, total)

        ttk.Label(
            wrapper,
            text=(
                f"Generados: {len(paths)} archivos | {directories_created} carpetas "
                f"dentro de {base_dir.name}/generated_long_paths"
            )
            + ("" if failures == 0 else f" | Fallidos: {failures}"),
            wraplength=680,
        ).pack(anchor=tk.W, pady=(6, 6))

        text.insert(tk.END, "\n".join(paths) + "\n")

        text.configure(state=tk.DISABLED)

        ttk.Button(wrapper, text="Close", command=dialog.destroy).pack(anchor=tk.E, pady=(10, 0))


if __name__ == "__main__":
    LongPathApp().mainloop()
