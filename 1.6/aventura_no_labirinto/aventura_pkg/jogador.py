
"""
Módulo de controle do jogador e pontuação.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Optional, Callable, Set

try:
    from pynput import keyboard
except Exception:  # pragma: no cover
    keyboard = None  # permite testes sem a dependência instalada

try:
    from rich.console import Console
    console = Console()
except Exception:  # pragma: no cover
    console = None

Cell = Tuple[int, int]

@dataclass
class Jogador:
    """Estado do jogador: posição e pontuação."""
    pos: Cell
    pontos: int = 0
    itens_coletados: int = 0
    movimentos: int = 0

def iniciar_jogador(entrada: Cell) -> Jogador:
    """Cria o jogador na posição de entrada do labirinto."""
    return Jogador(pos=entrada, pontos=0, itens_coletados=0, movimentos=0)

def pontuar(j: Jogador, evento: str) -> None:
    """Atualiza pontuação de acordo com o evento."""
    match evento:
        case "andar":
            j.pontos += 1
            j.movimentos += 1
        case "coletar":
            j.pontos += 10
            j.itens_coletados += 1
        case "bater_parede":
            j.pontos -= 1
            j.movimentos += 1
        case "chegar_saida":
            j.pontos += 50
        case _:
            pass

def mover(lab, jogador: Jogador, on_tick: Optional[Callable[[], None]] = None) -> Optional[str]:
    """
    Lê o teclado e move o jogador no labirinto.
    Retorna "sair" se o usuário pressionar ESC. Usa pynput, com fallback WASD por input().
    """
    if keyboard is None:
        # Fallback simples para ambientes sem pynput
        if console:
            console.print("[dim]Controles: W/A/S/D ou Q para sair[/]")
        else:
            print("Controles: W/A/S/D ou Q para sair")
        escolha = input("-> ").strip().lower()
        mapping = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1), 'q': None}
        delta = mapping.get(escolha)
        if delta is None:
            return "sair"
        if delta:
            _tentar_mover(lab, jogador, delta)
        if on_tick: on_tick()
        return None

    # Com pynput: listener por uma tecla
    pressed = {"done": False, "cmd": None}
    def on_press(key):
        try:
            k = key.char.lower()
        except AttributeError:
            k = str(key)
        mapping = {
            'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1),
            'Key.up': (-1, 0), 'Key.down': (1, 0), 'Key.left': (0, -1), 'Key.right': (0, 1),
            'q': None, 'Key.esc': None
        }
        if k in mapping:
            delta = mapping[k]
            if delta is None:
                pressed["done"] = True
                pressed["cmd"] = "sair"
                return False
            _tentar_mover(lab, jogador, delta)
            pressed["done"] = True
            return False

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    if on_tick: on_tick()
    return pressed["cmd"]

def _tentar_mover(lab, jogador: Jogador, delta: Tuple[int,int]) -> None:
    """Aplica o deslocamento se a célula alvo for válida."""
    r, c = jogador.pos
    dr, dc = delta
    nr, nc = r + dr, c + dc
    if not (0 <= nr < lab.altura and 0 <= nc < lab.largura):
        pontuar(jogador, "bater_parede")
        return
    alvo = lab.grade[nr][nc]
    if alvo == '#':
        pontuar(jogador, "bater_parede")
        return
    # mover
    jogador.pos = (nr, nc)
    pontuar(jogador, "andar")
    if alvo == '*':
        pontuar(jogador, "coletar")
        lab.grade[nr][nc] = ' '
    if alvo == 'S':
        pontuar(jogador, "chegar_saida")
