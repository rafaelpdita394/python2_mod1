"""
Módulo layout do pacote personalizador.
Fornece funções que exibem texto usando layouts do Rich.
"""

from rich.console import Console
from rich.layout import Layout

console = Console()

def exibir_layout(texto: str, isArquivo: bool = False):
    """
    Exibe o texto em um layout simples dividido em painéis.
    
    Args:
        texto (str): Texto ou caminho de arquivo.
        isArquivo (bool): True se texto for caminho de arquivo.
    """
    if isArquivo:
        with open(texto, 'r') as f:
            texto = f.read()
    layout = Layout()
    layout.split_column(
        Layout(texto, name="principal"),
        Layout("Footer", name="rodape")
    )
    console.print(layout)

def layout_colorido(texto: str, isArquivo: bool = False):
    """
    Exibe o texto em layout colorido.
    
    Args:
        texto (str): Texto ou caminho de arquivo.
        isArquivo (bool): True se texto for caminho de arquivo.
    """
    if isArquivo:
        with open(texto, 'r') as f:
            texto = f.read()
    layout = Layout()
    layout.split_row(
        Layout(f"[bold red]{texto}[/bold red]", name="esquerda"),
        Layout(f"[green]Painel direito[/green]", name="direita")
    )
    console.print(layout)
