from rich.console import Console

console = Console()

STYLES = {
    "default": "bold cyan",
    "error": "bold red",
    "success": "bold green",
    "warning": "bold yellow",
    "background": "on blue"   
}
def print_command(message, style="default"):
    """Helper function to print messages with predefined styles."""
    console.print(message, style=STYLES.get(style, STYLES["default"]))
    
