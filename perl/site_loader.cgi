#!/usr/bin/perl

# парсер для загрузки вакансий, резюме и отзывов о работодателях

select(STDOUT);
$|=1;#autoflush mode on
$MAX_LOAD = 10000; #максимальное количество загруженных страниц

$work_dir = ""; #корневая папка

#запрет повторного запуска парсера
{
	system("/bin/ps axuw > $work_dir/loader.ps");
	open(PS,"$work_dir/loader.ps");
	flock(PS,$LOCK_EX);
	local $s="";
	while (!eof(PS))
	{
		$s.=<PS>;
	}
	flock(PS,$LOCK_UN);
	close(PS);
	local $count = 0;
	$s=~s/\/site_loader\.cgi//i;
	$s=~s/\/site_loader\.cgi//i;
	exit(0) if ($s=~/\/site_loader\.cgi/i);
}


require("$work_dir/utf8tbl.cgi");
require("$work_dir/func.cgi");



use LWP::UserAgent;
use URI::_generic;
use HTTP::Cookies;
use DBI;
use POSIX;

$ua = new LWP::UserAgent;
$ua->agent("Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)");
$ua->timeout(30);

#формирование стартовой очереди для загрузки
$siteName='sitename';
loadQueue($siteName,5,'Referer',20);
loadSections();

#списка уже загруженных страниц
open (In,"$work_dir/ready.dat");
while (!eof(In))
{
	$s = <In>;
	$s=~s/\n|\r//ig;
	$ready{$s} = 1;
}
close(In);

#формирование очереди загрузки

open (In,"$work_dir/queue.dat");
while (!eof(In))
{
	$s = <In>;
	$s=~s/[\n\r]+//ig;
	@m = split("~!~",$s);
	if ($ready{$m[0]}!=1)
	{
		$queue{$m[0]} = $m[1];
		@n = split(/~!!~/,$m[1]);
		$queue_level{$m[0]} = $n[1];
	}
}
close(In);
@urls_order = sort {$queue_level{$b} <=> $queue_level{$a}} keys(%queue_level);
print "data readed $work_dir/loader.conf<hr>";

# загрузка кода для парсинга конкретного источника
$s = "";
open (In,"$work_dir/loader.conf");
while (!eof(In))
{
	$s.=<In>;
}
close(In);
for ($i=0;$i<10;$i++)
{
	$conf_codes{$i} = $1 if ($s=~/\[$i part\]((.|\n)*)\[!$i part\]/i);
}


#загрузка справочник уже существующих компаний и городов
%job_items_crc=();
%job_company=loadCompany();
%cities=loadCities();


# обработка очереди

$iterations = 0;
foreach $current_url (@urls_order)
{
	if ($queue{$current_url} ne "" && $ready{$current_url}!=1)
	{
		print "|".$current_url."\n";
		($current_ref,$current_level,$current_data) = split(/~!!~/,$queue{$current_url});
		$current_level=~s/\n|\r//ig;
		print "$current_ref $current_level $current_data\n==========\n";
		print "empty code $current_level" if ($conf_codes{$current_level}!~/\S/);
		eval($conf_codes{$current_level});
		$queue{$current_url} = "";
		$ready{$current_url} = 1;
		exit(0) if ($iterations>$MAX_LOAD);
		@urls_order = sort {$queue_level{$b} <=> $queue_level{$a}} keys(%queue_level);
		sleep(5);
	$iterations++;
	}
}

#обновление информации об уже загруженных страницах

%ex = ();
open (In,"$work_dir/ready.new");
while (!eof(In))
{
	$s = <In>;
	$s=~s/\n|\r//ig;
	$ex{$s} = 1;
}
close(In);


open (In,"$work_dir/ready.dat");
open (Out,">>$work_dir/ready.new");
while (!eof(In))
{
	$s = <In>;
	$s=~s/\n|\r//ig;
	print Out $s."\n" if ($s=~/fis=\d+/i && !$ex{$s});
}
close(In);
close(Out);

unlink ("$work_dir/ready.dat");
system("cp $work_dir/ready.new $work_dir/ready.dat");
unlink ("$work_dir/ready.dat");

# освобождение очереди

unlink("$work_dir/queue.dat");


