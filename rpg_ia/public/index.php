<?php
session_start();
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Chat com Gemini</title>
  <link rel="stylesheet" href="Style.css">
</head>
<body>
  <div class="container">
    <h2>Campanha Automática (Gemini)</h2>

    <div class="controls">
      <button id="startBtn">Iniciar Campanha</button>
      <button id="clearBtn">Limpar Conversa</button>
    </div>

    <div id="chat" class="chat">
      <div class="notice">Nenhuma mensagem. Clique em "Iniciar Campanha" para começar.</div>
    </div>

    <div class="form">
      <textarea id="input" rows="3" placeholder="Digite sua mensagem..."></textarea>
      <button id="sendBtn">Enviar</button>
    </div>
  </div>

  <script src="app.js"></script>
</body>
</html>
