<?php

require 'db.php';


$nome = "João";

$email = "joao@gmail.com";

$senha = password_hash("123456", PASSWORD_DEFAULT);


$sql = $pdo->prepare("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)");

$sql->execute([$nome, $email, $senha]);


echo "Usuário inserido com sucesso!";