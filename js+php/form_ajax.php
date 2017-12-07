<?php

$messages=array(
"1"=>array("subject"=>"Заявка на выезд специалиста",
	   "text"=>"<p><b>Требуется выезд специалиста</b></p><table><tr><td>Имя: </td><td>#name</td></tr><tr><td>Телефон: </td><td>#phone</td></tr></table>",
	    "success"=>"Ваша заявка на выезд специалиста успешно отправлена. Ожидайте звонка от менеджера компании."
	),
"2"=>array("subject"=>"Запрос обратного звонка",
	   "text"=>"<p><b>Клиент просит перезвонить</b></p><table><tr><td>Имя: </td><td>#name</td></tr><tr><td>Телефон: </td><td>#phone</td></tr></table>",
	    "success"=>"Ожидайте звонка от менеджера."
	),
"3"=>array("subject"=>"Заявка на замер и составление сметы",
	   "text"=>"<p><b>Требуется замер и составление сметы</b></p><table><tr><td>Имя: </td><td>#name</td></tr><tr><td>Телефон: </td><td>#phone</td></tr><tr><td>Адрес: </td><td>#address</td></tr><tr><td>Комментарий: </td><td>#comment</td></tr></table>",
	    "success"=>"Ваша заявка на замер и составление сметы успешно отправлена. Ожидайте звонка от менеджера компании."
	),
"7"=>array("subject"=>"Вопрос от клиента",
	   "text"=>"<p><b>Клиент задал вопрос</b></p><table><tr><td>Имя: </td><td>#name</td></tr><tr><td>Телефон: </td><td>#phone</td></tr><tr><td>Вопрос: </td><td>#comment</td></tr></table>",
	    "success"=>"Ваш вопрос отправлен менеджерам компании. Ожидайте обратного звонка."
	)

);


foreach ($_POST as $k=>$v)
	${$k}=iconv("UTF-8","Windows-1251",$v);

if(!$type) $type=3;

$data=array();


$to="test@yandex.ru";


$subject=$messages[$type]['subject'];
$message=$messages[$type]['text'];

$message=preg_replace("/#name/",$name,$message);
$message=preg_replace("/#phone/",$phone,$message);
$message=preg_replace("/#address/",$address,$message);
$message=preg_replace("/#comment/",$comment,$message);



$headers  = "MIME-Version: 1.0\r\n";
$headers .= "Content-type: text/html; charset:cp-1251\r\n";
$headers .= "From: SiteName <noreply@sitenname.com>\r\n";



if(mail($to,$subject,$message,$headers))
{
	$data[response]=$messages[$type][success];
	$data[status]='success';
}
else
{
	$data[response]="Произошла ошибка отправки Вашего письма. Попробуйте отправить позже или позвоните на указанные на сайте телефоны.";
	$data[status]='error';
}


echo iconv("Windows-1251","UTF-8","{\"status\":\"$data[status]\",\"response\":\"$data[response]\"}");
?>