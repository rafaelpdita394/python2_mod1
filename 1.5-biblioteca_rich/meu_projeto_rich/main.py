import argparse
from personalizador import layout, painel, progresso, estilo

modulos = {
    "layout": layout,
    "painel": painel,
    "progresso": progresso,
    "estilo": estilo
}

funcoes = {
    "layout": ["exibir_layout", "layout_colorido"],
    "painel": ["painel_simples", "painel_colorido"],
    "progresso": ["progresso_simples", "progresso_colorido"],
    "estilo": ["texto_bold", "texto_italic_color"]
}

parser = argparse.ArgumentParser(description="Exibe textos formatados com Rich.")
parser.add_argument("entrada", type=str, help="Texto ou caminho do arquivo a ser exibido")
parser.add_argument("-a", "--arquivo", action="store_true", help="Indica que a entrada é um arquivo")
parser.add_argument("-m", "--modulo", choices=list(modulos.keys()), required=True, help="Módulo a utilizar: layout, painel, progresso, estilo")
parser.add_argument("-f", "--funcao", required=True, help="Função do módulo. Opções:\n" + "\n".join([f"{k}: {', '.join(v)}" for k,v in funcoes.items()]))

args = parser.parse_args()

mod = modulos[args.modulo]
if args.funcao in funcoes[args.modulo]:
    func = getattr(mod, args.funcao)
    func(args.entrada, args.arquivo)
else:
    print(f"Função inválida para o módulo {args.modulo}.")
