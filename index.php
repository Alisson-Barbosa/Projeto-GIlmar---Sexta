<?php session_start(); ?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Chat com Gemini</title>
<link rel="stylesheet" href="Style.css">
</head>
<body>
  <div class="container">
    <h2>Campanha Automática</h2>

    <div class="controls">
      <button id="startBtn">Iniciar nova Campanha</button>
    </div>

    <div id="chat" class="chat">
      <div class="notice">Clique em "Iniciar nova Campanha" para começar.</div>
    </div>

    <div class="form">
      <textarea id="input" rows="3" placeholder="O que deseja fazer?"></textarea>
      <button id="sendBtn">Realizar Ação</button>
    </div>
  </div>

  <script src="app.js"></script>
</body>
</html>
