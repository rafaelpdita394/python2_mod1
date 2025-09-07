"""
Módulo progresso do pacote personalizador.
Funções que mostram barras de progresso.
"""

from rich.console import Console
from rich.progress import track
import time

console = Console()

def progresso_simples(texto: str, isArquivo: bool = False):
    """Mostra uma barra de progresso enquanto imprime o texto."""
    if isArquivo:
        with open(texto, 'r') as f:
            texto = f.read()
    for _ in track(range(10), description=texto):
        time.sleep(0.1)

def progresso_colorido(texto: str, isArquivo: bool = False):
    """Mostra barra de progresso colorida."""
    if isArquivo:
        with open(texto, 'r') as f:
            texto = f.read()
    for _ in track(range(10), description=f"[cyan]{texto}[/cyan]"):
        time.sleep(0.1)
