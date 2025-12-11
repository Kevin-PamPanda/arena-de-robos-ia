from models import Robo, Arena
import random
import time

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


def criar_robo_adversario():
    """
    Adversário temporário para as fases iniciais.
    Depois vamos substituir pelo gerador procedural da Fase 5.
    """
    return Robo("Adversário", "branco", 2, 2, 2, "agressivo")


def criar_arena():
    return Arena(largura=16, altura=5)


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
    print("\n💬 Oriente seu robô (ex: 'focar no ataque', 'focar mais na defesa', 'tentar esquivar', 'esquiva e contra-ataca'):")
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
# Simulação de batalha com arena
# -----------------------------------------

def mostrar_status(jogador: Robo, adversario: Robo, arena: Arena, turno: int):
    print(f"\n----- TURNO {turno} -----")
    print(
        f"{jogador.nome}: HP {jogador.hp_atual}/{jogador.hp_max} "
        f"Pos {jogador.posicao()}  ||  "
        f"{adversario.nome}: HP {adversario.hp_atual}/{adversario.hp_max} "
        f"Pos {adversario.posicao()}"
    )
    dist = arena.distancia(jogador, adversario)
    print(f"Distância entre eles: {dist}")


def simular_batalha(jogador: Robo, adversario: Robo, arena: Arena):
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

    while jogador.esta_vivo() and adversario.esta_vivo():
        mostrar_status(jogador, adversario, arena, turnos)

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
                    print(f"{robo.nome} ATACA! Causa {dano} de dano em {alvo.nome}.")
                else:
                    robo.mover_em_direcao(alvo, arena, aproximar=True)
                    print(
                        f"{robo.nome} se aproxima de {alvo.nome} "
                        f"e vai para {robo.posicao()} (distância {arena.distancia(robo, alvo)})."
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
                # Podemos, no futuro, usar essa ação para reduzir chance de ser acertado

            print(
                f"{alvo.nome} agora tem {alvo.hp_atual} HP "
                f"e está em {alvo.posicao()}."
            )

        turnos += 1
        time.sleep(0.8)

    print("\n💥 FIM DA BATALHA! 💥")

    if jogador.esta_vivo():
        print(f"🏆 {jogador.nome} venceu!")
    else:
        print(f"🏆 {adversario.nome} venceu!")


def iniciar_jogo():
    arena = criar_arena()
    jogador = criar_robo_jogador()
    adversario = criar_robo_adversario()

    simular_batalha(jogador, adversario, arena)
