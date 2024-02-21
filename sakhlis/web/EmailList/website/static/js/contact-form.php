<?php
$name = $_POST['name'];
$home = $_POST['home'];
$phone = $_POST['phone'];
$comments = $_POST['comments'];


$name = htmlspecialchars($name);
$home = htmlspecialchars($home);
$phone = htmlspecialchars($phone);
$comments = htmlspecialchars($comments);


$name = urlencode($name);
$home = urlencode($home);
$phone = urlencode($phone);
$comments = urlencode($comments);



$name = trim($name);
$tel = trim($tel);
$phone = trim($phone);
$comments = trim($comments);


if (mail("alprostov.1982@gmail.com",
     "Заказ на работы!",
	"Имя: ".$name."\n".
     "Адрес: ".$home."\n".
     "Телефон: ".$phone."\n".
     "Комментарий: ".$comments."\n",
     	"From: address_post@1gb.ru\r\nContent-type: text/plain; charset=utf-8")
){
     echo ("<h3>Ваш заказ принят. Мы Вам перезвоним.</h3>");
}

else {
     echo ("Error");
}


?>