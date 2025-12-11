import random
import time

import pygame

from models import Robo, Arena

# -----------------------------------------
# Criação de robôs e arena
# -----------------------------------------


def criar_robo_jogador():
    print("Escolha seu robô inicial:")
    print("1 - Robô Vermelho (Agressivo)")
    print("2 - Robô Verde (Defensivo)")
    print("3 - Robô Azul (Velocista)")

    escolha = input("Digite o número: ")

    nome = input("Escolha um nome para seu robô: ")

    if escolha == "1":
        return Robo(nome, "vermelho", 3, 2, 1, "agressivo")

    elif escolha == "2":
        return Robo(nome, "verde", 2, 3, 1, "defensivo")

    else:
        return Robo(nome, "azul", 1, 1, 4, "velocista")


def criar_arena():
    return Arena(largura=16, altura=5)


# -----------------------------------------
# Lógica de progressão da campanha
# -----------------------------------------

# Status máximo do adversário por partida (1 a 10)
STATUS_MAX_POR_PARTIDA = [6, 7, 8, 10, 11, 12, 14, 15, 16, 18]


def obter_status_maximo(partida: int) -> int:
    """
    Retorna o status máximo da partida (1 a 10).
    Usa a tabela acima, baseada no exemplo do documento.
    """
    indice = max(1, min(partida, 10)) - 1
    return STATUS_MAX_POR_PARTIDA[indice]


def gerar_stats_aleatorios(status_max: int) -> tuple[int, int, int]:
    """
    Gera (ataque, defesa, velocidade) com soma = status_max.
    Garante que cada um é pelo menos 1.
    """
    # ataque entre 1 e status_max - 2
    ataque = random.randint(1, status_max - 2)
    restante = status_max - ataque

    defesa = random.randint(1, restante - 1)
    velocidade = restante - defesa

    return ataque, defesa, velocidade


def definir_cor_e_personalidade(ataque: int, defesa: int, velocidade: int) -> tuple[str, str]:
    """
    Define cor do robô adversário com base no maior status:
    - maior = ataque -> vermelho
    - maior = defesa -> verde
    - maior = velocidade -> azul
    - todos iguais -> branco
    - empate entre dois -> escolhe aleatório entre as cores correspondentes

    Também define personalidade:
    - ataque maior -> agressivo
    - defesa maior -> defensivo
    - velocidade maior -> velocista
    - empatado -> aleatório entre esses perfis
    """
    valores = {"ataque": ataque, "defesa": defesa, "velocidade": velocidade}
    max_valor = max(valores.values())

    maiores = [k for k, v in valores.items() if v == max_valor]

    cores_map = {
        "ataque": "vermelho",
        "defesa": "verde",
        "velocidade": "azul",
    }

    if len(maiores) == 3:
        cor = "branco"
    elif len(maiores) == 1:
        cor = cores_map[maiores[0]]
    else:
        cor = cores_map[random.choice(maiores)]

    # personalidade
    if len(maiores) == 1:
        if maiores[0] == "ataque":
            personalidade = "agressivo"
        elif maiores[0] == "defesa":
            personalidade = "defensivo"
        else:
            personalidade = "velocista"
    else:
        personalidade = random.choice(["agressivo", "defensivo", "velocista"])

    return cor, personalidade


def criar_robo_adversario_procedural(partida: int) -> Robo:
    status_max = obter_status_maximo(partida)
    ataque, defesa, velocidade = gerar_stats_aleatorios(status_max)
    cor, personalidade = definir_cor_e_personalidade(ataque, defesa, velocidade)

    print(f"\n[INFO] Gerando adversário da partida {partida}...")
    print(
        f"Status máximo: {status_max} | "
        f"Ataque: {ataque}, Defesa: {defesa}, Velocidade: {velocidade} | Cor: {cor}"
    )

    nome = f"Adversário {partida}"
    return Robo(nome, cor, ataque, defesa, velocidade, personalidade)


def aplicar_upgrade(jogador: Robo):
    """
    Após cada vitória, jogador escolhe onde aplicar +1 ponto.
    - ataque: aumenta dano
    - defesa: aumenta redução de dano e HP máximo (+10)
    - velocidade: aumenta chance de agir primeiro e mobilidade
    """
    print("\n🏅 Você venceu! Ganho de 1 ponto de status.")
    print("Onde deseja aplicar o ponto?")
    print("1 - Ataque")
    print("2 - Defesa")
    print("3 - Velocidade")

    escolha = input("Digite o número (1/2/3): ").strip()

    if escolha == "1":
        jogador.ataque += 1
        print(f"{jogador.nome} agora tem ATAQUE {jogador.ataque}.")
    elif escolha == "2":
        jogador.defesa += 1
        jogador.hp_max += 10
        jogador.hp_atual += 10
        if jogador.hp_atual > jogador.hp_max:
            jogador.hp_atual = jogador.hp_max
        print(
            f"{jogador.nome} agora tem DEFESA {jogador.defesa} "
            f"e HP máximo {jogador.hp_max}."
        )
    else:
        jogador.velocidade += 1
        print(f"{jogador.nome} agora tem VELOCIDADE {jogador.velocidade}.")

    print(
        f"Status atual: ATAQUE {jogador.ataque} | "
        f"DEFESA {jogador.defesa} | VELOCIDADE {jogador.velocidade}"
    )


# -----------------------------------------
# Pygame – janela e desenho
# -----------------------------------------


def iniciar_pygame(arena: Arena):
    pygame.init()
    largura_tela = 800
    altura_tela = 400
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("ARIA - Arena de Robôs IA")
    fonte = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()
    return tela, fonte, clock


def desenhar_arena(tela, arena: Arena, jogador: Robo, adversario: Robo, fonte, turno: int):
    largura_tela, altura_tela = tela.get_size()

    cor_fundo = (90, 70, 50)    # marrom
    cor_arena = (160, 160, 160) # cinza
    cor_borda = (0, 0, 0)

    tela.fill(cor_fundo)

    margem = 60
    arena_larg_px = largura_tela - 2 * margem
    arena_alt_px = altura_tela - 2 * margem
    arena_rect = pygame.Rect(margem, margem, arena_larg_px, arena_alt_px)

    # Área da arena
    pygame.draw.rect(tela, cor_arena, arena_rect)
    pygame.draw.rect(tela, cor_borda, arena_rect, 3)

    # Tamanho de cada "célula" lógica
    cell_w = arena_larg_px / arena.largura
    cell_h = arena_alt_px / arena.altura

    def desenhar_robo(robo: Robo):
        cores = {
            "vermelho": (220, 60, 60),
            "verde": (60, 220, 60),
            "azul": (80, 80, 220),
            "branco": (230, 230, 230),
        }
        cor = cores.get(robo.cor, (200, 200, 200))

        cx = arena_rect.left + robo.x * cell_w + cell_w / 2
        cy = arena_rect.top + robo.y * cell_h + cell_h / 2

        raio = int(min(cell_w, cell_h) / 3)
        pygame.draw.circle(tela, cor, (int(cx), int(cy)), raio)
        pygame.draw.circle(tela, cor_borda, (int(cx), int(cy)), raio, 2)

    desenhar_robo(jogador)
    desenhar_robo(adversario)

    # HUD
    hud1 = fonte.render(
        f"{jogador.nome} HP {jogador.hp_atual}/{jogador.hp_max}", True, (255, 255, 255)
    )
    hud2 = fonte.render(
        f"{adversario.nome} HP {adversario.hp_atual}/{adversario.hp_max}",
        True,
        (255, 255, 255),
    )
    hud_turno = fonte.render(f"Turno {turno}", True, (255, 255, 0))

    tela.blit(hud1, (20, 10))
    tela.blit(hud2, (largura_tela - hud2.get_width() - 20, 10))
    tela.blit(hud_turno, (largura_tela / 2 - hud_turno.get_width() / 2, 10))


# -----------------------------------------
# Interpretação de comandos do jogador
# -----------------------------------------


def interpretar_comando(texto: str) -> dict:
    """
    Recebe um texto e devolve um dicionário com ajustes de preferência.
    Ex: "focar no ataque" -> {"ataque": +2}
    Aqui usamos uma lógica simples de palavras-chave.
    """

    texto = texto.lower()
    preferencias = {"ataque": 0, "defesa": 0, "esquiva": 0}

    if not texto.strip():
        # Nenhum comando = não muda nada
        return preferencias

    # Ataque
    if "ataq" in texto or "agress" in texto or "bate" in texto:
        preferencias["ataque"] += 2

    # Defesa
    if "defes" in texto or "proteg" in texto or "tank" in texto:
        preferencias["defesa"] += 2

    # Esquiva / distância
    if "esquiv" in texto or "desvi" in texto or "foge" in texto or "distân" in texto:
        preferencias["esquiva"] += 2

    # Combos simples
    if "contra" in texto:
        # defesa + ataque
        preferencias["defesa"] += 1
        preferencias["ataque"] += 1

    return preferencias


def obter_comando_do_jogador(robo_jogador: Robo):
    print(
        "\n💬 Oriente seu robô "
        "(ex: 'focar no ataque', 'focar mais na defesa', "
        "'tentar esquivar', 'esquiva e contra-ataca'):"
    )
    texto = input("Comando (ou deixe vazio para manter): ")

    prefs = interpretar_comando(texto)
    robo_jogador.aplicar_preferencias(prefs)

    print(
        f"Preferências atualizadas: "
        f"ATAQUE x{robo_jogador.pref_ataque}, "
        f"DEFESA x{robo_jogador.pref_defesa}, "
        f"ESQUIVA x{robo_jogador.pref_esquiva}"
    )


# -----------------------------------------
# Simulação de batalha com arena + visual
# -----------------------------------------


def mostrar_status_terminal(jogador: Robo, adversario: Robo, arena: Arena, turno: int):
    print(f"\n----- TURNO {turno} -----")
    print(
        f"{jogador.nome}: HP {jogador.hp_atual}/{jogador.hp_max} "
        f"Pos {jogador.posicao()}  ||  "
        f"{adversario.nome}: HP {adversario.hp_atual}/{adversario.hp_max} "
        f"Pos {adversario.posicao()}"
    )
    dist = arena.distancia(jogador, adversario)
    print(f"Distância entre eles: {dist}")


def simular_batalha(
    jogador: Robo,
    adversario: Robo,
    arena: Arena,
    tela,
    fonte,
    clock,
) -> bool:
    """
    Executa uma batalha entre jogador e adversário.
    Retorna True se o jogador venceu, False se perdeu ou a janela foi fechada.
    """
    print("\n🔥 A BATALHA VAI COMEÇAR! 🔥")
    print(
        f"{jogador.nome} (HP {jogador.hp_atual})  "
        f"VS  {adversario.nome} (HP {adversario.hp_atual})\n"
    )

    # Posição inicial dos robôs na arena
    jogador.set_posicao(2, arena.altura // 2, arena)
    adversario.set_posicao(arena.largura - 3, arena.altura // 2, arena)

    # Antes da batalha, já deixa o jogador orientar o robô
    obter_comando_do_jogador(jogador)

    turnos = 1
    rodando = True

    # Primeiro desenho antes dos turnos
    desenhar_arena(tela, arena, jogador, adversario, fonte, turnos)
    pygame.display.flip()

    while jogador.esta_vivo() and adversario.esta_vivo() and rodando:
        # Eventos do Pygame (fechar janela, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        if not rodando:
            break

        mostrar_status_terminal(jogador, adversario, arena, turnos)

        # A cada turno, oferece opção de mudar a orientação
        mudar = input("Quer mudar a orientação do seu robô? (s/N): ").strip().lower()
        if mudar == "s":
            obter_comando_do_jogador(jogador)

        # quem age primeiro? (maior velocidade)
        ordem = sorted([jogador, adversario], key=lambda r: r.velocidade, reverse=True)

        for robo in ordem:
            if not jogador.esta_vivo() or not adversario.esta_vivo():
                break

            alvo = adversario if robo is jogador else jogador

            dist_atual = arena.distancia(robo, alvo)
            acao = robo.escolher_acao()

            # ---------- Lógica de movimento + ação ----------

            if acao == "atacar":
                if dist_atual <= 1:
                    dano = robo.atacar(alvo)
                    print(
                        f"{robo.nome} ATACA! Causa {dano} de dano em {alvo.nome}."
                    )
                else:
                    robo.mover_em_direcao(alvo, arena, aproximar=True)
                    print(
                        f"{robo.nome} se aproxima de {alvo.nome} "
                        f"e vai para {robo.posicao()} "
                        f"(distância {arena.distancia(robo, alvo)})."
                    )

            elif acao == "defender":
                print(f"{robo.nome} levanta a guarda e se prepara para reduzir dano.")
                # futura lógica de buff de defesa pode entrar aqui

            elif acao == "esquivar":
                print(f"{robo.nome} tenta ESQUIVAR e se afastar!")
                robo.mover_em_direcao(alvo, arena, aproximar=False)
                print(
                    f"{robo.nome} recua para {robo.posicao()} "
                    f"(distância {arena.distancia(robo, alvo)})."
                )

            print(
                f"{alvo.nome} agora tem {alvo.hp_atual} HP "
                f"e está em {alvo.posicao()}."
            )

        # Atualiza visual
        desenhar_arena(tela, arena, jogador, adversario, fonte, turnos)
        pygame.display.flip()

        turnos += 1
        clock.tick(60)
        time.sleep(0.3)

    print("\n💥 FIM DA BATALHA! 💥")

    if not jogador.esta_vivo():
        print(f"🏆 {adversario.nome} venceu!")
        return False

    if not adversario.esta_vivo():
        print(f"🏆 {jogador.nome} venceu!")
        return True

    # Se a janela foi fechada, consideramos como derrota / interrupção
    print("Jogo interrompido.")
    return False


# -----------------------------------------
# Campanha de 10 partidas
# -----------------------------------------


def jogar_campanha():
    arena = criar_arena()
    jogador = criar_robo_jogador()
    tela, fonte, clock = iniciar_pygame(arena)

    vitorias = 0
    total_partidas = 10

    for partida in range(1, total_partidas + 1):
        print("\n" + "=" * 40)
        print(f"🎮 INICIANDO PARTIDA {partida} da campanha.")
        print("=" * 40)

        # Reseta HP do jogador antes da partida
        jogador.hp_atual = jogador.hp_max

        adversario = criar_robo_adversario_procedural(partida)

        venceu = simular_batalha(jogador, adversario, arena, tela, fonte, clock)

        if not venceu:
            print(f"\n❌ Você foi derrotado na partida {partida}.")
            print(f"Vitórias totais: {vitorias}.")
            break

        vitorias += 1

        if vitorias == total_partidas:
            print("\n🏆🏆🏆 PARABÉNS! VOCÊ É O CAMPEÃO DO ARIA! 🏆🏆🏆")
            print(
                f"Robô: {jogador.nome} | "
                f"Ataque: {jogador.ataque} | "
                f"Defesa: {jogador.defesa} | "
                f"Velocidade: {jogador.velocidade} | "
                f"HP Máx: {jogador.hp_max}"
            )
            break

        # Se venceu e ainda não chegou na última partida, aplica upgrade
        aplicar_upgrade(jogador)

    print("\nObrigado por jogar ARIA - Arena de Robôs IA!")
    pygame.quit()


def iniciar_jogo():
    jogar_campanha()
