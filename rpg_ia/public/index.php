<?php

session_start();
$messages = $_SESSION['messages'] ?? [];
?>
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>RPG Chat (Gemini)</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main class="container">
    <h1>RPG Chat (Gemini)</h1>

    <div class="controls">
      <button id="startBtn">Iniciar Campanha</button>
      <button id="clearBtn">Limpar Conversa</button>
    </div>

    <section id="chat" class="chat">
      <?php if (empty($messages)): ?>
        <div class="notice">Nenhuma mensagem. Clique em "Iniciar Campanha" para começar.</div>
      <?php else: ?>
        <?php foreach ($messages as $m): ?>
          <div class="msg <?= htmlspecialchars($m['role']) ?>">
            <div class="text"><?= nl2br(htmlspecialchars($m['text'])) ?></div>
          </div>
        <?php endforeach; ?>
      <?php endif; ?>
    </section>

    <form id="form" class="form" onsubmit="return false;">
      <textarea id="input" placeholder="Escreva sua ação..." rows="3"></textarea>
      <div class="actions">
        <button id="sendBtn" type="button">Enviar</button>
      </div>
    </form>
  </main>

  <script src="app.js"></script>
</body>
</html>