<?php

$code = htmlspecialchars($_POST["c-code"]);
print "$code";
$tests_description = htmlspecialchars($_POST["tests_description"]);
print "$tests_description";
$verification_script = htmlspecialchars($_POST["verification_script"]);
print "$verification_script";

?>
