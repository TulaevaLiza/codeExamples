$utf8_conv[208][145]='�';
$utf8_conv[208][185]='�';
$utf8_conv[208][134]='�';
$utf8_conv[208][131]='�';
$utf8_conv[208][186]='�';
$utf8_conv[208][181]='�';
$utf8_conv[208][189]='�';
$utf8_conv[208][179]='�';
$utf8_conv[208][136]='�';
$utf8_conv[208][137]='�';
$utf8_conv[208][183]='�';
$utf8_conv[208][133]='�';
$utf8_conv[208][138]='�';
$utf8_conv[208][132]='�';
$utf8_conv[208][139]='�';
$utf8_conv[208][178]='�';
$utf8_conv[208][176]='�';
$utf8_conv[208][191]='�';
$utf8_conv[208][128]='�';
$utf8_conv[208][190]='�';
$utf8_conv[208][187]='�';
$utf8_conv[208][180]='�';
$utf8_conv[208][182]='�';
$utf8_conv[208][141]='�';
$utf8_conv[208][143]='�';
$utf8_conv[208][135]='�';
$utf8_conv[208][129]='�';
$utf8_conv[208][188]='�';
$utf8_conv[208][184]='�';
$utf8_conv[208][130]='�';
$utf8_conv[208][140]='�';
$utf8_conv[208][177]='�';
$utf8_conv[208][142]='�';
$utf8_conv[208][153]='�';
$utf8_conv[208][166]='�';
$utf8_conv[208][163]='�';
$utf8_conv[208][154]='�';
$utf8_conv[208][149]='�';
$utf8_conv[208][157]='�';
$utf8_conv[208][147]='�';
$utf8_conv[208][168]='�';
$utf8_conv[208][169]='�';
$utf8_conv[208][151]='�';
$utf8_conv[208][165]='�';
$utf8_conv[208][170]='�';
$utf8_conv[208][164]='�';
$utf8_conv[208][171]='�';
$utf8_conv[208][146]='�';
$utf8_conv[208][144]='�';
$utf8_conv[208][159]='�';
$utf8_conv[208][160]='�';
$utf8_conv[208][158]='�';
$utf8_conv[208][155]='�';
$utf8_conv[208][148]='�';
$utf8_conv[208][150]='�';
$utf8_conv[208][173]='�';
$utf8_conv[208][175]='�';
$utf8_conv[208][167]='�';
$utf8_conv[208][161]='�';
$utf8_conv[208][156]='�';
$utf8_conv[208][152]='�';
$utf8_conv[208][162]='�';
$utf8_conv[208][172]='�';
$utf8_conv[208][145]='�';
$utf8_conv[208][174]='�';


$utf8_conv[209][145]='�';
$utf8_conv[209][185]='�';
$utf8_conv[209][134]='�';
$utf8_conv[209][131]='�';
$utf8_conv[209][186]='�';
$utf8_conv[209][181]='�';
$utf8_conv[209][189]='�';
$utf8_conv[209][179]='�';
$utf8_conv[209][136]='�';
$utf8_conv[209][137]='�';
$utf8_conv[209][183]='�';
$utf8_conv[209][133]='�';
$utf8_conv[209][138]='�';
$utf8_conv[209][132]='�';
$utf8_conv[209][139]='�';
$utf8_conv[209][178]='�';
$utf8_conv[209][176]='�';
$utf8_conv[209][191]='�';
$utf8_conv[209][128]='�';
$utf8_conv[209][190]='�';
$utf8_conv[209][187]='�';
$utf8_conv[209][180]='�';
$utf8_conv[209][182]='�';
$utf8_conv[209][141]='�';
$utf8_conv[209][143]='�';
$utf8_conv[209][135]='�';
$utf8_conv[209][129]='�';
$utf8_conv[209][188]='�';
$utf8_conv[209][184]='�';
$utf8_conv[209][130]='�';
$utf8_conv[209][140]='�';
$utf8_conv[209][177]='�';
$utf8_conv[209][142]='�';
$utf8_conv[209][153]='�';
$utf8_conv[209][166]='�';
$utf8_conv[209][163]='�';
$utf8_conv[209][154]='�';
$utf8_conv[209][149]='�';
$utf8_conv[209][157]='�';
$utf8_conv[209][147]='�';
$utf8_conv[209][168]='�';
$utf8_conv[209][169]='�';
$utf8_conv[209][151]='�';
$utf8_conv[209][165]='�';
$utf8_conv[209][170]='�';
$utf8_conv[209][164]='�';
$utf8_conv[209][171]='�';
$utf8_conv[209][146]='�';
$utf8_conv[209][144]='�';
$utf8_conv[209][159]='�';
$utf8_conv[209][160]='�';
$utf8_conv[209][158]='�';
$utf8_conv[209][155]='�';
$utf8_conv[209][148]='�';
$utf8_conv[209][150]='�';
$utf8_conv[209][173]='�';
$utf8_conv[209][175]='�';
$utf8_conv[209][167]='�';
$utf8_conv[209][161]='�';
$utf8_conv[209][156]='�';
$utf8_conv[209][152]='�';
$utf8_conv[209][162]='�';
$utf8_conv[209][172]='�';
$utf8_conv[209][145]='�';
$utf8_conv[209][174]='�';
$utf8_conv[226][148]='-';
$utf8_conv[226][162]='-';
$utf8_conv[194][160]=' ';





sub convert_utf
{
	local ($s) = @_;
	local $sss = chr(226).chr(128);
	$s=~s/($sss(.))/rp($1,$2)/ige;


	$s=~s/([���](.))/rp($1,$2)/ige;
	return $s;
}
sub convert_utf16
{
	local ($s) = @_;
	$s=~s/((\\u[a-f0-9][a-f0-9][a-f0-9][a-f0-9])+)/convert_utf16_chars($1)/ige;
	return $s;
}
sub convert_utf16_chars
{
	local ($ss) = @_;
#	print "in ".$ss."\n";
	$ss=~s/\\u([a-f0-9][a-f0-9])([a-f0-9][a-f0-9])/chr(hex($1)).chr(hex($2))/ige; 
	
	from_to($ss, 'UTF-16be', 'windows-1251');

#	print "out ".$ss."\n";
#	exit(0);
	return $ss;
}

sub rp
{
	local ($s,$t) = @_;
#	print ord($s)." ".ord($t)."->".$utf8_conv[ord($s)][ord($t)]."\n";
	if ($utf8_conv[ord($s)][ord($t)] ne "") {return $utf8_conv[ord($s)][ord($t)];}
	return $s;

}

