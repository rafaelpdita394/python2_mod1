
# Aventura no Labirinto

Um jogo de terminal onde você explora um labirinto, coleta *itens* e tenta chegar à **saída**.

## Requisitos do Trabalho
- **Função recursiva**: `resolver_recursivo` (DFS) no módulo `labirinto.py` e `animacao_vitoria_recursiva` em `utils.py`.
- **`match-case`**: usado em `pontuar`, `mostrar_menu` e CLI (`tamanho_por_dificuldade`).
- **Bibliotecas externas**: `rich` (visual), `pynput` (teclado), `playsound` (som).
- **Ambiente virtual**: instalar dependências e exportar `requirements.txt`.
- **Modular**: pacote `aventura_pkg/` com três módulos.
- **Docstrings**: em todos os módulos do pacote.
- **CLI**: `main.py` com opções/argumentos (5+ com 1 obrigatório).

## Instalação

```bash
git clone <seu-repo>
cd aventura_no_labirinto
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Como executar

```bash
python main.py --name "Seu Nome" --color cyan --dificuldade medio
```

**Opções úteis**:

- `--auto-solve`: assiste a solução recursiva (bot joga sozinho).
- `--instrucoes`: mostra este README formatado e sai.
- `--disable-sound`: desativa música (usa `playsound` se `trilha.mp3` existir na pasta).

## Controles (durante o jogo)
- Setas ou **W/A/S/D** para mover.
- **ESC** ou **Q** para sair da partida.

## Dificuldades
- `facil` (17x11), `medio` (31x17), `dificil` (41x23).

## Itens e Pontuação
- Andar: +1 ponto
- Bater na parede: -1 ponto
- Coletar item `*`: +10 pontos
- Chegar à saída `S`: +50 pontos

## Documentação (docstrings)
Gerar HTML com pydoc (arquivo `aventura_pkg.html`):

```bash
python - << 'PY'
import pydoc
pydoc.writedoc('aventura_pkg')
PY
```

O arquivo será criado na raiz do projeto.

## Prints de Tela (sugestão)
Inclua imagens do terminal renderizado com `rich` mostrando o labirinto.
