"""
Módulo estilo do pacote personalizador.
Funções que aplicam estilos ao texto.
"""

from rich.console import Console
from rich.text import Text

console = Console()

def texto_bold(texto: str, isArquivo: bool = False):
    """Exibe o texto em negrito."""
    if isArquivo:
        with open(texto, 'r') as f:
            texto = f.read()
    console.print(Text(texto, style="bold"))

def texto_italic_color(texto: str, isArquivo: bool = False):
    """Exibe o texto em itálico e cor."""
    if isArquivo:
        with open(texto, 'r') as f:
            texto = f.read()
    console.print(Text(texto, style="italic magenta"))
