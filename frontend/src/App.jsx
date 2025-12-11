import { useState, useEffect } from "react";

const API_BASE = "https://arena-de-robos-ia.onrender.com";

function App() {
  const [roboEscolha, setRoboEscolha] = useState(1);
  const [nomeRobo, setNomeRobo] = useState("Meu Robo");
  const [gameState, setGameState] = useState(null);
  const [commandText, setCommandText] = useState("");
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");

  const temJogo = !!gameState;

  async function iniciarNovoJogo(e) {
    e.preventDefault();
    setErro("");
    setLoading(true);

    try {
      const resp = await fetch(`${API_BASE}/new_game`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          robo_escolha: Number(roboEscolha),
          nome: nomeRobo || "SemNome",
        }),
      });

      if (!resp.ok) {
        let msg = "Erro ao iniciar jogo";
        try {
          const data = await resp.json();
          msg = data.detail || msg;
        } catch (_) {}
        throw new Error(msg);
      }

      const data = await resp.json();

      // Normaliza o estado para evitar undefined
      setGameState({
        ...data,
        arena: data.arena || { largura: 16, altura: 5 },
        logs: Array.isArray(data.logs) ? data.logs : [],
      });
      setCommandText("");
    } catch (err) {
      console.error(err);
      setErro(err.message || "Erro desconhecido ao iniciar jogo");
    } finally {
      setLoading(false);
    }
  }

  async function enviarComando(e) {
    if (e) e.preventDefault();
    if (!temJogo || !commandText.trim()) return;

    setErro("");
    setLoading(true);

    try {
      const resp = await fetch(`${API_BASE}/command`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ texto: commandText }),
      });

      if (!resp.ok) {
        let msg = "Erro ao enviar comando";
        try {
          const data = await resp.json();
          msg = data.detail || msg;
        } catch (_) {}
        throw new Error(msg);
      }

      const data = await resp.json();
      setGameState((prev) => {
        const merged = { ...(prev || {}), ...data };
        return {
          ...merged,
          arena: merged.arena || { largura: 16, altura: 5 },
          logs: Array.isArray(merged.logs) ? merged.logs : [],
        };
      });
    } catch (err) {
      console.error(err);
      setErro(err.message || "Erro desconhecido ao enviar comando");
    } finally {
      setLoading(false);
    }
  }

  async function executarTurno() {
    // usado pelo auto-loop
    if (!temJogo) return;
    if (loading) return;
    if (jogoFinalizado) return;

    setErro("");
    setLoading(true);

    try {
      const resp = await fetch(`${API_BASE}/turno`, {
        method: "POST",
      });

      if (!resp.ok) {
        let msg = "Erro ao executar turno";
        try {
          const data = await resp.json();
          msg = data.detail || msg;
        } catch (_) {}
        throw new Error(msg);
      }

      const data = await resp.json();
      setGameState((prev) => {
        const merged = { ...(prev || {}), ...data };
        return {
          ...merged,
          arena: merged.arena || { largura: 16, altura: 5 },
          logs: Array.isArray(merged.logs) ? merged.logs : [],
        };
      });
    } catch (err) {
      console.error(err);
      setErro(err.message || "Erro desconhecido ao executar turno");
    } finally {
      setLoading(false);
    }
  }

  function statusLabel(status) {
    if (status === "running") return "Em andamento";
    if (status === "player_won") return "Vitória do jogador";
    if (status === "enemy_won") return "Vitória do adversário";
    return status;
  }

  const jogoFinalizado =
    gameState && gameState.status && gameState.status !== "running";

  const arenaData = gameState?.arena || { largura: 16, altura: 5 };
  const logs = Array.isArray(gameState?.logs) ? gameState.logs : [];

  // 🔁 Loop automático de turnos a cada 10s
  useEffect(() => {
    if (!temJogo || jogoFinalizado) return;

    const id = setInterval(() => {
      executarTurno();
    }, 2000); // 2 segundos

    return () => clearInterval(id);
  }, [temJogo, jogoFinalizado, gameState?.turno]); // reinicia o timer quando o turno muda

  return (
    <div
      style={{
        minHeight: "100vh",
        padding: "16px",
        background: "#020617",
        color: "#f5f5f5",
        fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
      }}
    >
      <h1 style={{ textAlign: "center", marginBottom: "8px", fontSize: "2.4rem" }}>
        ARIA – Arena de Robôs IA (Frontend React)
      </h1>
      <p style={{ textAlign: "center", marginBottom: "24px", opacity: 0.8 }}>
        Controle seu robô via API FastAPI – escolha o robô, envie comandos e
        acompanhe os turnos automáticos.
      </p>

      {/* Seção de novo jogo */}
      <section
        style={{
          maxWidth: "800px",
          margin: "0 auto 24px auto",
          padding: "16px",
          borderRadius: "16px",
          background: "#020617",
          boxShadow: "0 0 24px rgba(15,23,42,0.9)",
          border: "1px solid #1e293b",
        }}
      >
        <h2 style={{ marginBottom: "8px" }}>Novo jogo</h2>
        <form
          onSubmit={iniciarNovoJogo}
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "12px",
            alignItems: "center",
          }}
        >
          <div>
            <label style={{ display: "block", marginBottom: "4px" }}>
              Robô inicial
            </label>
            <select
              value={roboEscolha}
              onChange={(e) => setRoboEscolha(e.target.value)}
              style={{
                padding: "6px 8px",
                borderRadius: "8px",
                border: "1px solid #334155",
                background: "#020617",
                color: "#f5f5f5",
              }}
            >
              <option value={1}>Vermelho (Agressivo)</option>
              <option value={2}>Verde (Defensivo)</option>
              <option value={3}>Azul (Velocista)</option>
            </select>
          </div>

          <div>
            <label style={{ display: "block", marginBottom: "4px" }}>
              Nome do robô
            </label>
            <input
              type="text"
              value={nomeRobo}
              onChange={(e) => setNomeRobo(e.target.value)}
              style={{
                padding: "6px 8px",
                borderRadius: "8px",
                border: "1px solid #334155",
                background: "#020617",
                color: "#f5f5f5",
              }}
              placeholder="Ex: Atlas, Bolt..."
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              padding: "10px 18px",
              borderRadius: "999px",
              border: "none",
              background: loading ? "#475569" : "#3b82f6",
              color: "#fff",
              cursor: loading ? "default" : "pointer",
              marginTop: "22px",
              fontWeight: 600,
            }}
          >
            {loading ? "Carregando..." : "Iniciar jogo"}
          </button>
        </form>
      </section>

      {/* Mensagens de erro */}
      {erro && (
        <div
          style={{
            maxWidth: "800px",
            margin: "0 auto 16px auto",
            padding: "10px 14px",
            borderRadius: "10px",
            background: "#7f1d1d",
          }}
        >
          <strong>Erro:</strong> {erro}
        </div>
      )}

      {/* Estado do jogo */}
      {temJogo && (
        <section
          style={{
            maxWidth: "1100px",
            margin: "0 auto",
            display: "grid",
            gridTemplateColumns: "1.4fr 0.9fr",
            gap: "16px",
          }}
        >
          {/* Painel principal */}
          <div
            style={{
              padding: "16px",
              borderRadius: "16px",
              background: "#020617",
              boxShadow: "0 0 24px rgba(15,23,42,0.9)",
              border: "1px solid #1e293b",
            }}
          >
            <h2 style={{ marginBottom: "4px" }}>Estado da batalha</h2>
            <p style={{ marginBottom: "4px", opacity: 0.8 }}>
              Turno: <strong>{gameState.turno}</strong> | Status:{" "}
              <strong>{statusLabel(gameState.status)}</strong>
            </p>
            <p style={{ marginBottom: "12px", opacity: 0.7, fontSize: "0.85rem" }}>
              Os turnos são executados automaticamente a cada 10 segundos enquanto
              a batalha estiver em andamento.
            </p>

            <div
              style={{
                display: "flex",
                gap: "12px",
                marginBottom: "16px",
                flexWrap: "wrap",
              }}
            >
              <RoboCard title="Jogador" robo={gameState.jogador} destaque />
              <RoboCard title="Adversário" robo={gameState.adversario} />
            </div>

            {/* Arena visual em grid */}
            <div
              style={{
                marginBottom: "16px",
                padding: "12px",
                borderRadius: "12px",
                background: "#020617",
                border: "1px solid #1e293b",
              }}
            >
              <h3 style={{ marginBottom: "8px" }}>Arena</h3>
              <ArenaGrid
                largura={arenaData.largura}
                altura={arenaData.altura}
                jogador={gameState.jogador}
                adversario={gameState.adversario}
              />
            </div>

            <form
              onSubmit={enviarComando}
              style={{ display: "flex", gap: "8px", marginBottom: "12px" }}
            >
              <input
                type="text"
                value={commandText}
                onChange={(e) => setCommandText(e.target.value)}
                placeholder="Ex: focar no ataque, focar mais na defesa, tentar esquivar..."
                style={{
                  flex: 1,
                  padding: "8px 10px",
                  borderRadius: "8px",
                  border: "1px solid #334155",
                  background: "#020617",
                  color: "#f5f5f5",
                }}
              />
              <button
                type="submit"
                disabled={loading || !commandText.trim() || jogoFinalizado}
                style={{
                  padding: "8px 12px",
                  borderRadius: "8px",
                  border: "none",
                  background: jogoFinalizado ? "#475569" : "#22c55e",
                  color: "#fff",
                  cursor:
                    loading || !commandText.trim() || jogoFinalizado
                      ? "default"
                      : "pointer",
                  whiteSpace: "nowrap",
                  fontWeight: 600,
                }}
              >
                Enviar comando
              </button>
            </form>

            {jogoFinalizado && (
              <p style={{ marginTop: "10px", color: "#22c55e" }}>
                A batalha terminou. Inicie um novo jogo acima para recomeçar.
              </p>
            )}
          </div>

          {/* Logs */}
          <div
            style={{
              padding: "16px",
              borderRadius: "16px",
              background: "#020617",
              boxShadow: "0 0 24px rgba(15,23,42,0.9)",
              border: "1px solid #1e293b",
              maxHeight: "420px",
              overflowY: "auto",
            }}
          >
            <h3 style={{ marginBottom: "8px" }}>Logs</h3>
            {logs.length === 0 ? (
              <p style={{ opacity: 0.7 }}>Nenhum log ainda.</p>
            ) : (
              <ul
                style={{
                  listStyle: "none",
                  padding: 0,
                  margin: 0,
                  fontSize: "0.9rem",
                }}
              >
                {logs.map((log, idx) => (
                  <li
                    key={idx}
                    style={{
                      marginBottom: "6px",
                      paddingBottom: "4px",
                      borderBottom: "1px solid rgba(148,163,184,0.1)",
                    }}
                  >
                    {log}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </section>
      )}

      {!temJogo && (
        <p style={{ textAlign: "center", marginTop: "16px", opacity: 0.7 }}>
          Inicie um novo jogo acima para começar a batalha.
        </p>
      )}
    </div>
  );
}

function RoboCard({ title, robo, destaque = false }) {
  if (!robo) return null;

  const hpPercent =
    robo.hp_max > 0 ? Math.max(0, (robo.hp_atual / robo.hp_max) * 100) : 0;

  return (
    <div
      style={{
        flex: 1,
        minWidth: "230px",
        padding: "12px",
        borderRadius: "12px",
        border: destaque ? "1px solid #3b82f6" : "1px solid #1f2937",
        background: "#020617",
      }}
    >
      <h3 style={{ marginBottom: "4px" }}>
        {title}: {robo.nome}
      </h3>
      <p style={{ marginBottom: "4px", fontSize: "0.9rem", opacity: 0.85 }}>
        Cor: {robo.cor} | ATK: {robo.ataque} | DEF: {robo.defesa} | VEL:{" "}
        {robo.velocidade}
      </p>
      <div style={{ marginBottom: "4px" }}>
        <span style={{ fontSize: "0.85rem" }}>
          HP: {robo.hp_atual}/{robo.hp_max}
        </span>
        <div
          style={{
            marginTop: "4px",
            width: "100%",
            height: "8px",
            borderRadius: "999px",
            background: "#020617",
            overflow: "hidden",
            border: "1px solid #1f2937",
          }}
        >
          <div
            style={{
              width: `${hpPercent}%`,
              height: "100%",
              background:
                hpPercent > 60
                  ? "#22c55e"
                  : hpPercent > 30
                  ? "#eab308"
                  : "#ef4444",
              transition: "width 0.3s ease",
            }}
          />
        </div>
      </div>
      <p style={{ fontSize: "0.8rem", opacity: 0.75, marginTop: "4px" }}>
        Posição: ({robo.x}, {robo.y})
      </p>
    </div>
  );
}

function ArenaGrid({ largura, altura, jogador, adversario }) {
  const w = Number.isFinite(largura) ? largura : 16;
  const h = Number.isFinite(altura) ? altura : 5;

  const cells = [];

  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const isJogador = jogador?.x === x && jogador?.y === y;
      const isAdversario = adversario?.x === x && adversario?.y === y;

      let bg = "#020617";
      let border = "1px solid #1e293b";
      let content = "";

      if (isJogador && isAdversario) {
        bg = "#f97316"; // os dois na mesma célula (raro)
        content = "X";
      } else if (isJogador) {
        bg = "#22c55e";
        content = "J";
      } else if (isAdversario) {
        bg = "#ef4444";
        content = "A";
      }

      cells.push(
        <div
          key={`${x}-${y}`}
          style={{
            width: "22px",
            height: "22px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "0.7rem",
            border,
            background: bg,
          }}
        >
          {content}
        </div>
      );
    }
  }

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: `repeat(${w}, 22px)`,
        gap: "2px",
        justifyContent: "center",
      }}
    >
      {cells}
    </div>
  );
}

export default App;
