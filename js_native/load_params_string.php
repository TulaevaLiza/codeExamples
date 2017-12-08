<?php


/**
 * загрузка стуктуры калькулятора и полей формы из базы
 * @return {JSON} 
 */



mysql_query_c("set character_set_client='cp1251'");
mysql_query_c("set character_set_results='cp1251'");
mysql_query_c("set collation_connection='cp1251_bin'");


$data=array();

$blockStatus=array("1"=>"rooms","2"=>"subblocks");

$res = mysql_query_c("select * from fields");
while($rw = mysql_fetch_array($res)) 
{
	$fields_name[$rw[id]]=$rw[name];
	$fields[$rw[id]]['type']=$rw['type'];
	$fields[$rw[id]]['name']=iconv("cp1251","utf-8",$rw[name_rus]);
	if($rw[add])
	{
		$tmp_ar=json_decode("{".iconv("cp1251","utf-8",$rw[add])."}");
		foreach($tmp_ar as $k=>$v) 
		{
			$fields[$rw[id]][$k]=$v;
		}
	}
}


$res = mysql_query_c("select * from params2fields");
while($rw = mysql_fetch_array($res)) 
{
	$par2f[$rw[param]][$fields_name[$rw[field]]]=$fields[$rw[field]];
}

$res = mysql_query_c("select * from params");
while($rw = mysql_fetch_array($res))  
{
	if($rw[status]>0)
	{
		$data[$blockStatus[$rw[status]]][$rw[name]]['name']=iconv("cp1251","utf-8",$rw[name_rus]);
		if($rw['formType'])
			$data[$blockStatus[$rw[status]]][$rw[name]]['formType']=$rw[formType];
		if($par2f[$rw[id]])
			$data[$blockStatus[$rw[status]]][$rw[name]]['fields']=$par2f[$rw[id]];
	}
	else
	{
		$data[$rw[name]]['name']=iconv("cp1251","utf-8",$rw[name_rus]);
		if($rw['formType'])
			$data[$rw[name]]['formType']=$rw[formType];
		if($par2f[$rw[id]])
			$data[$rw[name]]['fields']=$par2f[$rw[id]];
	}
}


echo json_encode($data);


function mysql_query_c($query)
{
	GLOBAL $db;
	if (!$db)
	{
		$db = mysql_connect("host","user","pwd") or die("Can't connect");
		mysql_select_db("dnname",$db) or die("Can't select db");
	}
	$res = mysql_query($query,$db);
	return $res;
}

?>