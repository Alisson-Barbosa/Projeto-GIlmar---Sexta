<?php

session_start();
header('Content-Type: application/json; charset=utf-8');

require_once __DIR__ . '/../src/GeminiClient.php';
$CONFIG = require __DIR__ . '/../config/config.php';

$client = new \App\Service\GeminiClient($CONFIG['gemini'] ?? []);

// Prompt inicial da campanha
$prompt = "Você é um Mestre de RPG. Apresente uma introdução curta para uma campanha medieval sombria, descreva o cenário inicial e ofereça 3 opções numeradas do que o jogador pode fazer. Seja conciso.";

$reply = $client->sendMessage($prompt);

// reinicia conversa na sessão e salva retorno
$_SESSION['messages'] = [];
if ($reply !== '') {
    $_SESSION['messages'][] = ['role' => 'assistant', 'text' => $reply, 'time' => time()];
}

echo json_encode(['success' => true, 'response' => $reply, 'messages' => $_SESSION['messages']]);