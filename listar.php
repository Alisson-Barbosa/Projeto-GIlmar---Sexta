<?php

require 'db.php';


$consulta = $pdo->query("SELECT * FROM usuarios");


foreach ($consulta as $linha) {

echo $linha['id'] . " - " . $linha['nome'] . " - " . $linha['email'] . "<br>";

} 