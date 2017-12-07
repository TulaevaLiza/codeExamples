<?php

/**
 * ��������� �������, ������������ � ������ ��������
 */

/**
 * ��������� �������� ������� �� ������� 
 * @params $word {string} �������� �������
 * @params $form {int} ����� (2 - ���������, 3 - �����������, 4 - �����������)
 * @return $out {string} ����� �������� �������
 */

function getRegionCase($word,$form)
{
	global $wordform_reps;
	if(!is_array($wordform_reps))
	{
		$wordform_reps[2] = array("��"=>"��","��"=>"��","��"=>"��","��"=>"��","��"=>"��","��"=>"��","(�� �-��|�� �������)"=>"�� �-���","��"=>"��","��"=>"��","(�|�|�)"=>"�","��"=>"��","(�|�|�|�|�|�|�|�|�|�)"=>"\\1�","�"=>"��","��"=>"��","��"=>"���","�"=>"��","�"=>"��","���������� ����"=>"�����","�������"=>"�������","������� ������"=>"������� ������","������-��-����"=>"�������-��-����","������ �����"=>"������ ������","����"=>"����");
		$wordform_reps[3] = array("��"=>"��","��"=>"��","��"=>"��","��"=>"��","��"=>"��","(�� �-��|�� �������)"=>"�� �-���","�"=>"�","��"=>"��","���"=>"����","��"=>"���","��"=>"��","��"=>"���","��"=>"��","�"=>"�","�"=>"","(�)�"=>"\\1�","([^�])�"=>"\\1�","(�|�|�|�|�|�|�|�)"=>"\\1�","�"=>"��","�"=>"��","���������� ����"=>"�����","������� ������"=>"������� ������","������-��-����"=>"�������-��-����","������ �����"=>"������� ������","����"=>"����");
		$wordform_reps[4] = array("��"=>"��","��"=>"��","��"=>"��","��"=>"��","��"=>"��","(�� �-��|�� �������)"=>"�� �-���","�"=>"�","��"=>"��","��"=>"��","��"=>"��","��"=>"��","��"=>"��","�"=>"�","�"=>"","(�)�"=>"\\1�","([^�])�"=>"\\1�","(�|�|�|�|�|�|�|�|�)"=>"\\1�","�"=>"��","���������� ����"=>"����","������� ������"=>"������� ������","������-��-����"=>"������-��-����","������ �����"=>"������ �����","����"=>"����");
	}

	$lt = ruslow($word);
	foreach ($wordform_reps[$form] as $k=>$v)
		if ($lt == ruslow($k)) return $v;

	$aa = preg_split("/\s+/",$word);
	foreach ($aa as $t)
	{
		foreach ($wordform_reps[$form] as $k=>$v)
			if (preg_match("/".$k."$/",$t)) 
			{
				$t = preg_replace("/".$k."$/",$v,$t);
				break;
			}

		$out.=($out?" ":"").$t;
	}
        return $out;

}

/**
 * ������������ �������� �������
 * @params $pl {string} id �������
 * @return $out {string} 
 */


function print_place_for_h1($pl)
{
// " � �������������� ������, �����-����������"
// " � �. ������ ������, ������ ������, ��������� �������"
	global $places;
	if(in_array($places[$pl]['sname'],array("�","�","�","���","���")) || $places[$pl]['level']>=2)
	{
		$s.=$places[$pl]['sname'] . ". ". $places[$pl]['name'];
	}
	else
		$s.= getRegionCase($places[$pl]['text_value'],2);

	$p=$places[$pl][parent];
	while($p>0)
	{
		$s1.=($s1?", ":""). getRegionCase($places[$p]['text_value'],3);
		$p=$places[$p][parent];
	}

	return $s." ".$s1;
}


/**
 * ���������� � ������� ��������, � �.�. ��������
 * @params $s {string} 
 * @return {string} 
 */

function ruslow($s)
{
	return strtolower(strtr($s,"��������������������������������","��������������������������������"));
}

/**
 * ���������� � ������� ��������, � �.�. ��������
 * @params $s {string} 
 * @return {string} 
 */

function rusup($s)
{
	return strtoupper(strtr($s,"��������������������������������","��������������������������������"));
}


//����� ����� ������ �� ������� ������ data � cols �������. 

/**
 * ������������ HTML ����: ������ ���������� � ������� � ������ �������� Bootstrap
 * @params $data {array} ������ ������ 
 * @params $cols {int} ���������� �������
 * @return {string} 
 */

function printCols($data,$cols=2)
{
	foreach($data as $s)
	{
		$o[(int)($i/$cols)][$i%$cols]=$s;
		$i++;
	}

	foreach($o as $i=>$oo)
	{
		if(!$cols)
			$cols=(int)(12/count($oo));
		$out .= "<div class='row tbl'><div class='col-sm-".$cols."'>" . join("</div><div class='col-sm-".$cols."'>",$oo) . "</div></div>";

	}
	return $out;
}

/**
 * �������������� ����/�������
 * @params $d {string} ���� � ������� datetime - 0000-00-00 00:00:00
 * @return {string} ������ ��.��.���� ��:��
 */


function format_datetime($d)
{
	$a = split(" ",$d);
	$b = split("-",$a[0]);
	$c = split(":",$a[1]);
	return $b[2].".".$b[1].".".$b[0]." ".$c[0].":".$c[1];
}

/**
 * �������������� ����/�������
 * @params $d {string} ���� � ������� datetime - 0000-00-00 00:00:00
 * @return {string} ������ �� <����� (�������)>, ��:��
 */

function format_datetime_short($d)
{
	$month = array("01"=>"������","02"=>"�������","03"=>"�����","04"=>"������","05"=>"���","06"=>"����","07"=>"����","08"=>"�������","09"=>"��������","10"=>"�������","11"=>"������","12"=>"�������");
	$a = split(" ",$d);
	$b = split("-",$a[0]);
	$c = split(":",$a[1]);
	return $b[2]." ".$month[$b[1]].", ".$c[0].":".$c[1];
}

/**
 * �������������� ����/�������
 * @params $d {string} ���� � ������� datetime - 0000-00-00 00:00:00
 * @return {string} ������ �� <����� (����.)>, ��:��
 */

function format_datetime_short_eng($d)
{
	$month = array("01"=>"January ","02"=>"February","03"=>"March","04"=>"April","05"=>"May","06"=>"June","07"=>"July","08"=>"August","09"=>"September","10"=>"October","11"=>"November","12"=>"December");
	$a = split(" ",$d);
	$b = split("-",$a[0]);
	$c = split(":",$a[1]);
	return $month[$b[1]]." ".$b[2].", ".$b[0].", ".$c[0].":".$c[1];
}

/**
 * �������������� ����/�������
 * @params $d {string} ���� � ������� datetime - 0000-00-00 00:00:00
 * @return {string} ������ ��.��.����
 */

function format_date($d)
{
	$a = split(" ",$d);
	$b = split("-",$a[0]);
	return $b[2].".".$b[1].".".$b[0];
}

/**
 * �������������� ����/�������
 * @params $d {string} ���� � ������� datetime - 0000-00-00 00:00:00
 * @return {string} ������ ��:��
 */

function format_time($d)
{
	$a = split(" ",$d);
	$c = split(":",$a[1]);
	return $c[0].":".$c[1];
}


/**
 * �������������� ������ � �������� �� ��������
 * @params $s {string} 
 * @return {string} 
 */


function make_pul($s)
{
	$trans=array("�"=>"a","�"=>"b","�"=>"v","�"=>"g","�"=>"d","�"=>"e","�"=>"g","�"=>"z","�"=>"e","�"=>"i","�"=>"k","�"=>"l","�"=>"m","�"=>"n","�"=>"o","�"=>"p","�"=>"r","�"=>"s","�"=>"t","�"=>"y","�"=>"f","�"=>"h","�"=>"ch","�"=>"sh","�"=>"sch","�"=>"","�"=>"","�"=>"e","�"=>"yu","�"=>"ya","�"=>"j","�"=>"c","�"=>"u");
	$str=mb_ereg_replace("[^a-zA-Z�-��-�0-9 _]"," ",$s);

	$str=mb_ereg_replace("^\s+","",$str);
	$str=mb_ereg_replace("\s+$","",$str);
	$str=mb_ereg_replace("\s+","_",$str);
	$str = ruslow($str);
	foreach ($trans as $k=>$v)
		$str = str_replace($k,$v,$str);

	return $str;
}


/**
 * ������������ ��� ������ ( ������� ��� ����� �� ������������)
 * @params $s {string} ������ � ������� /?param1=..&param2=..&param3=..
 * @params $mode {bool} ������������ �� ��������� � ������������� ����������, �� �� ���������� � $s, ��� ���
 * @return {string} 
 */


function makelink($s,$mode=0)
{

// ���������� �������-�����������, ������������ ��� ������������ ������
 
	global $types,$rooms,$categories,$places,$metro,$stations;
	global $exdir_types,$conf;	

// ������������ ����������, ������� ����� ����������� � ������
	$names = array("realty","city_id","region_id","district_id","station_id","type_id","category_id","room_id","room_ids","districts_ids","stations_ids","address","price_from","price_to","sq_from","sq_to","newbuildings","house_id","rest","rest_type","rest_section","rest_region");


	for ($i=0;$i<count($names);$i++)
		if (!preg_match("/&".$names[$i]."=/",$s) && $GLOBALS[$names[$i]]!="" && $mode)
		{
			if (is_array($GLOBALS[$names[$i]]))
			{
				foreach($GLOBALS[$names[$i]] as $ii => $vv)
					$s .= "&" . $names[$i] . "[" . $ii . "]=" . $vv;
			}
			else
				$s.="&".$names[$i]."=".$GLOBALS[$names[$i]];
		}


// ������� ��� �������������� ������

	if(preg_match("/&?newbuildings=1/",$s,$m))
	{
		$u.="/newbuildings";
		$s=preg_replace("/&?newbuildings=1/","",$s);
	}
	if(preg_match("/&?rest=1/",$s,$m))
	{
		$u.="/rest";
		$s=preg_replace("/&?rest=1/","",$s);
	}


	if(preg_match("/&?type_id=(\d+)/",$s,$m) && preg_match("/&?category_id=(\d+)/",$s,$m1))
	{
		if($m[1]>0 && $m1[1]>0)
		{
			$u.="/".make_pul($types[$m[1]]['name']."_".$categories[$m1[1]]['name2'])."_t".$m[1]."c".$m1[1];
			$type_id=$m[1];
		}
		elseif($m[1]>0)
		{
			$u.="/".make_pul($types[$m[1]]['name'])."_t".$m[1];
			$type_id=$m[1];
		}

		$s=preg_replace("/&?type_id=(\d+)/","",$s);
		$s=preg_replace("/&?category_id=(\d+)/","",$s);
	}
	elseif(preg_match("/&?type_id=(\d+)/",$s,$m))
	{
		if($m[1]>0)
		{
			$u.="/".make_pul($types[$m[1]]['name'])."_t".$m[1];
			$type_id=$m[1];
		}
		$s=preg_replace("/&?type_id=(\d+)/","",$s);
	}

	if(preg_match("/&?rest_type=(\d+)/",$s,$m))
	{
		if($m[1]>0)
		{
			$u.="/".make_pul($exdir_types[$m[1]]['name'])."_rt".$m[1];
		}
		$s=preg_replace("/&?rest_type=(\d+)/","",$s);
	}
	if(preg_match("/&?city_id=(\d+)/",$s,$m))
	{
		if($m[1]>0)
		{
			if($conf['translate'])
				$u.="/".make_pul("homes ".($type_id>0?$types[$type_id]["name"]:"")." in ".make_wordform($places[$m[1]][text_value],2))."_c".$m[1];
			else
				$u.="/".make_pul(($type_id>0?$types[$type_id]["name"]." ������������":"�����������")." � ".make_wordform($places[$m[1]][text_value],2))."_c".$m[1];
		}
		$s=preg_replace("/&?city_id=(\d+)/","",$s);
	}
	if(preg_match("/&?place_id=(\d+)/",$s,$m))
	{
		if($m[1]>0)
			$u.="/".make_pul($places[$m[1]][text_value])."_p".$m[1];
		$s=preg_replace("/&?place_id=(\d+)/","",$s);
	}
	if(preg_match("/&?room_id=(\d+)/",$s,$m))
	{
		if($m[1]>0)
			$u.="/".make_pul($rooms[$m[1]][name2])."_r".$m[1];
		$s=preg_replace("/&?room_id=(\d+)/","",$s);
	}
	if(preg_match("/&?station_id=(\d+)/",$s,$m))
	{
		if($m[1]>0)
			$u.="/".make_pul($stations[$m[1]][name])."_st".$m[1];
		$s=preg_replace("/&?station_id=(\d+)/","",$s);
	}
	if(preg_match("/&?metro_id=(\d+)/",$s,$m))
	{
		if($m[1]>0)
			$u.="/".make_pul($metro[$m[1]][name])."_m".$m[1];
		$s=preg_replace("/&?metro_id=(\d+)/","",$s);
	}
	if(preg_match("/&?house_id=(\d+)/",$s,$m))
	{
		if(preg_match("/&?house_name=([^&]+)/",$s,$m1))
		{
			if($m[1]>0)
				$u.="/".make_pul($m1[1])."_h".$m[1];
			$s=preg_replace("/&?house_id=(\d+)/","",$s);
			$s=preg_replace("/&?house_name=([^&]+)/","",$s);
		}
	}
	if(preg_match("/&?rest_id=(\d+)/",$s,$m))
	{
		if(preg_match("/&?rest_name=([^&]+)/",$s,$m1))
		{
			if($m[1]>0)
				$u.="/".make_pul($m1[1])."_rest".$m[1];
			$s=preg_replace("/&?rest_id=(\d+)/","",$s);
			$s=preg_replace("/&?rest_name=([^&]+)/","",$s);
		}
	}

	$s=preg_replace("/&?[a-z0-9_]+=0/","",$s);
	$s=preg_replace("/&?[a-z0-9_]+=(&|$)/","\\1",$s);
	$s=preg_replace("/^&/","",$s);

	$u=strtolower($u);

	
	if ($s != "")
		$s = "/?".$s;
	
	return $u.$s;
}

/**
 * ������������ ���������
 * @params $start {int} ����� ��������
 * @params $rep_on_page {int} ���������� ����������/������ �� ��������
 * @params $all {int} ����� ���������� ����������/������
 * @return {string} ������ � HTML �����
 */


function makePages($start,$rep_on_page,$all)
{
	$start = ((int)($start/$rep_on_page))*$rep_on_page;
	$start_page = $start-10*$rep_on_page;
	if ($start_page<0) $start_page = 0;
	$end_page = $start+10*$rep_on_page;
	if ($end_page>$all) $end_page = $all;

	$out = "<ul class='pagination'>";

	if ($start>0) $list.="<li><a href='".makelink("start=".($start-$rep_on_page),1)."'>&lt;&lt;</a></li>";
	for ($i=$start_page;$i<$end_page;$i+=$rep_on_page)
	{
		$out .= "<li><a" . ($i==$start?" class='sel'":"") . " href='" . makelink("start=$i",1) . "'>" . (int)($i/$rep_on_page+1) . "</a></li>";
	}
	if ($start+$rep_on_page<$all) $out .= "<li><a href='".makelink("start=".($start+$rep_on_page),1)."'>&gt;&gt;</a></li>";

	$out .= "</ul>";

	return $out;
}

/**
 * ������ � ���� ������ (mysql)
 * @params $q {string} ������ � ���� ������ mysql
 * @params $new_db {string} �������� ���� ������ mysql
 * @return {resource}
 */

function mysql_query_c($q,$dbname)
{
	GLOBAL $db,$db_db;
	

	if (!$db)
	{
		$db = mysql_connect("host","user","pwd") or die("Can't connect");
		mysql_select_db($new_db,$dbname) or die("Can't select db $dbname");
		$db_db = $dbname;
	}

	if ($dbname != $db_db)
	{
		mysql_select_db($dbname,$db);
		$db_db = $dbname;
	}


	$res = mysql_query($q,$db);

	return $res;
}

/**
 * ������ � ���� ������ (mysqli)
 * @params $q {string} ������ � ���� ������ mysql
 * @params $new_db {string} �������� ���� ������ mysql
 * @return {resource}
 */


function mysqli_query_c($q,$dbname)
{
	GLOBAL $db,$db_db;

	if (!$db)
	{
		$db = mysqli_connect("host","user","pwd") or die("Can't connect");
		mysqli_select_db($db,$dbname) or die("Can't select db $dbname");
		$db_db = $dbname;
	}

	if ($dbname != $db_db)
	{
		mysqli_select_db($db,$dbname) or die("Can't select db $dbname");
		$db_db = $dbname;
	}

	$res = @mysqli_query($db,$query);
	
	return $res;
}


/**
 * ������������ ������ ���������� ��� ����� �� ������������
 * @params $rw {array} 
 * @return {string}
 */


function printFullItem($rw)
{
	global $places,$rooms,$stations,$types,$categories,$metro,$conf;
	global $title,$kw,$description,$navbar,$h1;


	$rw[date_print] = format_datetime_short($rw[date]);

// ������������ ����������, ��������, �������� ����

	$title = $types[$rw[type]][name] . " ". ($rw[room_id]>0 && in_array($rw[category],array(1,16))?$rooms[$rw[room_id]]['name3']:$categories[$rw[category]][name2]) . "," . $rw['address'];
	$h1=$types[$rw[type]][name] . " ". ($rw[room_id]>0 && in_array($rw[category],array(1,16))?$rooms[$rw[room_id]]['name3']:$categories[$rw[category]][name2])." � ".print_place_for_h1($rw[place_id]);
	$h2_map=($rw[room_id]>0 && in_array($rw[category],array(1,16))?$rooms[$rw[room_id]]['name2']:$categories[$rw[category]][name2])." � ".print_place_for_h1($rw[place_id])." �� �����";

	$kw=$types[$rw[type]][name] . " ". $categories[$rw[category]][name2] .", ".$types[$rw[type]][name] . " ". $categories[$rw[category]][name2] .  " � " . getRegionCase($places[$rw[city]]['text_value'],2).", ".$types[$rw[type]][name2] . " ". $categories[$rw[category]][name3] .", ".$types[$rw[type]][name2] . " ". $categories[$rw[category]][name3] .  " � " . getRegionCase($places[$rw[city]]['text_value'],2).",";
	$kw1=", ������������ � " . getRegionCase($places[$rw[city]]['text_value'],2).",";

	if ($rw[station_id])
	{
		$kw.=", ".$types[$rw[type]][name2]." ".$categories[$rw[category]][name2]." � ������� ".$stations[$rw[station_id]][name].",";
		$kw1.=", ������������ � ������� ".$stations[$rw[station_id]][name].",";
	}

	if ($rw[metro_id])
	{
		$kw.=", ".$types[$rw[type]][name2]." ".$categories[$rw[category]][name2]." ����� ".$metro[$rw[metro_id]][name].",";
		$kw1.=", ������������ ����� ".$metro[$rw[metro_id]][name].",";
	}

	$description="���������� �".$rw[id]." - ".$title;
	$kw.=", ".$kw1;


// ������������ ������ ����������
	if ($rw[price])
	{
		$h1 .= " �� " .number_format($rw[price], 0, ',', ' ') . " " . $rw[price_type];
		$description .= " �� " . number_format($rw[price], 0, ',', ' ') . " " . $rw[price_type];
		$realty_price=number_format($rw[price], 0, ',', ' ') . " " . $rw[price_type];
		if($rw[price_per_m])
			$realty_price.="<small>".number_format($rw[price_per_m], 0, ',', ' ')." ".$rw[price_type]." �� �<sup>2</sup></small>";
	}

	if($rw['room_id'])
	{
		$obj_info.=$rooms[$rw['room_id']]['name2'];
	}
	else
	{
		$obj_info.=$categories[$rw['category']][name];
	}
	if($rw['house_id']>0)
	{
		$obj_info.=" � ".print_nb_link($rw['house_id']);
	}



	$realty_params = "";
	$realty_text = "";
	$ar = split("::",$rw[all_info]);
	foreach($ar as $str)
	{
		$arr = preg_split("/(:==|==)/",$str);
		if (preg_match("/�������/",$arr[0]) && !preg_match("/(�<sup>2</sup>|��\.\s*�)/",$arr[1]))  $arr[1].=" �<sup>2</sup>";
		if (!preg_match("/��������|�������|���������|������������ �����������/",$arr[0])) $realty_params .= "<tr><td class='pph' >$arr[0]</td><td class='pp'>$arr[1]</td></tr>";
		if (preg_match("/��������|�������|���������/",$arr[0])) $realty_text = $arr[1];
		if (preg_match("/������������ �����������|�������/",$arr[0])) $realty_transport = "<div class='realty_transport'>".$arr[1]."</div>";		
	}


	$tmp_contacts = "";

	if ($rw2 = get_agency($rw[agency]))
	{
		$tmp_contacts = "
			<tr><td colspan=2 class='agency-name'><span itemprop='name'>$rw2[title]</span></td></tr>
			" . ($rw2[person]?"<tr><td class='pph' >���</td><td class='pp'><span itemprop='employee' itemscope itemtype='http://schema.org/Person'><span itemprop='name'>$rw2[person]</span></span></td></tr>":"") . "
			" . ($rw2[address]?"<tr><td class='pph' >�����</td><td class='pp'><span itemprop='address'>$rw2[address]</span></td></tr>":"<meta itemprop='address' content='-'>") . "
			" . ($rw2[phones]?"<tr><td class='pph' >�������</td><td class='pp'><span itemprop='telephone'>$rw2[phones]</span></td></tr>":"") . "
		";

		$tmp_contacts = "<div itemprop='seller' itemscope itemtype='http://schema.org/Organization'>
				<table class='params' style='width:100%;'>$tmp_contacts</table></div>";
	}

	$obj_link = "<a href='".makelink("type_id=".$rw[type]."&category_id=".$rw[category]."&city_id=".$rw[city])."'>" . $types[$rw[type]][name] . " ".$categories[$rw['category']]['name2']." � ".getRegionCase($places[$rw[city]]['text_value'],2)."</a>";
	$tmp_type = "<a href='".makelink("type_id=".$rw[type]."&category_id=".$rw[category])."'>" . $types[$rw[type]][name] . " ".$categories[$rw['category']]['name2']."</a>";


// ������������ ������� ������
	
	$navbar[] = "<li><a href='/'>".ucfirst($conf['host'])."</a></li>";
	$navbar[] = "<li><a href='".makelink("type_id=".$rw[type])."'>" . $types[$rw[type]][name] . " ������������</a></li>";
	$navbar[] = "<li><a href='".makelink("type_id=".$rw[type]."&category_id=".$rw[category])."'>" . $types[$rw[type]][name] . " ".$categories[$rw['category']]['name2']."</a></li>";
	$navbar[] = "<li><a href='".makelink("type_id=".$rw[type]."&category_id=".$rw[category]."&city_id=".$rw[city])."'>" . $places[$rw[city]]['text_value'] . "</a></li>";
	

	if ($places[$rw[place_id]][name] && $rw[place_id]!=$rw[city])
	{
		$place_name=print_place_name($places[$rw[place_id]]);
		$tmp_str1 = "<li><a href='".makelink("type_id=".$rw[type]."&category_id=".$rw[category]."&city_id=".$rw[city]."&place_id".$rw[place_id])."'>". $place_name . "</a></li>";
		$pl=$places[$rw[place_id]][parent];
		while($pl!=$rw[city] && $pl>0)
		{
			$place_name=print_place_name($places[$pl]);
			$tmp_str1 = "<li><a href='".makelink("type_id=".$rw[type]."&category_id=".$rw[category]."&city_id=".$rw[city]."&place_id".$pl)."'>" . $place_name . "</a></li>".$tmp_str1;
			$pl=$places[$pl][parent];
		}
		$navbar[] = $tmp_str1;
	}   
	$navbar[] = "<li><a href='".makelink("type_id=".$rw[type]."&category_id=".$rw[category]."&city_id=".$rw[city]."&place_id=".$rw[place_id]."&room_id=".$rw[room_id])."'>" . $rooms[$rw[room_id]][name2] . "</a></li>";


// ������������ ����� � �������������

	if ($rw[img_cnt]>0)
	{
		$tmp_small_pics = "";
		if ($rw[img_cnt]>1)
		{
			for ($i = 0; $i < $rw[img_cnt]; $i++)
			{
//				$imgs[]=$rw[id]."_".$i.".jpg";
				$imgs[]=($rw[id]%100)."/".$rw[id]."/".$i.".jpg";
			}
		}
		$tmp_small_pics=print_small_images($imgs,4);

		$realty_content_img .= "
			<div class='realty_pics'>
			<div id='realty_big_img'><a name=main_photo><img src='/estate_img/$rw[id]_0.jpg' itemprop='image'></a></div>
			$tmp_small_pics	
			</div>
		";

	}    


// ������ ���� ������ ����������

	$out .= "
		<div class='item_content'>
		<ol class='breadcrumb'>".join("",$navbar)."</ol>
		<div itemscope itemtype='http://schema.org/Offer'>
			<meta itemprop='name' content='$h1'>
			<div class='row'>
				<div class='col-sm-6 obj-link'>$obj_link</div>
				<div class='col-sm-6 item-date' style='text-align:right;'>".$rw['date_print']."</div>
			</div>
			<div class='row'>
				<div class='col-sm-6'>
					<div class='item-title'>$obj_info</div>
					<div class='item-address'>
						<div itemprop='availableAtOrFrom' itemscope itemtype='http://schema.org/Place'>
							<div itemprop='name'>
								<div itemprop='address' itemscope itemtype='http://schema.org/PostalAddress'>
									<span itemprop='streetAddress' class='realty_address'>$rw[address]</span>
									<meta itemprop='telephone' content='-'>
								</div>
							</div>
							<meta itemprop='addressLocality' content='".$places[$rw[city]][text_value]."'>
						</div>
					</div>
					<div class='item-transport'>$realty_transport</div>
					<div class='item-price'> $realty_price </div>
					<div class='item-params'>
						<span class='title'>����� ����������</span>
						<table class='params'>
							<td class='pph'>��� ��������:</td><td class='pp'><span itemprop='category'>$tmp_type</span></td></tr>
							" . ($rw[station_id]?"<tr><td class='pph' >�-�. �������:</td><td class='pp'><a href='" . make_pul($stations[$rw[station_id]][name]) . "_st$rw[station_id]'>" . $stations[$rw[station_id]][name] . "</a></td></tr>":"") . "							
							" . ($rw[metro_id]?"<tr><td class='pph' >�����:</td><td class='pp'><a href='" . make_pul($metro[$rw[metro_id]][name]) . "_m$rw[metro_id]'>" . $metro[$rw[metro_id]][name] . "</a></td></tr>":"") . "							
							" . ($rw[house]?"<tr><td class='pph' >��� ����:</td><td class='pp'>$rw[house]</td></tr>":"") . "
							$realty_params
						</table>
					</div>
					<div class='item-text' itemprop='description'>$realty_text</div>
					<div class='item-contact'>$tmp_contacts</div>
				</div>
				<div class='col-sm-6'>
					$realty_content_img
					<div style='width:100%; margin: 20px 0px;'><!-- google_code --></div>
				</div>
			</div>
		";
		if ($rw[lat] && $rw[long])
		{
			if($rw[zoom]==0) $rw[zoom]=14;
			$out .= "
				<h2 class='h2_map'>$h2_map</h2>
				<script type='text/javascript'>
				    ymaps.ready(init);
				    var map,myPlacemark;

				    function init(){  		
					    map = new ymaps.Map(\"realty_map\", {
				            center: [".$rw[lat].", ".$rw[long]."], 
			        	    zoom: ".($rw[zoom]>0?$rw[zoom]:7)."
				        	});

				            myPlacemark = new ymaps.Placemark([".$rw[lat].", ".$rw[long]."], {
	                    		    hintContent: '".$types[$rw[type]]['name'] . " ".($rw[room_id]>0 && $rw[category]!=2?$rooms[$rw[room_id]]['name3']:$categories[$rw[category]][name2])."',
			                    balloonContent: '<strong>".$types[$rw[type]]['name'] . " ".($rw[room_id]>0 && $rw[category]!=2?$rooms[$rw[room_id]]['name3']:$categories[$rw[category]][name2])."</strong><br>".$rw[address]."'
				            });
	            
				            map.geoObjects.add(myPlacemark);
					}
				</script>
				<div id='realty_map' style='width:100%;height:400px;'></div>
			";
		}

		$out .= "</div>
			<h2>" . $types[$rw[type]]['name2'] . " ".$categories[$rw[category]]['name3']." � " . getRegionCase($places[$rw[city]]['text_value'],2) . "</h2>
		";

	return $out;
}


?>