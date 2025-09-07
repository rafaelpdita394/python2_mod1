
"""
Funções utilitárias para I/O, menus, efeitos e animações.
"""
from __future__ import annotations
from typing import Optional, List
import time
import sys
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.prompt import Prompt
    from rich.table import Table
    console = Console()
except Exception:  # pragma: no cover
    console = None

def imprime_instrucoes(path: str) -> None:
    """Lê um arquivo de instruções e imprime formatado com Rich (se disponível)."""
    p = Path(path)
    conteudo = p.read_text(encoding="utf-8") if p.exists() else "# Instruções\nSem conteúdo."
    if console:
        console.print(Panel(Markdown(conteudo), title="Instruções", border_style="blue"))
    else:
        print(conteudo)

def mostrar_menu(nome: str) -> str:
    """Mostra menu inicial e retorna a opção escolhida usando match-case."""
    if console:
        table = Table(title=f"Aventura no Labirinto — Bem-vindo(a), {nome}!")
        table.add_column("Opção", justify="center")
        table.add_column("Descrição")
        table.add_row("1", "Jogar")
        table.add_row("2", "Assistir solução recursiva")
        table.add_row("3", "Instruções")
        table.add_row("4", "Sair")
        console.print(table)
        escolha = Prompt.ask("Escolha", choices=["1","2","3","4"], default="1")
    else:
        print(f"Bem-vindo(a), {nome}!")
        print("1) Jogar\n2) Assistir solução\n3) Instruções\n4) Sair")
        escolha = input("Escolha: ").strip()

    match escolha:
        case "1":
            return "jogar"
        case "2":
            return "assistir"
        case "3":
            return "instrucoes"
        case "4":
            return "sair"
        case _:
            return "sair"

def animacao_vitoria_recursiva(n: int) -> None:
    """Animação recursiva simples para celebrar a vitória."""
    if n <= 0:
        return
    if console:
        console.print("[bold green]★[/] " * n)
    else:
        print("★ " * n)
    time.sleep(0.05)
    animacao_vitoria_recursiva(n-1)

def tocar_musica(caminho: Optional[str]) -> None:
    """Toca música com playsound, se disponível e caminho válido."""
    if not caminho:
        return
    try:
        from playsound import playsound
        playsound(caminho, block=False)
    except Exception:
        pass
