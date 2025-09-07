
"""
Ponto de entrada do jogo "Aventura no Labirinto".
Implementa uma CLI com argparse.
"""
from __future__ import annotations
import argparse
import time
from pathlib import Path

from aventura_pkg.labirinto import criar_labirinto, imprimir_labirinto, resolver_recursivo
from aventura_pkg.jogador import iniciar_jogador, mover
from aventura_pkg import utils

try:
    from rich.console import Console
    console = Console()
except Exception:  # pragma: no cover
    console = None

def parse_args():
    parser = argparse.ArgumentParser(
        prog="aventura",
        description="Aventura no Labirinto — explore, colete e escape!",
        epilog="Exemplo: python main.py --name Valter --color cyan --dificuldade medio"
    )
    parser.add_argument("--name", required=True, help="Nome do(a) jogador(a). [Obrigatório]")
    parser.add_argument("--color", default="green", help="Cor principal do jogador (Rich).")
    parser.add_argument("--dificuldade", choices=["facil", "medio", "dificil"], default="medio",
                        help="Define o tamanho do labirinto.")
    parser.add_argument("--disable-sound", action="store_true", help="Desliga a música/sons do jogo.")
    parser.add_argument("--auto-solve", action="store_true", help="Assiste a solução recursiva automaticamente.")
    parser.add_argument("--instrucoes", action="store_true", help="Mostra instruções e sai.")
    return parser.parse_args()

def tamanho_por_dificuldade(nivel: str) -> tuple[int,int]:
    match nivel:
        case "facil":
            return (17, 11)
        case "dificil":
            return (41, 23)
        case _:
            return (31, 17)

def main():
    args = parse_args()
    nome = args.name

    if args.instrucoes:
        utils.imprime_instrucoes("README.md")
        return

    # Música (opcional)
    if not args.disable_sound:
        trilha = "trilha.mp3"
        if Path(trilha).exists():
            utils.tocar_musica(trilha)

    # Loop de menu
    while True:
        acao = utils.mostrar_menu(nome)
        if acao == "sair":
            break

        largura, altura = tamanho_por_dificuldade(args.dificuldade)
        lab = criar_labirinto(largura, altura, itens=5)

        if acao == "assistir" or args.auto_solve:
            caminho = resolver_recursivo(lab)
            if caminho is None:
                if console: console.print("[red]Sem solução encontrada![/]")
                else: print("Sem solução encontrada!")
                continue
            j = iniciar_jogador(lab.entrada)
            for cel in caminho:
                j.pos = cel
                imprimir_labirinto(lab, j.pos, cor=args.color)
                time.sleep(0.03)
            utils.animacao_vitoria_recursiva(20)
            continue

        if acao == "instrucoes":
            utils.imprime_instrucoes("README.md")
            continue

        # Jogar de fato
        j = iniciar_jogador(lab.entrada)
        while True:
            imprimir_labirinto(lab, j.pos, cor=args.color)
            cmd = mover(lab, j)
            if cmd == "sair":
                break
            # vitória?
            if j.pos == lab.saida:
                if console: console.print(f"[bold green]Parabéns, {nome}! Pontos: {j.pontos}[/]")
                else: print(f"Parabéns, {nome}! Pontos: {j.pontos}")
                utils.animacao_vitoria_recursiva(20)
                break

if __name__ == "__main__":
    main()
