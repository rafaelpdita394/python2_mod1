
"""
Módulo de geração e impressão de labirintos.

Contém funções para criar um labirinto aleatório, imprimir em terminal com Rich
e resolver o labirinto de forma recursiva (busca em profundidade).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Set
import random

try:
    # impressão bonita (opcional em testes)
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text
    console = Console()
except Exception:  # pragma: no cover
    console = None  # fallback silencioso

Cell = Tuple[int, int]

@dataclass
class Labirinto:
    """Representa um labirinto retangular com paredes e espaços vazios.

    A grade usa:
      - '#': parede
      - ' ': espaço livre
      - 'E': entrada
      - 'S': saída
      - '*': item colecionável

    Attributes:
        largura: número de colunas.
        altura: número de linhas.
        grade: lista de listas de caracteres.
        entrada: coordenada (linha, coluna) da entrada.
        saida: coordenada (linha, coluna) da saída.
        itens: conjunto de coordenadas com itens.
    """
    largura: int
    altura: int
    grade: List[List[str]]
    entrada: Cell
    saida: Cell
    itens: Set[Cell]

def _vizinhos(c: Cell, largura: int, altura: int, passo: int = 2) -> List[Cell]:
    """Retorna vizinhos candidatos para o algoritmo de labirinto (saltando em `passo`)."""
    r, q = c
    cand = [(r-2, q), (r+2, q), (r, q-2), (r, q+2)]
    return [(i, j) for i, j in cand if 0 < i < altura-1 and 0 < j < largura-1]

def criar_labirinto(largura: int, altura: int, sementes: Optional[int] = None, itens: int = 3) -> Labirinto:
    """Gera um labirinto aleatório usando DFS recursivo para cavar túneis.

    Args:
        largura: número de colunas (min 7, ímpar recomendado).
        altura: número de linhas (min 7, ímpar recomendado).
        sementes: semente do gerador de aleatoriedade para reprodutibilidade.
        itens: quantidade de itens colecionáveis a espalhar no labirinto.
    """
    if sementes is not None:
        random.seed(sementes)
    largura = max(largura, 7)
    altura = max(altura, 7)
    if largura % 2 == 0: largura += 1
    if altura % 2 == 0: altura += 1

    grade = [['#' for _ in range(largura)] for _ in range(altura)]

    # Algoritmo: DFS recursivo cavando de 2 em 2 células
    def cavar(c: Cell):
        r, q = c
        grade[r][q] = ' '
        viz = _vizinhos(c, largura, altura)
        random.shuffle(viz)
        for nr, nq in viz:
            if grade[nr][nq] == '#':
                # remove parede intermediária
                mr, mq = (r + nr)//2, (q + nq)//2
                grade[mr][mq] = ' '
                cavar((nr, nq))

    # Início do carving
    start = (1, 1)
    cavar(start)

    # Define entrada e saída em bordas opostas
    entrada = (1, 1)
    saida = (altura-2, largura-2)
    grade[entrada[0]][entrada[1]] = 'E'
    grade[saida[0]][saida[1]] = 'S'

    # Espalhar itens em células vazias
    livres = [(i, j) for i in range(1, altura-1) for j in range(1, largura-1) if grade[i][j] == ' ']
    random.shuffle(livres)
    itens_pos = set()
    for k in range(min(itens, len(livres))):
        i, j = livres[k]
        grade[i][j] = '*'
        itens_pos.add((i, j))

    return Labirinto(largura, altura, grade, entrada, saida, itens_pos)

def imprimir_labirinto(lab: Labirinto, jogador: Optional[Cell] = None, cor: str = "green") -> None:
    """Imprime o labirinto no terminal. Se `jogador` for informado, marca a posição com '@'."""
    if console is None:
        # fallback: print simples
        for i in range(lab.altura):
            linha = "".join(lab.grade[i])
            if jogador and i == jogador[0]:
                j = jogador[1]
                linha = linha[:j] + '@' + linha[j+1:]
            print(linha)
        return

    table = Table(show_header=False, show_lines=False, pad_edge=False, expand=False)
    for i in range(lab.altura):
        linha = ""
        for j in range(lab.largura):
            ch = lab.grade[i][j]
            if jogador and (i, j) == jogador:
                linha += f"[bold {cor}]@[/]"
            elif ch == '#':
                linha += "[grey74]#[/]"
            elif ch == '*':
                linha += "[yellow]*[/]"
            elif ch == 'E':
                linha += "[cyan]E[/]"
            elif ch == 'S':
                linha += "[magenta]S[/]"
            else:
                linha += " "
        table.add_row(linha)
    console.print(table)

def resolver_recursivo(lab: Labirinto, origem: Optional[Cell] = None, destino: Optional[Cell] = None) -> Optional[List[Cell]]:
    """Resolve o labirinto via DFS recursivo e retorna uma lista de passos (células).

    A busca considera movimentos em 4 direções. Retorna a sequência de células
    desde a origem até o destino (inclusivos), ou None se não houver caminho.
    """
    if origem is None:
        origem = lab.entrada
    if destino is None:
        destino = lab.saida

    visitado: Set[Cell] = set()
    caminho: List[Cell] = []

    def dfs(c: Cell) -> bool:
        if c in visitado:
            return False
        visitado.add(c)
        caminho.append(c)
        if c == destino:
            return True
        r, q = c
        for nr, nq in [(r-1,q), (r+1,q), (r,q-1), (r,q+1)]:
            if 0 <= nr < lab.altura and 0 <= nq < lab.largura:
                ch = lab.grade[nr][nq]
                if ch in (' ', 'S', '*'):
                    if dfs((nr, nq)):
                        return True
        caminho.pop()
        return False

    # trata 'E' como espaço
    er, eq = origem
    if lab.grade[er][eq] == 'E':
        lab.grade[er][eq] = ' '

    achou = dfs(origem)
    # restaura 'E'
    lab.grade[er][eq] = 'E'
    return caminho if achou else None
