<?php
session_start();
header('Content-Type: application/json; charset=utf-8');

// Mensagem inicial
$_SESSION['messages'] = [
  ['role' => 'assistant', 'text' => 'Olá! Eu sou o assistente da campanha. Como posso te ajudar hoje?']
];

echo json_encode(['success' => true, 'messages' => $_SESSION['messages']]);
