"""
Matplotlib backend selection and figure display helpers.
"""

import os
import platform
import subprocess
from pathlib import Path

import matplotlib


def configure_matplotlib_backend(prefer_interactive: bool = True) -> None:
    """
    Select an appropriate matplotlib backend for the current environment.

    Args:
        prefer_interactive: When True, try TkAgg/Qt backends before falling back to Agg.
    """
    if os.environ.get("MPLBACKEND"):
        return

    if not prefer_interactive:
        matplotlib.use("Agg", force=True)
        return

    interactive_backends = ["TkAgg", "Qt5Agg", "QtAgg"]
    backend_set = False

    if os.name == "nt":
        for backend in ["TkAgg", "Qt5Agg"]:
            try:
                matplotlib.use(backend, force=True)
                backend_set = True
                break
            except (ImportError, ValueError):
                continue
    elif "DISPLAY" in os.environ:
        for backend in interactive_backends:
            try:
                matplotlib.use(backend, force=True)
                backend_set = True
                break
            except (ImportError, ValueError):
                continue

    if not backend_set:
        matplotlib.use("Agg", force=True)


def show_or_open_figure(output_file: Path) -> None:
    """Display a figure interactively, or just report the saved path in notebooks/Colab."""
    import matplotlib.pyplot as plt

    in_colab = Path("/content").exists() or "COLAB_RELEASE_TAG" in os.environ
    in_notebook = False
    try:
        from IPython import get_ipython

        in_notebook = get_ipython() is not None
    except (ImportError, NameError):
        in_notebook = False

    current_backend = matplotlib.get_backend().lower()
    print(f"Matplotlib backend: {matplotlib.get_backend()}")

    in_streamlit = bool(os.environ.get("STREAMLIT_SERVER_PORT") or os.environ.get("STREAMLIT_RUNTIME"))

    if in_colab or in_notebook or in_streamlit:
        print(f"Figure saved to: {output_file}")
        print("In Colab: run the display cell below, or open this file in the left Files sidebar.")
        return

    if current_backend != "agg":
        print("Displaying figure...")
        try:
            plt.show(block=True)
            return
        except OSError as exc:
            print(f"Could not display graph interactively: {exc}")

    print(f"Non-interactive backend detected. Graph saved to: {output_file}")
    try:
        if platform.system() == "Windows":
            os.startfile(str(output_file))
        elif platform.system() == "Darwin":
            subprocess.run(["open", str(output_file)], check=False)
        else:
            subprocess.run(["xdg-open", str(output_file)], check=False)
    except OSError as exc:
        print(f"Could not open image file automatically: {exc}")
