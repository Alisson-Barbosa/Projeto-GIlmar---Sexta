<?php

session_start();
header('Content-Type: application/json; charset=utf-8');

require_once __DIR__ . '/../src/GeminiClient.php';
$CONFIG = require __DIR__ . '/../config/config.php';

$input = json_decode(file_get_contents('php://input'), true);
$message = trim((string)($input['message'] ?? ''));

if ($message === '') {
    echo json_encode(['success' => false, 'error' => 'Mensagem vazia']);
    exit;
}

if (!isset($_SESSION['messages'])) {
    $_SESSION['messages'] = [];
}

// salva a mensagem do jogador
$_SESSION['messages'][] = ['role' => 'user', 'text' => $message, 'time' => time()];

// monta contexto simples (todas as mensagens) para enviar ao Gemini
$context = "";
foreach ($_SESSION['messages'] as $m) {
    $role = $m['role'] === 'user' ? 'Jogador' : 'Mestre';
    $context .= $role . ': ' . $m['text'] . "\n";
}
$context .= "Mestre: Continue a história a partir do contexto acima, descreva consequências e apresente novas opções de ação. Seja conciso.";

// chama Gemini
$client = new \App\Service\GeminiClient($CONFIG['gemini'] ?? []);
$reply = $client->sendMessage($context);

// salva resposta
$_SESSION['messages'][] = ['role' => 'assistant', 'text' => $reply, 'time' => time()];

echo json_encode(['success' => true, 'response' => $reply, 'messages' => $_SESSION['messages']]);