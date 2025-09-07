"""
Módulo painel do pacote personalizador.
Funções para exibir painéis estilizados.
"""

from rich.console import Console
from rich.panel import Panel

console = Console()

def painel_simples(texto: str, isArquivo: bool = False):
    """Exibe o texto dentro de um painel simples."""
    if isArquivo:
        with open(texto, 'r') as f:
            texto = f.read()
    console.print(Panel(texto))

def painel_colorido(texto: str, isArquivo: bool = False):
    """Exibe o texto dentro de um painel com cores e estilo."""
    if isArquivo:
        with open(texto, 'r') as f:
            texto = f.read()
    console.print(Panel(f"[bold cyan]{texto}[/bold cyan]", title="[red]Título[/red]"))
