#!/usr/bin/perl

$redirect_level_max=10;
$redirect_level=0;


$dbh = DBI->connect("DBI:mysql:dbname;host=host","user","pwd",{RaiseError=>1,PrintError=>1});
if (!$dbh) {print "db connect error ".$DBI::errstr; exit(0);};


#инициализация запросов к БД

$sth_insert_vac = $dbh->prepare("");
$sth_select_vac = $dbh->prepare("");

$sth_select_company = $dbh->prepare("");
$sth_select_company_alt = $dbh->prepare("");
$sth_select_company_alt1 = $dbh->prepare("");
$sth_select_company_reviews = $dbh->prepare("");
$sth_select_company_by_title = $dbh->prepare("");
$sth_insert_company = $dbh->prepare("");

$sth_insert_resume = $dbh->prepare("");
$sth_select_resume = $dbh->prepare("");


$sth_insert_review = $dbh->prepare("");
$sth_select_review = $dbh->prepare("");


$sth_select_user=$dbh->prepare("");
$sth_insert_user=$dbh->prepare("");
$sth_select_user_contact=$dbh->prepare("");
$sth_insert_user_contact=$dbh->prepare("");




%sections=();
%sections_child=();
%sections_map=();
%sections_name=();
%sec_map=();
%queue=();
%queue_level=();

# карта сопостовления локаций источника и БД, не совпадающих по названию/написанию

%cities_map=();

# ... заполнение %cities_map




# загрузка очереди
#
# @param  $source {string}  название источника
# @param  $pos {int}  номер поля в базе с ссылкой на страницы источника
# @param  $href {string} ссылка referer источника
# @param  $limit {int}  количество загружаемых страниц
# @param  $add_w {string}  дополнительные условия запроса
#

sub loadQueue 
{
	local ($source,$pos,$href,$limit,$add_w)=@_;

	$sth_select_sec = $dbh->prepare("select * from sections_sources where source='".$source."'".($add_W?" ".$add_w:"")." and map>0 order by last_access asc limit 0,".$limit);
	$sth_select_sec->execute();
	while ((@i = $sth_select_sec->fetchrow()))
	{
		print "load ".$i[$pos]." -> ".$i[7]."\n";
		if($i[$pos] ne "")
		{
			$sec_map{$i[$pos]} = $i[7];
			$queue{$i[$pos]} = $href."~!!~0~!!~$i[7]";
			$queue_level{$i[$pos]} = 0;
			$sec_ids.=($sec_ids?",":"").$i[7];
		}
		$dbh->do("update sections_sources set last_access=UNIX_TIMESTAMP(NOW()) where id=".$i[0]);
	}

	$sth_select_sec = $dbh->prepare("select * from sections_sources where source='".$source."'");
	$sth_select_sec->execute();
	while ((@i = $sth_select_sec->fetchrow()))
	{
		$sections_map{$i[0]} = $i[7];
		$sections_name{$i[0]} = $i[3];
	}

}

# загрузка компаний
#


sub loadCompany
{
	%job_company=();
	$sth_select_all = $dbh->prepare("select id,title,phone from company");
	$sth_select_all->execute();
	while ((@i = $sth_select_all->fetchrow()))
	{
		$i[1].=$i[2];
		$i[1]=getKey($i[1]);
	
		$job_company{$i[1]} = $i[0];
		if ($i[0]%1000 == 0)
		{
			print "load company ".$i[0]."\n";
		}
	}
	return %job_company;
}


# загрузка  городов
#

sub loadCities 
{
	%cities=();
	$sth_select_all = $dbh->prepare("select * from places where parent>0 order by name");
	$sth_select_all->execute();
	while ((@i = $sth_select_all->fetchrow()))
	{
		$cities{$i[2]} = $i[0];
		$i[2]=getKey($i[2]);
		$cities_key{$i[2]} = $i[0];
	}
	return %cities;
}


# загрузка разделов (профессиональные области)

sub loadSections 
{
	local ($sec_ids)=@_;
	$sth_select_sec = $dbh->prepare("select * from sections_new");
	$sth_select_sec->execute();
	while ((@i = $sth_select_sec->fetchrow()))
	{
		$sections{$i[0]} = $i[2];
		$sections_child{$i[1]} .= ($sections_child{$i[1]}?",":"").$i[0] if($i[1]>0);
		$sections_key{getKey($i[2])} = $i[1];


		if($i[1]>0) {
			$i[2]=~s/\s*\/\s*/,/ig;
			$i[2]=~tr/ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ/йцукенгшщзхъфывапролджэячсмитьбю/;
			$sections_all{$i[0]} = $i[2];
		}
		
	}
	if($sec_ids) 
	{
		$sth_select_sec = $dbh->prepare("select * from sections_new where parent in ($sec_ids)");
		$sth_select_sec->execute();
		while ((@i = $sth_select_sec->fetchrow()))
		{
			$sec_childs{$i[1]}.=($sec_childs{$i[1]}?",":"").$i[0];
			$sth_select_sec1 = $dbh->prepare("select * from sections_new where parent=$i[0]");
			$sth_select_sec1->execute();
			while ((@i1 = $sth_select_sec1->fetchrow()))
			{
				$sec_childs{$i[1]}.=($sec_childs{$i[1]}?",":"").$i1[0];
			}	
		}
	}

	%sec_ids_index=();
	if($sec_ids)
	{
		@ar=split(/,/,$sec_ids);
		foreach $a(@ar)
		{
			$sec_ids_index{$a}=1;
		}
	}

	local %sections_parent=();

	$sth_select_sec = $dbh->prepare("select * from sections_new");
	$sth_select_sec->execute();
	while ((@i = $sth_select_sec->fetchrow()))
	{
		$sections_index{$i[0]}=$i[2];
		$sections_parent{$i[0]}=$i[1];
		$sections_new{$i[2]} = $i[0] if(!$sec_ids || $sec_ids_index{$i[0]});
		$sections_key{getKey($i[2])} = $i[0]  if(!$sec_ids || $sec_ids_index{$i[0]});		
	}
	foreach $k(keys(%sections_index)) 
	{
		$parent=$sections_parent{$k};
		while($parent>0)
		{
			$sections_child_new{$parent} .= ($sections_child_new{$parent}?",":"").$k if(!$sec_ids || $sec_ids_index{$parent});
			$parent=$sections_parent{$parent};			
		}

	}

}


# проверка по тегу наличия среди детей раздела более подходящего раздела
# @param $found_sec {int} раздел, в котором ищем
# @param $c {string} тег, по которому ищем
# @return {int} уточненный раздел

sub checkSections 
{
	local ($found_sec,$c)=@_;
	$sec_id=0;
	return 0 if($c eq "");
	print "check $c\n";
	$others=0;
	

	if($found_sec>0) 
	{
		print "check sections childs $found_sec -> ".$sections_child_new{$found_sec}."\n";
		@ar=split(/,/,$sections_child_new{$found_sec});
		foreach $sec (@ar)
		{
			$s_name=$sections_index{$sec};
			print "$sec -> $s_name in $c\n";
			@m=split(/\s*\/\s*/,$s_name);
			foreach $mm(@m)  {
				if ($c=~/$mm/i)
				{
					$sec_id = $sec;				
					print "found section = $sec $s_name\n";
					return $sec_id;
				}
			}
			$others=$sec if($s_name=~/другие/);
		}
		foreach $sec (@ar)
		{
			$s_name=$sections_index{$sec};
#			print "$sec -> $c in $s_name\n";
			if ($s_name=~/$c/i)
			{
				$sec_id = $sec;				
				print "found section = $sec $s_name\n";
				return $sec_id;
			}
		}
	}
	else {
		$c_key=getKey($c);
		$sec_id = $sections_key{$c_key};
		print "key $c_key -> $sec_id\n";
		return $sec_id if($sec_id>0);

		print "check all sections childs\n";
		foreach $ch (keys(%sections_child_new))
		{
			@ar=split(/,/,$sections_child_new{$ch});
			foreach $ch (@ar)
			{
				$s_name=$section_index{$sec};
				if ($c=~/$s_name/i)
				{
					$sec_id = $sec;				
					print "found section = $sec $s_name\n";
					return $sec_id;
				}
			}
		}
	}

	if(keys %sections_tmpl)
	{
		print "check sections map\n";
		foreach $cc (keys(%sections_tmpl))
		{
			$str=$sections_tmpl{$cc};
			if ($c=~/($str)/i)
			{
				$sec_id = $cc;				
				print "found sec = $sec_id $str\n";
				return $sec_id;
			}
		}
	}

	print "set section others $others\n\n" if($others>0);
	return $others if($others>0);
	print "dont find section\n\n";
	return $found_sec;
}

# регистрация загруженного url
#
# @param $u {string} url
#


sub regUrl
{
	local($u) = @_;
	$ready{$u} = 1;
	$queue{$u}="";
	open (Q,">>$work_dir/ready.dat");
	print Q $u."\n";
	close(Q);

#	print "reg url $u<br>";

}

#  добавление записи в очередь загрузки
#
# @param $u {string} url
# @param $ref {string} referer
# @param $lev {int} часть кода для разбора
# @param $data {string} передаваемые данные
#

sub pushUrl
{
	local($u,$ref,$lev,$data) = @_;
	$data=~s/\n|\r//ig;
	$data=~s/(\s)\s+/$1/ig;
	$u = getLinkFromAction($ref,$u);
	if ($ready{$u}!=1 && $queue{$u} eq "")
	{
		print "push url $u $ref $lev $data<br>\n";
		$queue{$u} = $ref."~!!~".$lev."~!!~".$data;
		push(@urls_order,$u);
		open (Q,">>$work_dir/queue.dat");
		print Q $u."~!~".$queue{$u}."\n";
		close(Q);
		$queue_level{$u} = $lev;
	}
	else
	{
		if ($ready{$u})
		{
			print "ready\n";
		}else
		{
			print "allready pushed\n";
		}
	}
}

# подготовка url к загрузке
#
# @param $ref {string} referer
# @param $action {string} url
# @return {string}


sub getLinkFromAction
{
	local ($ref,$action) = @_;
#	print "action: '$ref' '$action'<br>\n";
	if ($action=~/^\/\//)
	{
		return "http:".$action;
	}elsif ($action!~/^http/)
	{
		$root = $ref;
		$root=~s/http:\/\///;
		$root=~s/^\/\///;
		$root=~s/\/[^\/]*$//;
		$root=~s/\/*$//;
		$root="http://".$root if ($root!~/^http/);
		local @temp = split(/\//,$root);
		local $host=$temp[0]."//".$temp[2];
#		print $host." $root<hr>";
		
		return $host.$action if ($action=~/^\//);
#		print $action."<br>";
		local $l = $root."/".$action;
		$l=~s/\/[^\/]*\/\.\.//ig;
		$l=~s/\/[^\/]*\/\.\.//ig;
		$l=~s/\/[^\/]*\/\.\.//ig;
		$l=~s/\/[^\/]*\/\.\.//ig;
		return $l;
	}
	return $action;
}

# загрузка url методом get 
#
# @param $link {string} url
# @param $ref {string} referer
# @return {string} содержимое загруженной страницы


sub get
{
	local ($link,$ref) = @_;
	$link=getLinkFromAction($ref,$link);
#	print "get url $link $ref<br>";
	local $s = GetRequest($link,"",$ref);
#	print "<hr>$s<hr>";
	print "error empty text<hr>" if ($s eq "");
#	print "output end";
	return $s;
}


# загрузка url методом post 
#
# @param $link {string} url
# @param $ref {string} referer
# @param $cookie {string} cookie
# @param $post {string} post request

# @return {string} содержимое загруженной страницы

sub post
{
	local ($link,$ref,$cookie,$post) = @_;
	$link=getLinkFromAction($ref,$link);
	print "\n=============\npost url $link ref $ref cookie $cookie post $post\n";
	local $s = PostRequest($link,$ref,$post,$cookie);
#	print "<hr>$s<hr>";
	print "error empty text<hr>" if ($s eq "");
#	print "output end";
	return $s;
}

# нахождение контрольной суммы
#
# @param $s {string} 
# @return {int} crc
#

sub get_crc
{
	local ($s) = @_;
	local @c = (0xff,0x0f,0x00,0x00);
	local $crc = 0;
	$s=~s/[ \n\r\t,.:~!\/\\()&;-]//ig;
	$s=~tr/ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮQWERTYUIOPASDFGHJKLZXCVBNM/йцукенгшщзхъфывапролджэячсмитьбюqwertyuiopasdfghjklzxcvbnm/;
	local $i;
	for ($i=0;$i<length($s);$i++)
	{
		$c[3]^=$c[2];
		$c[2]^=$c[1];
		$c[1]^=$c[0];
		$c[0]^=ord(substr($s,$i));
	}
	$crc = (($c[0]<<24) | ($c[1]<<16) | ($c[2]<<8) | $c[3]);
	return $crc;
}

# нахождение контрольной суммы вакансии
#
# @param $d {array}  параметры вакансии (ex. город, название, текстовая информация, название компании)
# @return {int} crc
#

sub get_item_crc
{
	local @d = @_;
	local $city = $d[1];
	local $target = $d[2];
	local $text = $d[3].$d[4].$d[5].$d[6];
	local $company = $d[7];
	$crc = get_crc($target.$text);
	return $crc;
}

# нахождение контрольной суммы резюме
#
# @param $d {array}  параметры вакансии (ex. город, название, текстовая информация, название компании)
# @return {int} crc
#

sub get_resume_crc
{
	local @d = @_;
	local $name = $d[0];
	local $phone = $d[1];
	local $email = $d[2];
	$crc = get_crc($name.$phone.$email);
	return $crc;
}

# нахождение контрольной суммы отзыва
#
# @param $d {array}  параметры вакансии (ex. город, название, текстовая информация, название компании)
# @return {int} crc
#

sub get_review_crc
{
	local @d = @_;
	$crc = get_crc($d[0].$d[1].$d[2]);
	return $crc;
}

# загрузка всех вакансий, уже загруженных с источника

sub loadAllVacancies
{
	print "load items $sec\n";
	return if ($loaded_vacancies);
	$sth_select_all = $dbh->prepare("");
	$sth_select_all->execute();
	while ((@i = $sth_select_all->fetchrow()))
	{
		local ($id,@d) = @i;
		$crc = get_item_crc(@d);
		$job_items_crc{$crc} = $i[0];
		if ($i[0]%1000 == 0)
		{
			print "load item ".$i[0]."\n";
			$dbh->do("select 1");
		}
		$loaded_vacancies = 1;
	}
}

#добавление данных компании
#
# @params @data {array} 
# @return {int} id компании

sub pushCompanyData
{
	local @data = @_;
	print "save company $data[0] -----\n";
	$data[0]=~s/&?(laquo|raquo|quot|apos);?/"/ig;
	return 0 if ($data[0]!~/\S/);

	local $id=0;
	$id=checkCompany(@data);
	return $id if($id>0);

	$sth_insert_company->execute(@data);
	print $sth_insert_company->errstr;

	$sth_select_id = $dbh->prepare("select LAST_INSERT_ID()");
	$sth_select_id->execute();
	local @item;
	if (@item = $sth_select_id->fetchrow())
	{
		print "new ".$item[0]."\n";
		sleep(3);
		$job_company{$key} = $item[0];
		return $item[0] if($item[0]>0);
	}

	$sth_select_company_alt->execute($data[0],$data[5]);
	local @item;
	if ((@item = $sth_select_company_alt->fetchrow()))
	{
		print "new ".$item[0]."\n";
		return $item[0];
	}

	print "!!!!!!!!!!!!!!!!!error!!!!!!!!!!!!!!!!!\n";
	return 0;
}

#проверка существования компании
#
# @params @data {array} 
# @return {int} id компании


sub checkCompany
{
	local @data = @_;
	$data[0]=~s/&?(laquo|raquo|quot|apos);?/"/ig;

	$name_alt=$data[0];
	$name_alt=~s/(ООО|ооо|зао|ЗАО|ао|АО|ЧОП|хоо|ХОО|ЧОО|чоо|ГК|ПСКФ?|СК)\s*//ige;
	$name_alt=~s/"|'//ige;
	$name_alt=~s/^\s*//ige;
	$name_alt=~s/\s*$//ige;

	return 0 if ($data[0]!~/\S/);
	local @phones=split(/[;,]/,$data[5]);
	push(@phones,$data[5]) if($data[5]=~/[;,]/);
	foreach $ph(@phones) 
	{
		$key = $data[0].$ph;
		print "check company '$key'\n";
		$key=getKey($key);
		print "company key '$key' ".$job_company{$key}."\n";
		return $job_company{$key} if ($job_company{$key} && $key!~/\S/);


		$key = $name_alt.$ph;
		print "check company alt '$key'\n";
		$key=getKey($key);
		print "company key '$key' ".$job_company{$key}."\n";
		return $job_company{$key} if ($job_company{$key} && $key!~/\S/);
	}
	foreach $ph(@phones) 
	{
		$ph=~s/^\+?[7,8]//ige;
		$ph=~s/[\(\)-\s]+/%/ig;
		$ph=~s/^%+//ige;
		$ph=~s/%+$//ige;
		print "check $name_alt,$ph\n";
		$sth_select_company_alt->execute("%".$name_alt."%","%".$ph."%");
		local @item;
		if ((@item = $sth_select_company_alt->fetchrow()))
		{
			print "exist ".$item[0]."<\n>";
			return $item[0];
		}
	}
	print "check $data[0],$data[1]\n";
	$sth_select_company_alt1->execute($data[0],$data[1]);
	local @item;
	if ((@item = $sth_select_company_alt1->fetchrow()))
	{
		print "exist ".$item[0]."\n";
		return $item[0];
	}

	print "check $name_alt,$data[1]\n";
	$sth_select_company_alt1->execute($name_alt,$data[1]);
	local @item;
	if ((@item = $sth_select_company_alt1->fetchrow()))
	{
		print "exist ".$item[0]."\n";
		return $item[0];
	}


	if($is_reviews)
	{
		print "check for reviews $data[0],$data[1]\n";
		$sth_select_company_reviews->execute($data[0],$data[1]);
		local @item;
		if ((@item = $sth_select_company_reviews->fetchrow()))
		{
			print "exist ".$item[0]."\n";
			return $item[0];
		}

		print "check for reviews $name_alt,$data[1]\n";
		$sth_select_company_reviews->execute($name_alt,$data[1]);
		local @item;
		if ((@item = $sth_select_company_reviews->fetchrow()))
		{
			print "exist ".$item[0]."\n";
			return $item[0];
		}

		if($data[1]==0)
		{
			print "check for reviews company name $data[0]\n";
			$sth_select_company_by_title->execute($data[0]);
			local @item;
			if ((@item = $sth_select_company_by_title->fetchrow()))
			{
				print "exist ".$item[0]."\n";
				return $item[0];
			}

			print "check for reviews company name $name_alt\n";
			$sth_select_company_by_title->execute($name_alt);
			local @item;
			if ((@item = $sth_select_company_by_title->fetchrow()))
			{
				print "exist ".$item[0]."\n";
				return $item[0];
			}
		}
	}

	print "!!!!!!!!!!!!!!!!!don't find!!!!!!!!!!!!!!!!!\n";
	return 0;
}


#добавление пользователя
#
# @params @data {array} 
# @return {int} id пользователя


sub pushUser 
{
	local @data=@_;
	print "save user --- @data\n";

	%user=();
	$user_id=0;
	@m=split(/\s+/,$data[0]);
	foreach $mm(@m) 
	{
		if($mm=~/(вна|вич)$/)
		{
			$user{'secondname'}=$mm;
		}
		elsif($mm=~/(ов|ова|ин|ина|ко)$/ && $mm!~/^([Ее]?[Кк]атерина|[Яя]нина|[Ии]рина)$/i && $user{'name'})
		{
			$user{'sirname'}=$mm;
		}
		else
		{
			$user{'name'}=$mm;
		}
	}

	foreach $k(keys(%user)) 
	{
		print "$k -> ".$user{$k}."\n====\n";
	}

	$sth_select_user->execute($user{'name'},$user{'sirname'}."",$user{'secondname'}."",$data[3]);
	while(@r = $sth_select_user->fetchrow())
	{
		if(!$user_id && $r[0]) 
		{
			print "check user $r[0]\n";				
			if(checkUserContact($r[0],1,$data[1]) || checkUserContact($r[0],2,$data[2]))
			{
				print "exist user $r[0]\n";
				$user_id=$r[0];
				return $user_id;
			}
		}
	}

	$sth_insert_user->execute($user{'name'},$user{'name'},$user{'sirname'}."",$user{'secondname'}."",$data[3]);
	print $sth_insert_user->errstr;
	
	
	$sth_select_user->execute($user{'name'},$user{'sirname'}."",$user{'secondname'}."",$data[3]);
	if (@r = $sth_select_user->fetchrow())
	{
		print "new user $r[0]\n";
		$user_id=$r[0];
	}

	
	if($user_id>0) 
	{
		pushUserContact($user_id,1,$data[1]) if($data[1] ne "");	
		pushUserContact($user_id,2,$data[2]) if($data[2] ne "");	
	}

	return $user_id;
}


#добавление контактной информации пользователя
#
# @params @data {array} 
# @return {int} id 

sub pushUserContact
{
	local (@data)=@_;
	print "save user contact --- @data\n";
        
	$sth_select_user_contact->execute(@data);
	if (@r = $sth_select_user_contact->fetchrow())
	{
		print "exist user contact $r[0]\n";
		return $r[0];
	}

	$sth_insert_user_contact->execute(@data);
	print $sth_insert_user_contact->errstr;


	$sth_select_user_contact->execute(@data);
	if (@r = $sth_select_user_contact->fetchrow())
	{
		print "new user contact $r[0]\n";
		return $r[0];
	}
	print "!!!!!!!!!!! error !!!!!!!!!!!\n";
	return 0;
}

#проверка на существование контактной информации у пользователя
#
# @params @data {array} 
# @return {int} id 


sub checkUserContact
{
	local (@data)=@_;
	print "check user contact --- @data\n";

	return 0 if(!$data[2]);
        
	$sth_select_user_contact->execute(@data);
	if (@rr = $sth_select_user_contact->fetchrow())
	{
		print "exist user contact @rr\n";
		return 1;
	}

	return 0;
}

#добавление вакансии
#
# @params @data {array} 
# @return {int} id вакансии


sub pushVacancy
{
	local @data = @_;

	print "save data --- $data[0]\n";

	loadAllVacancies($data[0]);

	$user_id=0;
	$company_id=0;
	if($data[13]=~/^\s*(Работодатель|\.|Торговая Компания|[Ии]ндивидуальный [Пп]редприниматель|Компания|Транспортная компания|ООО|ИП|Группа компаний|Ирина|Наталья|Елена|Агентство по подбору персонала|Крупная Компания|Ольга|Людмила|Мария|Прямой работодатель|Производственное предприятие|Дмитрий|Светлана|салон красоты|Аптечная сеть|Андрей|Строительная компания|Автосервис)\s*$/i) 
	{
		$user_id=pushUser($data[14],$data[15],$data[16],$data[1]);
		print "set user_id=$user_id\n========\n";			
	}
        else 
	{
		$company_id = pushCompanyData($data[13],$data[1],"",$data[14],$data[15],$data[16]);
	}
	
	if ($company_id>0 || $user_id>0)
	{
		
		$sss = join(" ",$data[0],$data[1],$data[2],$data[3],$data[4],$data[5],$data[6],$data[7],$data[8],$data[9]);
		print "\nget crc from \n----------------------\n$sss\n---------------\n";
		local @m = ($data[0],$data[1],$data[8],$data[9],$data[10],$data[11],$data[12],$company_id);

		$crc = get_item_crc(@m);
		$id = $job_items_crc{$crc};

		if ($id>0) 
		{
			print "exist $id\n";
			
			return $id;
		}


		$sth_select_vac->execute($data[1],$data[2],$data[3],$data[4],$data[5],$data[6],$data[7],$data[8],$data[9]);
		if (@r = $sth_select_vac->fetchrow())
		{
			$job_items_crc{$crc} = $r[0];
			print "exist item $r[0]\n";
			return $r[0];
		}



		$sth_insert_vac->execute(@data,$user_id,$company_id,$siteName,$crc,$current_url);
		print $sth_insert_vac->errstr;
		$sth_select_id = $dbh->prepare("select LAST_INSERT_ID()");
		$sth_select_id->execute();
		if (@r = $sth_select_id->fetchrow())
		{
			$job_items_crc{$crc} = $r[0];
			print "new item $r[0]\n";
			return $r[0] if($r[0]>0);
		}

		$sth_select_vac->execute($data[1],$data[2],$data[3],$data[4],$data[5],$data[6],$data[7],$data[8],$data[9]);
		if (@r = $sth_select_vac->fetchrow())
		{
			$job_items_crc{$crc} = $r[0];
			print "new item $r[0]\n";
			return $r[0];
		}

	}
	return 0;
}


# загрузка всех резюме, уже загруженных с источника

sub loadAllResume 
{
	return if ($loaded_resume);

	print "load resume\n";

	%resume_items_crc = ();
	$sth_select_all = $dbh->prepare("");
	$sth_select_all->execute();
	while ((@i = $sth_select_all->fetchrow()))
	{
		($id,@data1) = @i;
		$crc = get_resume_crc(@data1);
		$resume_items_crc{$crc} = $i[0];
		if ($i[0]%1000 == 0)
		{
			print "load resume ".$i[0]."\n";
			$dbh->do("select 1");
		}
	}
        $loaded_resume=1;
	print "resume loaded\n";

}

#добавление резюме
#
# @params @data {array} 
# @return {int} id резюме



sub pushResume
{
	local @data = @_;
	print "save resume data --- $data[0]<br>\n";

	loadAllResume();
#	print "push data\n".join("\n=======================\n",@data);
	
	print "to crc -> $data[18],$data[19],$data[20]\n";

	$crc = get_resume_crc($data[18],$data[19],$data[20]);
	print "crc $crc\n";

	$id = $resume_items_crc{$crc};
	if ($id>0) 
	{
		print "exist $id\n";
		return $id;
	}

	$sth_select_resume = $dbh->prepare("select * from resume where source_url like ?");
	$sth_select_resume->execute($current_url);
	if (@r = $sth_select_resume->fetchrow())
	{
		$resume_items_crc{$crc} = $r[0];
		print "exist $r[0]\n";
		return $r[0];
	}
	$sth_insert_resume->execute(@data,$siteName,$current_url);
	print $sth_insert_resume->errstr;
	$sth_select_resume = $dbh->prepare("select LAST_INSERT_ID()");
	$sth_select_resume->execute();
	if (@r = $sth_select_resume->fetchrow())
	{
		$resume_items_crc{$crc} = $r[0];
		print "new $r[0]\n";
		return $r[0] if($r[0]>0);
	}

	$sth_select_resume->execute($current_url);
	if (@r = $sth_select_resume->fetchrow())
	{
		$resume_items_crc{$crc} = $r[0];
		print "new $r[0]\n";
		return $r[0];
	}




	return 0;
}


#добавление всех отзывов, уже загруженных с источника

sub loadAllReviews 
{
	return if ($loaded_reviews);

	print "load reviews\n";

	%resume_items_crc = ();
	$sth_select_all = $dbh->prepare("");
	$sth_select_all->execute();
	while ((@i = $sth_select_all->fetchrow()))
	{
		($id,@data1) = @i;
		$crc = get_review_crc(@data1);
		$reviews_items_crc{$crc} = $i[0];
		if ($i[0]%1000 == 0)
		{
			print "load review ".$i[0]."\n";
			$dbh->do("select 1");
		}
	}
        $loaded_reviews=1;
	print "resume loaded\n";

}

#добавление отзыва
#
# @params @data {array} 
# @return {int} id отзыва


sub pushReview
{
	local (@data) = @_;
	print "save data --- $data[0] $data[1] $data[2]<br>";

	loadAllReviews();


	print "to crc -> $data[0],$data[1],$data[2],$data[3],$data[4]\n";

	$crc = get_review_crc($data[0],$data[1],$data[2],$data[3],$data[4]);
	print "crc $crc\n";


	$id = $reviews_items_crc{$crc};
	if ($id>0) 
	{
		print "exist $id\n";
		return $id;
	}

	$sth_select_review->execute($data[0],$data[2]);

	local @item;
	if ((@item = $sth_select_review->fetchrow()))
	{
		print "exist review ".$item[0]."<br>";
		return $item[0];
	}

	$sth_insert_review->execute(@data);
	print $sth_insert_review->errstr;
	$sth_select_review->execute($data[0],$data[2]);

	local @item;
	if ((@item = $sth_select_review->fetchrow()))
	{
		print "new review ".$item[0]."<br>";
		$reviews_items_crc{$crc} = $item[0];
		return $item[0];
	}
	print "\n\n!!!!!!!!!!!!!!!!!error!!!!!!!!!!!!!!!!!<br><hr><hr><hr><hr>\n\n";
#	exit(0);
	return 0;
}


# проверка на существование города
#
# @params $c {string} название города
# @return {int} id города

sub checkCity 
{
	local ($c)=@_;
	$c_id=0;
	return 0 if($c eq "");
	print "check city $c\n";
	
	$c=~s/ё/е/ig;
	$c_key=getKey($c);
	$c_id = $cities_key{$c_key};
	return $c_id if($c_id>0);

	$c=~s/(область|обл\.?|край|республика|респ\.?)//ige;

	print "check all cities (".keys(%cities).")\n";
	foreach $cc (keys(%cities))
	{
#		print $cc." -> ".$cities{$cc}." ";
		if ($c=~/(^|\s|,|\.)$cc(\s|,|$)/i)
#		if ($c=~/$cc/i)
		{
			$c_id = $cities{$cc};				
			print "found city = $c_id $cc\n";
			return $c_id if($c_id>1);
		}
	}

	print "check cities map\n";
	foreach $cc (keys(%cities_map))
	{
		$str=$cities_map{$cc};
		if ($c=~/($str)/i)
		{
			$c_id = $cc;				
			print "found city = $c_id $str\n";
			$params{'region'}=$c;
			return $c_id;
		}
	}

	print "dont find\n\n";
	return 0;
}

# выполнение get запроса
#
# @params $link {string} url
# @params $cookie {string} cookie
# @params $ref {string} referer
# @return {string}

sub GetRequest
{
	local ($link,$cookie, $ref) = @_;

	local @m = ("");
	local($i,$r);

	if(!$scriptName) 
	{ 
		$scriptName=$siteName;
	}

	my $req = new HTTP::Request GET => $link;

    ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday) = gmtime(time);
	@wd = ("Mon","Tue","Wed","Thu","Fri","Sun","Sat");
	@mn = ("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");

	local $t = $wd[$wday-1].", $mday ".$mn[$mon]." ".($year+1900)." ";
	$t.="0" if ($hour<10);
	$t.=$hour.":";
	$t.="0" if ($min<10);
	$t.=$min.":";
	$t.="0" if ($sec<10);
	$t.=$sec;
	$cc = $cookie;
	foreach (keys(%cookies))
	{
		$cc.=";" if ($cc ne "");
		$cc.=$_."=".$cookies{$_};
	}
	$req->header("Cookie" => $cc) if ($cc ne "");

	$host = $link;
	$host=~s/^(http|https):\/\///ig;
	$host=~s/\/.*//ig;
	$req->header('Host' => $host);
	$req->header(Referer => $ref)  if ($ref=~/\S/);
	$req->header(Date => $t." GMT");  # set current date
	$req->header(Accept => 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8');
	$req->header('Connection' => 'keep-alive');
	$req->header('Accept-Language' => 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3');
	$req->header('Cache-Control' => 'private');
	$req->header('Cache-Control' => 'max-age=0');
	$req->header('Upgrade-Insecure-Requests' => '1');
	$req->header('User-Agent' => 'Mozilla/5.0 (Windows NT 5.1; rv:51.0) Gecko/20100101 Firefox/51.0');

	$req->header('Accept-Encoding' => 'gzip, deflate');

	print "\n".$req->as_string."\n===\n";
	my $res = $ua->request($req);
	$r = $res->as_string;

	$r=~s/Set-Cookie:\s*(.*)/add_cookie($1)/ige;
	$redirect = "";
	if ($r=~/Location:\s*(.*)/i)
	{
		$redirect = $1;
		$redirect=getLinkFromAction($link,$redirect);
		print "\n\nredirect ".$redirect."\n\n";
		$redirect_level++;
		if ($redirect_level < $redirect_level_max)
		{
			$redt = GetRequest($redirect, $cookie, $ref);
		}
		$redirect_level--;
		return $redt;
	}
	@m = split(/(\n.?\n)/,$r);

	return decompress_gzip($res->content) if ($m[0]=~/Content-Encoding:\s*gzip/i);

	return $res->content;
}

# извелечение данных из zip архива
#
# @param $s {string}
# @return {string}

sub decompress_gzip
{
	local ($s) = @_;
	open(Out,">$work_dir/response.zip");
	print Out $s;
	close(Out);
	system("gunzip $work_dir/response.zip -c >$work_dir/response.out");
	open(In,"$work_dir/response.out");
	$s = "";
	while (!eof(In))
	{
		$s.=<In>;
	}
	close(In);
	return $s;

}

# добавление cookie
#
# @param $c {string}

sub add_cookie
{
	local ($c) = @_;
	$c=~s/;.*//ig;
	$c=~s/^\s*//ig;
	print "cookie ";
	local @m = split(/=/,$c);
	$cookies{$m[0]} = $m[1];
	print $m[0]."->".$m[1]."\n\n";
}

# выполнение post запроса
#
# @params $link {string} url
# @params $cookie {string} cookie
# @params $data {string} post request
# @params $ref {string} referer
# @return {string}


sub PostRequest
{
	local ($link, $ref, $data,$cookie) = @_;
	local @m=("");
	local ($i,$r);

	$host = $link;
	$host=~s/^(http|https):\/\///ig;
	$host=~s/\/.*//ig;


	my $req = new HTTP::Request POST => $link;

	$data=~s/\[/%5B/g;
	$data=~s/\]/%5D/g;
    ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday) = gmtime(time);
	@wd = ("Mon","Tue","Wed","Thu","Fri","Sun","Sat");
	@mn = ("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");

	local $t = $wd[$wday-1].", $mday ".$mn[$mon]." ".($year+1900)." ";
	$t.="0" if ($hour<10);
	$t.=$hour.":";
	$t.="0" if ($min<10);
	$t.=$min.":";
	$t.="0" if ($sec<10);
	$t.=$sec;

	$cookie = "";
	foreach (keys(%cookies))
	{
		$cookie.=";" if ($cookie ne "");
		$cookie.=$_."=".$cookies{$_};
	}

	$req->header(Cookie => $cookie) if ($cookie ne "");
	$req->header('MIME-version' => '1.0') if ($cookie=~/\S/);
	$req->header(Referer => $ref)  if ($ref=~/\S/);
	$req->header(Date => $t." GMT");  # set current date
	$req->header('Cache-Control' => 'private');
	$req->header('Host' => $host);


	$req->header(Accept => 'application/xml, text/xml, */*; q=0.01');

	$req->header('Connection' => 'keep-alive');
	$req->header('Accept-Language' => 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3');
	$req->header('Accept-Encoding' => 'gzip, deflate'); 
	$req->header('Upgrade-Insecure-Requests' => '1');
	$req->header('User-Agent' => 'Mozilla/5.0 (Windows NT 5.1; rv:51.0) Gecko/20100101 Firefox/51.0');
	$req->header('X-Requested-With' => 'XMLHttpRequest');



	$req->content_type('application/x-www-form-urlencoded');
	$req->content_length(length($data));
	$req->content($data);

	print $req->as_string;
	my $res = $ua->request($req);
	$r = $res->as_string;
#	print $r."\n";
	$r=~s/\n\r?\n\r?(.|\n)*//ig;

	$r=~s/Set-Cookie:\s*(.*)/add_cookie($1)/ige;
	$redirect = "";
	if ($r=~/\sLocation:(.*)/i)
	{
		$redirect = $1;
		$redirect=~s/^\s*//ige;
		$redirect=getLinkFromAction($ref,$redirect);
		print "\n=======================\nredirect ".$redirect."\n\n";
		$redirect_level++;
		if ($redirect_level < $redirect_level_max)
		{
			$last_redirect_link=$redirect;
			$redt = GetRequest($redirect, $cookie, $ref);
		}
		$redirect_level--;
		return $redt;
	}

	@m = split(/(\n.?\n)/,$r);

	return decompress_gzip($res->content) if ($m[0]=~/Content-Encoding:\s*gzip/i);


	return $res->content;
}

# установка proxy

# @param $url {string} тестовый url 
# @param $text {string} тестовая строка

sub change_proxy
{
	local ($url,$test)=@_;
	$ex = 0;
	$check_proxy=1;

	$dbh2 = DBI->connect("DBI:mysql:dbname;host=host","user","pwd",{RaiseError=>0,PrintError=>1});
	if (!$dbh2) {print "db connect error ".$DBI::errstr; exit(0);};

	$sth = $dbh2->prepare("");
	$sth->execute();
	while ((@r = $sth->fetchrow()) && !$ex)
	{
		
		$proxy_id = $r[0];
		$proxy = $r[1].":".$r[2];
	
		$dbh->do("select 1");
		$dbh2->do("select 1");

		print "|http://".$proxy."|\n";

		$ua->proxy(['http'],"http://".$proxy."/");
	
		if (($s = get($url)) ne "" && length($s)>300 && $s=~/$test/)
		{
			print "ok \n".substr($s,0,300);
			$ex = 1;
		}else
		{
			print "bad -> ".substr($s,0,300)."\n";
		}
	}

}


# корректрировка ошибок, возникающих при смене кодировки
# @param $t {string}
# @return {string}



sub correct
{
	local ($t)=@_;

	$ss = chr(226).chr(132).chr(150);	
	$t=~s/$ss/"№"/ige;
	$ss = chr(226).chr(150).chr(170);	
	$t=~s/$ss/"-"/ige;
	$ss = chr(226).chr(128).chr(162);
	$t=~s/$ss/"-"/ige;
	$ss = chr(226).chr(128).chr(154);
	$t=~s/$ss/";"/ige;
	$ss = chr(226).chr(128).chr(148);
	$t=~s/$ss/"-"/ige;
	$ss = chr(226).chr(128).chr(147);
	$t=~s/$ss/"-"/ige;
	$ss = chr(226).chr(128).chr(145);
	$t=~s/$ss/"-"/ige;
	$ss = chr(226).chr(128).chr(156);
	$t=~s/$ss/"\""/ige;
	$ss = chr(226).chr(128).chr(157);
	$t=~s/$ss/"\""/ige;
	$ss = chr(226).chr(128).chr(166);
	$t=~s/$ss/"..."/ige;
	$ss = chr(226).chr(128).chr(175);	
	$t=~s/$ss//ige;
	$ss = chr(195).chr(151);
	$t=~s/$ss/"*"/ige;
	$ss = chr(194).chr(171);
	$t=~s/$ss/"\""/ige;
	$ss = chr(194).chr(187);
	$t=~s/$ss/"\""/ige;
	$ss = chr(194).chr(160);
	$t=~s/$ss/" "/ige;
	$ss = chr(209).chr(130);
	$t=~s/$ss/"т"/ige;
	$ss = chr(209).chr(131);
	$t=~s/$ss/"у"/ige;

	return $t;
}

# исправление графы Образование под внутренние стандарты
# @param $edu {string}
# @return {string}


sub parseEdu 
{
	local ($edu)=@_;

	@edu_enum=("Не имеет значения","Неполное среднее","Среднее","Средне-специальное","Неполное высшее","Высшее","Высшее техническое","Высшее гуманитарное","Высшее медицинское","Высшее юридическое");

	%edu_tr=();
	$edu_tr{'Без спец. подготовки|Любое|Не важно|Не имеет значения'}="Не имеет значения";
	$edu_tr{'[Нн]еполное среднее'}="Неполное среднее";
	$edu_tr{'Средне-специальное|Не ниже средне-специального|средне-специальное|Среднее профессиональное|Среднее специальное|среднее-специальное|Среднее специальное|среднеспециальное'}="Средне-специальное";
	$edu_tr{'Неполное высшее|неоконч\. высшее|Неоконченное высшее|неполное высшее|[Сс]тудент|Неполное высшее'}="Неполное высшее";
	$edu_tr{'Высшее финансовое|Высшее музыкальное|Высшее художественное|Высшее экономическое|Высшее гуманитарное'}="Высшее гуманитарное";
	$edu_tr{'Высшее строительное|Высшее техническое'}="Высшее техническое";

	%edu_tr1=();

	$edu_tr1{'среднее|Среднее общее|Средние учебные заведения|Учащийся|Среднее'}="Среднее";
	$edu_tr1{'[Вв]ысшее|Высшие учебные заведения|Послевузовское'}="Высшее";
	
	$list=join("|",@edu_enum);

	$edu_out="";
	print "\n=======\n";

	if($edu=~/^($list)$/)
	{
		$edu_out=$1;
	}
	else
	{
		foreach $k(keys(%edu_tr))
		{	
			if($edu=~/($k)/i && $edu_out eq "")
			{
				$edu_out=$edu_tr{$k};
				break;
			}
		}
	}
	if($edu_out eq "")
	{
		foreach $k(keys(%edu_tr1))
		{	
			if($edu=~/($k)/i  && $edu_out eq "")
			{
				$edu_out=$edu_tr1{$k};
				break;
			}
		}
	}
	print $edu." -> ".$edu_out."\n";
	return $edu_out;
}

# формирование ключа для поиска
# @param $c {string}
# @return {string}


sub getKey
{
	local ($c)=@_;
	$c=~s/&nbsp;//ige;
	$c=~tr/ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮQWERTYUIOPASDFGHJKLZXCVBNM/йцукенгшщзхъфывапролджэячсмитьбюqwertyuiopasdfghjklzxcvbnm/;
	$c=~s/[^0-9a-zйцукенгшщзхъфывапролджэячсмитьбю]//ig;
	return $c;
}


# формирование строки в формате json
# @param %h {hash}
# @return {string}


sub make_json
{
	local (%h) = @_;
	local $sout = "";
	foreach $k (keys(%h))
	{
		$sout.="," if ($sout ne "");
		$sout.="\"".$k."\":\"".$h{$k}."\"";
	}
	return "{".$sout."}" if ($sout ne "");
	return "";
}

# декодирует любую %## кодировку в данной строке
# @param $s {string}
# @return {string}

sub urldecode
{
	local ($l) = @_;
	$l=~s/\+/ /ig;
	$l=~s/%([0-9a-fA-F][0-9a-fA-F])/pack("c",hex($1))/ige;
	return $l;
}

# кодирует строку в %## кодировку
# @param $s {string}
# @return {string}


sub urlencode
{
	local ($s) = @_;
	@hex= ("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f");
	$s=~s/([^a-zA-Z0-9_-])/"%".$hex[ord($1)>>4].$hex[ord($1)%16]/ige;
	return $s;
}


