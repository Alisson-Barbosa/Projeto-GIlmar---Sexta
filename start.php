<?php
session_start();
header('Content-Type: application/json; charset=utf-8');

// Mensagem inicial
$_SESSION['messages'] = [
  ['role' => 'assistant', 'text' => 'Olá! Eu sou o mestre da campanha. Deseja iniciar sua jornada?']
];

echo json_encode(['success' => true, 'messages' => $_SESSION['messages']]);
