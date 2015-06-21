#!/usr/local/bin/perl

# =========================================================================
#
#                  /////apeboard+ Ver.1.04 (Shift_JIS)/////
#
#                      Copyright (C) 2001,by 2apes.com
#                           All rights reserved
#                    Script written by Taishi Yokoyama
#                     web site : http://www.2apes.com
#                         mail : support@2apes.com
#
# =========================================================================

# 必要なファイルのパス指定 ------------------------------------------------

require './jcode.pl';
require './boardini.cgi';
require './skinini.cgi';

# 設定終了 ----------------------------------------------------------------

# -------------------------------------------------------------------------
# 基本処理
# -------------------------------------------------------------------------

# フォームデータの処理 ------------------------------------------

if ($ENV{'REQUEST_METHOD'} eq "POST") {
	read(STDIN, $query, $ENV{'CONTENT_LENGTH'}); 
} else {
	$query= $ENV{'QUERY_STRING'};
}

@assocarray = split(/&/, $query);

foreach (@assocarray) {
	($property, $value) = split(/=/);
	
	$value =~ tr/+/ /;
	$value =~ s/%([\dA-Fa-f][\dA-Fa-f])/pack("C", hex($1))/eg;
	
	$value =~ s/\r\n/\r/g;
	$value =~ s/\n/\r/g;
	$value =~ s/ \r \r//g;
	$value =~ s/\　\r\　\r//g;
	$value =~ s/ \r/\r/g;
	$value =~ s/\　\r/\r/g;
	$value =~ s/\r\r\r\r//g;

	$value =~ s/&/&amp;/g;
	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;
	$value =~ s/,/\0/g;
	
	if ($tagset eq 'off') {
		$value =~ s/"/&quot;/g;
	}

# jcode.pl による文字コードの変換 -------------------------------
	
	&jcode'convert(*value,'sjis');
	&jcode'h2z_sjis(*value);

# ハッシュに格納 ------------------------------------------------

	if ($property eq 'target'){
		push(@RM,$value);
	} else {
	$FORMDATA{$property} = $value;
	}
}

# 変数に割当て --------------------------------------------------

&get_cookie($cookiename);
$ck_name = $cookie{'name'};
$ck_mail = $cookie{'mail'};
$ck_url  = $cookie{'url'};
$ck_pwd  = $cookie{'pwd'};
$ck_icon = $cookie{'icon'};

$name       = $FORMDATA{'name'};
$mail       = $FORMDATA{'mail'};
$url        = $FORMDATA{'url'};
$pwd        = $FORMDATA{'pwd'};
$icon       = $FORMDATA{'icon'};
$subject    = $FORMDATA{'subject'};
$message    = $FORMDATA{'message'};
$msgnum     = $FORMDATA{'msgnum'};
$command    = $FORMDATA{'command'};
$use_cookie = $FORMDATA{'use_cookie'};
$tgtid      = $FORMDATA{'target'};

$master_pwd = $FORMDATA{'mpwd'};

# ---------------------------------------------------------------

if ($url eq 'http://'){
	$url = '';
}

if ($msgnum eq ''){
	$msgnum = 0;
}

$message =~ s/\r/<br>/g;

# タグの使用不可の場合（URL にリンクをはる） --------------------

if ($tagset eq 'off') {
	if ($autolink ne '') {
		$message =~ s/(s?https?:\/\/[-_.!~*'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)/<a href="$1" target="_blank">$autolink<\/a>/ig;
	} else {
		$message =~ s/(s?https?:\/\/[-_.!~*'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)/<a href="$1" target="_blank">$1<\/a>/ig;
	}
}

# タグの使用可の場合の各処理 ------------------------------------

if ($tagset eq 'on') {

	$message =~ s/(&lt;[^&]*)<br>([^&]*&gt;)/$1$2/gi;
	
	if ($tagimg eq 'on') {
		$message =~ s/(&lt;(img([^&]+))&gt;)/<img$3>/gi;
	}

	$message .= "</a>" x (
		($message =~ s/(&lt;(a href=([^&]+))&gt;)/<a href=$3>/gi)
		- ($message =~ s/&lt;\/a&gt;/<\/a>/gi)
	);
	
	if ($tagfnt eq 'on') {
		$message .= "</font>" x (
			($message =~ s/(&lt;(font([^&]*))&gt;)/<font$3>/gi)
			- ($message =~ s/&lt;\/font&gt;/<\/font>/gi)
		);
	}
	
	$message .= "</b>" x (
		($message =~ s/&lt;b&gt;/<b>/gi)
		- ($message =~ s/&lt;\/b&gt;/<\/b>/gi)
	);
	
	$message .= "</i>" x (
		($message =~ s/&lt;i&gt;/<i>/gi)
		- ($message =~ s/&lt;\/i&gt;/<\/i>/gi)
	);
	
	$message =~ s/("[^ "<>]+)>/$1">/gi;
}

# 処理の分岐 ----------------------------------------------------

if ($command eq 'read'){
	&read_message;
} elsif ($command eq 'write'){
	&write_message;
	&read_message;
} elsif ($command eq 'remove'){
	&remove_message;
	&read_message;
} elsif ($command eq 'setpwd'){
	&set_mtpassword;
	&read_message;
} elsif ($command eq 'viewres'){
	&show_res;
} elsif ($command eq 'reswrite'){
	&write_res;
	&read_message;
} else {
	&read_message;
}
exit(0);

# -------------------------------------------------------------------------
# 通常部分の表示用サブルーチン
# -------------------------------------------------------------------------

sub read_message {

# PROXY からのアクセスを制限 ------------------------------------

	if($pcheck ne ''){
		$proc = &chkproxy;
		if($proc == 2 && $plevel >= 1){
			&print_error("あなたのホストは投稿制限の対象となっています。");
		}
		if($proc == 1){
			if($plevel == 2){
				&print_error("あなたのホストは投稿制限の対象となっています。");
			}
		}
	}

# 特定ホストからのアクセスを制限 --------------------------------

	if ($deny_host ne ''){
		@denyhost = split(/\,/,$deniedhost);
		foreach (@denyhost) {
			if ($ENV{'REMOTE_HOST'} =~ /$_/){
				$match=1; last;
			}
		}
		if ($match){
			&print_error("あなたのホスト $ENV{'REMOTE_HOST'} は投稿制限の対象となっています。");
		}
	}

# 特定IPからのアクセスを制限 ------------------------------------

	if ($deny_IP ne ''){
		@denyip = split(/\,/,$deniedip);
		foreach (@denyip) {
			if ($ENV{'REMOTE_ADDR'} =~ /$_/){
				$match=1; last;
			}
		}
		if ($match){
			&print_error("あなたのIPアドレス $ENV{'REMOTE_ADDR'} は投稿制限の対象となっています。");
		}
	}

# データファイルを読み込む --------------------------------------

	&lock_open(TXT, "+<$datafile");
	@txt = <TXT>;
	&unlock_close(TXT);

	($encoded_pass) = splice(@txt, 0, 1);
	chop($encoded_pass);

	if ($encoded_pass eq '') {
		&show_setpwd;
	}

# データの数を調べる --------------------------------------------

	$volume = scalar(@txt);

# 表示範囲の設定 ------------------------------------------------

	$msgstart = $msgnum;

	if ($msgstart < 0) {
		$msgstart = 0;
	}

	$msgend = $msgnum + $data_out;

	if ($msgend > $volume) {
		$msgend = $volume;
	}

# 画面に表示する前の設定 ----------------------------------------


	if (($command eq 'write' || $command eq 'reswrite') && $use_cookie eq 'on') {
		undef %cookie;
		$cookie{'name'} = $name;
		$cookie{'mail'} = $mail;
		$cookie{'url'}  = $url;
		$cookie{'pwd'}  = $pwd;
		$cookie{'icon'} = $icon;

		&print_cookie($cookiename, $cookieday);

		$ck_name = $name;
		$ck_mail = $mail;
		$ck_url  = $url;
		$ck_pwd  = $pwd;
		$ck_icon = $icon;
	}

	if ($ck_url eq '') {
		$ck_url = 'http://';
	}

	print "Content-type: text/html; charset=Shift_JIS\n\n";
	
# apeskin ファイルを開く ----------------------------------------

	open(APES, $apeskin_html) || &print_error("$apeskin_htmlが開けません。");
	$apeskin = join('',<APES>);
	close(APES) || die "can't close $apeskin_html: $!\n";
	
# apeskin ファイルを切り分ける ----------------------------------

	($head_html,$mainhtml,$fot_html) = split(/<!--cut-->/, $apeskin);
	

	if ($mainhtml =~ m/<!--resstart-->(.*)<!--resend-->/si) {
		$reshtml = $1;
	}
#	$mainhtml =~ s/[\n\r\t]//ig;
	$mainhtml =~ s/<!--resstart-->.*<!--resend-->/<!--res-->/si;
	

# ヘッダ部分の作成と変換 ----------------------------------------

	$head_html =~ s/(name="name")/$1 value="$ck_name"/i;
	$head_html =~ s/(name="mail")/$1 value="$ck_mail"/i;
	$head_html =~ s/(name="url")/$1 value="$ck_url"/i;
	$head_html =~ s/(name="pwd")/$1 value="$ck_pwd"/i;
	$head_html =~ s/(a href="back_url")/a href="$back_url"/i;
	$head_html =~ s/(option value="$ck_icon")/$1 selected/i;
	
	print $head_html;

# 投稿の表示 ----------------------------------------------------

	for ($i = $msgstart; $i < $msgend; $i++) {
#		@article = split(/,/, $txt[$i]);

		($dispid,$dispname,$dispicon,$dispmail,$dispurl,$dispdate,$disppwd,$dispsubject,$dispmsg,$disphost,$dispres) = split(/,/, $txt[$i]);
		
		$dispname =~ s/\0/,/g;
		$dispicon =~ s/\0/,/g;
		$dispmail =~ s/\0/,/g;
		$dispurl =~ s/\0/,/g;
		$disppwd =~ s/\0/,/g;
		$dispsubject =~ s/\0/,/g;
		$dispmsg =~ s/\0/,/g;
		$disphost=~ s/\0/,/g;
		$dispres =~ s/\0/,/g;
		chomp($dispres);
		
		$dat_tmp = $dateline;
		($d_year,$d_mon,$d_day,$d_weekstr,$d_hour,$d_min) = split(/&/, $dispdate);
				
		if ($addzero_md eq 'on') {
			if ($d_mon < 10) {
				$d_mon = "0$d_mon";
			}
			if ($d_day <10) {
				$d_day = "0$d_day";
			}
		}
	
		if($addzero_hm eq 'on') {
			if ($d_hour < 10) {
				$d_hour = "0$d_hour";
			}
			if ($d_min < 10) {
				$d_min = "0$d_min";
			}
		}

		$dat_tmp =~ s/year/$d_year/i;
		$dat_tmp =~ s/month/$d_mon/i;
		$dat_tmp =~ s/day/$d_day/i;
		$dat_tmp =~ s/week/$d_weekstr/i;
		$dat_tmp =~ s/hour/$d_hour/i;
		$dat_tmp =~ s/minute/$d_min/i;

# リンク部分の作成 ----------------------------------------------

		&mk_mainlink;

# メイン部分の作成と文字列の変換（親部分）-----------------------

		$maintmp = $mainhtml;
		$maintmp =~ s/(name="target")/$1 value="$dispid"/i;
		$maintmp =~ s/idnum<!--s-->/$dispid/i;
		$maintmp =~ s/name<!--s-->/$dispname/i;
		$maintmp =~ s/url<!--s-->/$dispurl/i;
		$maintmp =~ s/icon<!--s-->/<img src="$icon_path$dispicon\.$icon_format" width="$icon_width" height="$icon_height" alt="$dispicon" border="0">/i;
		$maintmp =~ s/subject<!--s-->/$dispsubject/i;
		$maintmp =~ s/message<!--s-->/$dispmsg/i;
		$maintmp =~ s/date<!--s-->/$dat_tmp/i;
		$maintmp =~ s/mail<!--s-->/$dispmail/i;
		$maintmp =~ s/(a href="resinput")/a href="$thisurl?command=viewres&target=$dispid"/i;

# レス部分表示の準備 --------------------------------------------

		if ($dispres ne '' and $maintmp =~ /<!--res-->/i) {
		
			$all_res = '';
			@part_res = split(/:&:/, $dispres);
			$res_volume = scalar(@part_res);

# レス部分の表示 ------------------------------------------------

			for ($j = 0; $j < $res_volume; $j++) {
#				@res_article = split(/<>/, $part_res[$i]);

				($dresnum,$dresname,$dresicon,$dresmail,$dresurl,$dresdate,$drespwd,$dressubject,$dresmsg,) = split(/<>/, $part_res[$j]);

				$res_dat_tmp = $dateline;
				($dres_year,$dres_mon,$dres_day,$dres_weekstr,$dres_hour,$dres_min) = split(/&/, $dresdate);
				
				if ($addzero_md eq 'on') {
					if ($dres_mon < 10) {
						$dres_mon = "0$dres_mon";
					}
					if ($dres_day <10) {
						$dres_day = "0$dres_day";
					}
				}
	
				if($addzero_hm eq 'on') {
					if ($dres_hour < 10) {
						$dres_hour = "0$dres_hour";
					}
					if ($dres_min < 10) {
						$dres_min = "0$dres_min";
					}
				}
				
				$res_dat_tmp =~ s/year/$dres_year/i;
				$res_dat_tmp =~ s/month/$dres_mon/i;
				$res_dat_tmp =~ s/day/$dres_day/i;
				$res_dat_tmp =~ s/week/$dres_weekstr/i;
				$res_dat_tmp =~ s/hour/$dres_hour/i;
				$res_dat_tmp =~ s/minute/$dres_min/i;


# リンク部分の作成 ----------------------------------------------

				&res_mk_mainlink;

# メイン部分の作成と文字列の変換（子部分） ----------------------

				$restmp = $reshtml;
				$restmp =~ s/(name="target")/$1 value="$dresnum"/i;
				$restmp =~ s/resname<!--s-->/$dresname/i;
				$restmp =~ s/resurl<!--s-->/$dresurl/i;
				$restmp =~ s/resicon<!--s-->/<img src="$icon_path$dresicon\.$icon_format" width="$icon_width" height="$icon_height" alt="$dresicon" border="0">/i;
				$restmp =~ s/ressubject<!--s-->/$dressubject/i;
				$restmp =~ s/resmessage<!--s-->/$dresmsg/i;
				$restmp =~ s/resdate<!--s-->/$res_dat_tmp/i;
				$restmp =~ s/resmail<!--s-->/$dresmail/i;

				$all_res .= $restmp;
			}
			$maintmp =~ s/<!--res-->/$all_res/i;
		} 

		print $maintmp;
	}

# フッタ部分の作成と文字列の変換 --------------------------------

	$nextmsg = $msgend;

	if ($data_out + $msgnum + 1 > $volume) {
		$fot_html =~ s/<a href="back"[\d\w\s]*>(.+)<\/a>/$1/i;
		$fot_html =~ s/(name="pwd")/$1 value="$ck_pwd"/i;
		$fot_html =~ s/(a href="top")/a href="$thisurl"/i;
		$fot_html =~ s/(a href="back_url")/a href="$back_url"/i;
 
		print $fot_html;
	} else {
		$fot_html =~ s/(name="pwd")/$1 value="$ck_pwd"/i;
		$fot_html =~ s/(a href="back")/a href="$thisurl?command=read_message&msgnum=$nextmsg"/i;
		$fot_html =~ s/(a href="top")/a href="$thisurl"/i;
		$fot_html =~ s/(a href="back_url")/a href="$back_url"/i;
 
		print $fot_html;
	}

	exit(0);

}

# -------------------------------------------------------------------------
# レス投稿ページの表示用サブルーチン
# -------------------------------------------------------------------------

sub show_res {

# データファイルを読み込み対象となるメッセージを探す ------------

	&lock_open(TXT, "+<$datafile");
	@txt = <TXT>;
	&unlock_close(TXT);

	($encoded_pass) = splice(@txt, 0, 1);
	chop($encoded_pass);
	$tgtid = $RM[0];
	$index = &find_msg;

	if ($index < 0) {
		&unlock_close(TXT);
		&print_error("そのメッセージは存在しません。");
	}

# 画面に表示する前の設定 ----------------------------------------

	print "Content-type: text/html; charset=Shift_JIS\n";
		
	if ($ck_url eq '') {
		$ck_url = 'http://';
	}
	
	print "\n";

# 投稿の表示 ----------------------------------------------------

	($dispid,$dispname,$dispicon,$dispmail,$dispurl,$dispdate,$disppwd,$dispsubject,$dispmsg,$disphost,$dispres) = split(/,/, $txt[$index]);

	$dispname =~ s/\0/,/g;
	$dispicon =~ s/\0/,/g;
	$dispmail =~ s/\0/,/g;
	$dispurl =~ s/\0/,/g;
	$disppwd =~ s/\0/,/g;
	$dispsubject =~ s/\0/,/g;
	$dispmsg =~ s/\0/,/g;
	$disphost=~ s/\0/,/g;
	$dispres =~ s/\0/,/g;
	chomp($dispres);

	$dat_tmp = $dateline;
	($d_year,$d_mon,$d_day,$d_weekstr,$d_hour,$d_min) = split(/&/, $dispdate);

	if ($addzero_md eq 'on') {
		if ($d_mon < 10) {
			$d_mon = "0$d_mon";
		}
		if ($d_day <10) {
			$d_day = "0$d_day";
		}
	}
	
	if($addzero_hm eq 'on') {
		if ($d_hour < 10) {
			$d_hour = "0$d_hour";
		}
		if ($d_min < 10) {
			$d_min = "0$d_min";
		}
	}
	
	$dat_tmp =~ s/year/$d_year/i;
	$dat_tmp =~ s/month/$d_mon/i;
	$dat_tmp =~ s/day/$d_day/i;
	$dat_tmp =~ s/week/$d_weekstr/i;
	$dat_tmp =~ s/hour/$d_hour/i;
	$dat_tmp =~ s/minute/$d_min/i;
		

# レスファイルを開く --------------------------------------------

	open(APRS, $res_file) || &print_error("$res_fileが開けません。");
	$resfile = join('',<APRS>);
	close(APRS) || die "can't close $res_file: $!\n";
	
# apeskin ファイルを切り分ける ----------------------------------

	($res_head_html,$res_mainhtml,$res_fot_html) = split(/<!--cut-->/, $resfile);
	
	if ($res_mainhtml =~ m/<!--resstart-->(.*)<!--resend-->/si) {
		$res_reshtml="$1";
	}
	
	$res_mainhtml =~ s/<!--resstart-->.*<!--resend-->/<!--res-->/si;
	
# ヘッダ部分の作成と変換 ----------------------------------------

	$res_head_html =~ s/(name="name")/$1 value="$ck_name"/i;
	$res_head_html =~ s/(name="mail")/$1 value="$ck_mail"/i;
	$res_head_html =~ s/(name="url")/$1 value="$ck_url"/i;
	$res_head_html =~ s/(name="pwd")/$1 value="$ck_pwd"/i;
	$res_head_html =~ s/command="write"/command="reswrite"/i;
	$res_head_html =~ s/(option value="$ck_icon")/$1 selected/i;

	$res_head_html =~ s/<input type="hidden" name="command".+>/<input type="hidden" name="command" value="reswrite">\n<input type="hidden" name="target" value="$dispid">/i;
	
	print	$res_head_html;

# リンク部分の作成 ----------------------------------------------

	&mk_mainlink;

# メイン部分の作成と文字列の変換（親部分）-----------------------

	$res_mainhtml =~ s/name<!--s-->/$dispname/i;
	$res_mainhtml =~ s/idnum<!--s-->/$dispid/i;
	$res_mainhtml =~ s/url<!--s-->/$dispurl/i;
	$res_mainhtml =~ s/icon<!--s-->/<img src="$icon_path$dispicon\.$icon_format" width="$icon_width" height="$icon_height" alt="$dispicon" border="0">/i;
	$res_mainhtml =~ s/subject<!--s-->/$dispsubject/i;
	$res_mainhtml =~ s/message<!--s-->/$dispmsg/i;
	$res_mainhtml =~ s/date<!--s-->/$dat_tmp/i;
	$res_mainhtml =~ s/mail<!--s-->/$dispmail/i;
	$res_mainhtml =~ s/<a href="resinput">(.+)<\/a>/$1/i;

# レス部分表示の準備 --------------------------------------------
	if ($dispres ne '') {
		$res_all_res = '';
		@part_res = split(/:&:/, $dispres);
		$res_volume = scalar(@part_res);

# レス部分の表示 ------------------------------------------------

		for ($i = 0; $i < $res_volume; $i++) {
#		@res_article = split(/<>/, $part_res[$i]);
		
			($dresnum,$dresname,$dresicon,$dresmail,$dresurl,$dresdate,$drespwd,$dressubject,$dresmsg,$dreshost) = split(/<>/, $part_res[$i]);

			$res_dat_tmp = $dateline;
			($dres_year,$dres_mon,$dres_day,$dres_weekstr,$dres_hour,$dres_min) = split(/&/, $dresdate);
	
			if ($addzero_md eq 'on') {
				if ($dres_mon < 10) {
					$dres_mon = "0$dres_mon";
				}
				if ($dres_day <10) {
					$dres_day = "0$dres_day";
				}
			}
	
			if($addzero_hm eq 'on') {
				if ($dres_hour < 10) {
					$dres_hour = "0$dres_hour";
				}
				if ($dres_min < 10) {
					$dres_min = "0$dres_min";
				}
			}
			
			$res_dat_tmp =~ s/year/$dres_year/i;
			$res_dat_tmp =~ s/month/$dres_mon/i;
			$res_dat_tmp =~ s/day/$dres_day/i;
			$res_dat_tmp =~ s/week/$dres_weekstr/i;
			$res_dat_tmp =~ s/hour/$dres_hour/i;
			$res_dat_tmp =~ s/minute/$dres_min/i;

# リンク部分の作成 ----------------------------------------------

			&res_mk_mainlink;

# メイン部分の作成と文字列の変換（子部分） ----------------------

			$res_restmp = $res_reshtml;
			$res_restmp =~ s/resname<!--s-->/$dresname/i;
			$res_restmp =~ s/resurl<!--s-->/$dresurl/i;
			$res_restmp =~ s/resicon<!--s-->/<img src="$icon_path$dresicon\.$icon_format" width="$icon_width" height="$icon_height" alt="$dresicon" border="0">/i;
			$res_restmp =~ s/ressubject<!--s-->/$dressubject/i;
			$res_restmp =~ s/resmessage<!--s-->/$dresmsg/i;
			$res_restmp =~ s/resdate<!--s-->/$res_dat_tmp/i;
			$res_restmp =~ s/resmail<!--s-->/$dresmail/i;
			
			$res_all_res .= $res_restmp;
		}
	}
	$res_mainhtml =~ s/<!--res-->/$res_all_res/i;

	print $res_mainhtml;

# フッタ部分の作成と文字列の変換 --------------------------------
	
	$res_fot_html =~ s/<a href="back"[\d\w\s]*>(.+)<\/a>//i;
	$res_fot_html =~ s/<a href="top"[\d\w\s]*>(.+)<\/a>//i;
	
	print $res_fot_html;

	exit(0);

}

# -------------------------------------------------------------------------
# 通常の記録用サブルーチン
# -------------------------------------------------------------------------
sub write_message {

# 書き込み元のチェック ------------------------------------------

	if ($fromsite ne ''){
		&check_fromsite;
	}

# 入力事項のチェック --------------------------------------------

	&check_input;

# データファイルを読み込む --------------------------------------

	&lock_open(TXT, "+<$datafile");
	@txt = <TXT>;
	$encoded_pass = splice(@txt, 0, 1);
	chop($encoded_pass);
	seek(TXT, 0, 0);
	print TXT "$encoded_pass\n";

# 二重投稿のチェック --------------------------------------------

	for ($i = 0; $i < 5; $i++) {
		($dispid,$dispname,$dispicon,$dispmail,$dispurl,$dispdate,$disppwd,$dispsubject,$dispmsg,$disphost,$dispres) = split(/,/, $txt[$i]);
		if ($dispmsg eq $message) {
		&unlock_close(TXT);
		&print_error("同じ内容で書き込もうとしています。戻ってチェックしてみて下さい。");
		}
	}

# 日付の取得 ----------------------------------------------------

	$datestr = &get_date_string;

# メールで送信 --------------------------------------------------

	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($host eq $addr) { $host = gethostbyaddr(pack('C4',split(/\./,$host)),2) || $addr; }
	if ($host eq  "") { $host =  $addr; }

	if ($smail != '0'){
		&sd_mail("$FORMDATA{'subject'}");
	}

# 記事番号の設定 ------------------------------------------------

	$id = 1;
	for ($i = 0; $i < @txt; $i++) {
		($thisid) = split(/,/, $txt[$i]);
		if ($thisid >= $id) {
			$id = $thisid + 1;
		}
	}

# 書き込む情報の整列 --------------------------------------------

	if ($must_pwd eq ''){
		if ($pwd eq ''){
			$encpwd = $encoded_pass;
		} else {
			$encpwd = &encode_pwd($pwd);
		}
	} else {
		$encpwd = &encode_pwd($pwd);
	}
	
	$oneline = "$id,$name,$icon,$mail,$url,$datestr,$encpwd,$subject,$message,$host,\n";
	unshift(@txt, $oneline);
	splice(@txt, $max_data);
	print TXT @txt;
	truncate(TXT, tell(TXT));
	
	&unlock_close(TXT);

}

# -------------------------------------------------------------------------
# レス部分の記録用サブルーチン
# -------------------------------------------------------------------------
sub write_res {

# 書き込み元のチェック ------------------------------------------

	if ($fromsite ne ''){
		&check_fromsite;
	}

# 入力事項のチェック --------------------------------------------

	&check_input;

# データファイルを読み込む --------------------------------------

	&lock_open(TXT, "+<$datafile");
	@txt = <TXT>;
	$encoded_pass = splice(@txt, 0, 1);
	chop($encoded_pass);
	$tgtid = $RM[0];
	$index = &find_msg;

	if ($index < 0) {
		&unlock_close(TXT);
		&print_error("そのメッセージは存在しません。");
	}

	($dispid,$dispname,$dispicon,$dispmail,$dispurl,$dispdate,$disppwd,$dispsubject,$dispmsg,$disphost,$dispres) = split(/,/, $txt[$index]);

	chomp($dispres);
#	splice(@txt, $index, 1);
#	seek(TXT, 0, 0);
#	print TXT "$encoded_pass\n";

	@part_res = split(/:&:/, $dispres);

# 二重投稿のチェック --------------------------------------------

	for ($i = 0; $i < 5; $i++) {
		($dresnum,$dresname,$dresicon,$dresmail,$dresurl,$dresdate,$drespwd,$dressubject,$dresmsg,$dreshost) = split(/<>/, $part_res[$i]);
		if ($dresmsg eq $message) {
		&unlock_close(TXT);
		&print_error("同じ内容で書き込もうとしています。戻ってチェックしてみて下さい。");
		}
	}

# 日付の取得 ----------------------------------------------------

	$datestr = &get_date_string;

# メールで送信 --------------------------------------------------

	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($host eq $addr) { $host = gethostbyaddr(pack('C4',split(/\./,$host)),2) || $addr; }
	if ($host eq  "") { $host =  $addr; }

	if ($smail == '2'){
		&sd_mail("Re:$dispsubject");
	}

# 記事番号の設定 ------------------------------------------------

	$id = 1;
	for ($i = 0; $i < @part_res; $i++) {
		($thisid) = split(/<>/, $part_res[$i]);
		($pnum,$cnum) = split(/_/,$thisid);
		if ($cnum >= $id) {
			$id = $cnum + 1;
		}
	}

	$id = "$dispid" . '_' . "$id";
# 書き込む情報の整列 --------------------------------------------

	if ($must_pwd eq ''){
		if ($pwd eq ''){
			$encpwd = $encoded_pass;
		} else {
			$encpwd = &encode_pwd($pwd);
		}
	} else {
		$encpwd = &encode_pwd($pwd);
	}

	$oneline = "$dispid,$dispname,$dispicon,$dispmail,$dispurl,$dispdate,$disppwd,$dispsubject,$dispmsg,$disphost,$dispres$id<>$name<>$icon<>$mail<>$url<>$datestr<>$encpwd<>$subject<>$message<>$host:&:\n";
	
	if ($res_sort eq 'on'){
		splice(@txt, $index, 1);
		seek(TXT, 0, 0);
		print TXT "$encoded_pass\n";
		unshift(@txt, $oneline);
	} else {
		splice(@txt, $index, 1, $oneline);
		seek(TXT, 0, 0);
		print TXT "$encoded_pass\n";
	}
	
	print TXT @txt;
	
	&unlock_close(TXT);

}

# -------------------------------------------------------------------------
# メッセージを削除するサブルーチン
# -------------------------------------------------------------------------
sub remove_message {

	if (!@RM) {
		&print_error('メッセージが指定されていません。');
	}
	
	&lock_open(TXT, "+<$datafile");
		@txt = <TXT>;
		($encoded_pass) = splice(@txt, 0, 1);
		chop($encoded_pass);
		
	@tmp = @RM;
	foreach $tgtid(@tmp){

		if ($tgtid =~ m/\d+_\d+/) {
			($pnum,$cnum) = split (/_/, $tgtid);
			$tgtid = $pnum;
		}
		$index = &find_msg;
		if ($index < 0) {
			&unlock_close(TXT);
			&print_error("そのメッセージは存在しません。");
		}

		($dispid,$dispname,$dispicon,$dispmail,$dispurl,$dispdate,$disppwd,$dispsubject,$dispmsg,$disphost,$dispres) = split(/,/, $txt[$index]);
	
		if ($cnum) {
			$tgtrsid = "$tgtid" . '_' ."$cnum";
			chomp($dispres);
			@part_res = split(/:&:/, $dispres);

			for ($i = 0; $i < @part_res; $i++) {
				($dresnum,$dresname,$dresicon,$dresmail,$dresurl,$dresdate,$drespwd,$dressubject,$dresmsg,$dreshost) = split(/<>/, $part_res[$i]);
				if ($tgtrsid eq $dresnum) {
					if (&mismatch_password($pwd, $drespwd) && &mismatch_password($pwd, $encoded_pass)) {
						&unlock_close(TXT);
						&print_error("パスワードが不適切で削除できません");
					}
					splice(@part_res, $i, 1);
					$dispres = join(':&:',@part_res);
					$oneline = "$dispid,$dispname,$dispicon,$dispmail,$dispurl,$dispdate,$disppwd,$dispsubject,$dispmsg,$disphost,$dispres:&:\n";
					$oneline =~ s/,:&:/,/i;
					splice(@txt, $index, 1, $oneline);
					last;
				}
			}
		} else {
			if (&mismatch_password($pwd, $disppwd) && &mismatch_password($pwd, $encoded_pass)) {
				&unlock_close(TXT);
				&print_error("パスワードが不適切で削除できません");
			}
			splice(@txt, $index, 1);
		}
	}
		unshift(@txt, ("$encoded_pass\n"));
		seek(TXT, 0, 0);
		print TXT @txt;
		truncate(TXT, tell(TXT));
		&unlock_close(TXT);
		
}

# -------------------------------------------------------------------------
# 入力事項をチェックするサブルーチン
# -------------------------------------------------------------------------

sub check_input {

	if ($must_name ne '' && $name eq '') {
		if ($miss) {
			$miss .= 'と名前';
		} else {
			$miss .= '名前';
		}
	}

	if ($must_mail ne '' && $mail eq '') {
		if ($miss) {
			$miss .= 'とメールアドレス';
		} else {
			$miss .= 'メールアドレス';
		}
	}

	if ($message eq '') {
		if ($miss) {
			$miss .= 'とコメント';
		} else {
			$miss .= 'コメント';
		}
	}

	if ($miss) {
		&print_error("$missが入力されていません。");
	}

	if ($must_mail ne '' && $mail !~ /.+\@.+\..+/) {
		&print_error('メールアドレスが不正です。');
	}
	
#--------------------------------------------------------------------------
#メールのチェックを厳しくしたい場合は以下を有効にして、上のチェックを無効に
#--------------------------------------------------------------------------
#	if ($mail ne '' && $mail !~ /.+\@.+\..+/) {
#		&print_error('メールアドレスが不正です。');
#	}
#--------------------------------------------------------------------------

	if ($maxlength > 0) {
		if (length($message) > $maxlength) {
			&print_error('書き込みが長すぎます。');
		}
	}
	
	if ($must_pwd ne ''){
		if ($pwd eq '' || length($pwd) < 4) {
		&print_error('パスワードが入力されていないか、短すぎます。');
		}
	}

}

# -------------------------------------------------------------------------
# メイン部分を表示する際にリンクを作成するサブルーチン（親部分）
# -------------------------------------------------------------------------
sub mk_mainlink {

	#メールアドレスにリンクをはる___________________________
	if ($dispmail ne '' && $mail_link ne ''){
		$dispmail = "<a href=\"mailto:$dispmail\">$dispmail</A>";
	}
	
#名前にメールアドレスのリンクをはる_____________________
	if ($dispmail ne '' && $name_link ne ''){
		$dispname = "<a href=\"mailto:$dispmail\">$dispname</A>";
	}

#画像にメールアドレスのリンクをはる_____________________
	if ($dispmail ne '' && $image_mail ne ''){
		$dispmail = "<a href=\"mailto:$dispmail\">" . $mail_image01 . '</A>';
	} elsif ($dispmail eq '' && $image_mail ne ''){
		$dispmail = $mail_image02;
	}
		
#URLにリンクをはる______________________________________
	if ($dispurl ne '' && $url_link ne ''){
		$dispurl = "<a href=\"$dispurl\" target=\"_blank\">$dispurl</A>";
	}

#画像にURLのリンクをはる________________________________
	if ($dispurl ne '' && $image_url ne ''){
		$dispurl = "<a href=\"$dispurl\" target=\"_blank\">" . $url_image01 . '</A>';
	} elsif ($dispurl eq '' && $image_url ne ''){
		$dispurl = $url_image02;
	}
	
}

# -------------------------------------------------------------------------
# メイン部分を表示する際にリンクを作成するサブルーチン（子部分）
# -------------------------------------------------------------------------
sub res_mk_mainlink {

	#メールアドレスにリンクをはる___________________________
	if ($dresmail ne '' && $res_mail_link ne ''){
		$dresmail = "<a href=\"mailto:$dresmail\">$dresmail</a>";
	}
	
#名前にメールアドレスのリンクをはる_____________________
	if ($dresmail ne '' && $res_name_link ne ''){
		$dresname = "<a href=\"mailto:$dresmail\">$dresname</a>";
	}

#画像にメールアドレスのリンクをはる_____________________
	if ($dresmail ne '' && $res_image_mail ne ''){
		$dresmail = "<a href=\"mailto:$dresmail\">" . $res_mail_image01 . '</a>';
	} elsif ($dresmail eq '' && $res_image_mail ne ''){
		$dresmail = $res_mail_image02;
	}
		
#URLにリンクをはる______________________________________
	if ($dresurl ne '' && $res_url_link ne ''){
		$dresurl = "<a href=\"$dresurl\" target=\"_blank\">$dresurl</a>";
	}

#画像にURLのリンクをはる________________________________
	if ($dresurl ne '' && $res_image_url ne ''){
		$dresurl = "<a href=\"$dresurl\" target=\"_blank\">" . $res_url_image01 . '</a>';
	} elsif ($dresurl eq '' && $res_image_url ne ''){
		$dresurl = $res_url_image02;
	}
	
}

# -------------------------------------------------------------------------
# 書込み元チェックのサブルーチン
# -------------------------------------------------------------------------

sub check_fromsite {

	$ref = $ENV{'HTTP_REFERER'};
	$ref =~ s/\?.*//;
	@frmsite = split(/\,/,$site);
	foreach (@frmsite) {
		if (!($ref =~ /$_/)){
			&print_error("外部からの書き込みはできません");
		}
	}

}

# -------------------------------------------------------------------------
# メール送信のサブルーチン
# -------------------------------------------------------------------------

sub sd_mail {

	local($sbj) = @_;

	$mail_subject = "[$mail_head]$sbj";
	if ($sbj eq ''){
		$mail_subject = "[$mail_head](No Subject in original)";
	}
		
	$bf_m_mes = $FORMDATA{'message'};
	
	$bf_m_mes =~ s/&amp;/&/g;
	$bf_m_mes =~ s/&lt;/</g;
	$bf_m_mes =~ s/&gt;/>/g;
	$bf_m_mes =~ s/\0/,/g;

	$mail_msg = substr("__ $mail_head ______________________________________________________",0,70)."\n\n";
	$mail_msg .= "Title  : $FORMDATA{'subject'}\n";
	$mail_msg .= "Sender : $FORMDATA{'name'}さん\n\n";
	$mail_msg .= "$bf_m_mes\n\n";
	$mail_msg .= "__ User_Info ______________________________________________________\n";
	$mail_msg .= "Mail Address      : $FORMDATA{'mail'}\n";
	$mail_msg .= "Web site          : $FORMDATA{'url'}\n";
	$mail_msg .= "HTTP-User-Agent   : $ENV{'HTTP_USER_AGENT'}\n";
	$mail_msg .= "Remote-host       : $host\n";
	$mail_msg .= "Remote-Addr       : $ENV{'REMOTE_ADDR'}\n";
	$mail_msg .= "___________________________________________________________________\n";
	$mail_msg .= "\n";

	$mail_msg =~ s/\r/\n/g;
	&jcode'convert(*mail_subject,'jis');
	&jcode'convert(*mail_msg,'jis');

	if (!open(MAIL,"| $sendmail -t")){
		&print_error(bad_sendmail);
	}
	print MAIL "To: $admin\n";
	print MAIL "From: $mail\n";
	print MAIL "Subject: $mail_subject\n";
	print MAIL "Content-Type: text/plain\; charset=\"iso-2022-jp\"\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: apeboard(2apes.com)\n\n\n";
	print MAIL "$mail_msg";
	print MAIL "\n";
	
	close(MAIL);
	
}

# -------------------------------------------------------------------------
# 管理者用パスワード設定のサブルーチン
# -------------------------------------------------------------------------

sub set_mtpassword {

	if ($master_pwd eq '' || length($master_pwd) < 4) {
		&print_error('パスワードが入力されていないか、短すぎます。');
	}
	
	&lock_open(TXT, "+<$datafile");
	@txt = <TXT>;
	unless (@txt){
		$encmaster = &encode_pwd($master_pwd);
		seek(TXT, 0, 0);
		print TXT "$encmaster\n";
	}
	
	&unlock_close(TXT);

}

# -------------------------------------------------------------------------
# ファイルロックのサブルーチン
# -------------------------------------------------------------------------

sub lock_open {

	local(*FILE, $lk_name) = @_;
	if (!open(FILE, $lk_name)) {
		&print_error("$lk_nameがオープンできません。");
	}
	if ($lock) {
		eval("flock(FILE, 2)"); # 2=LOCK_EX
		if ($@) {
			&print_error("$@ - この環境では flock は使えません。\$uselock = 0 にしてください。");
		}
	}
	seek(FILE, 0, 0);

}

# -------------------------------------------------------------------------
# ファイルアンロックのサブルーチン
# -------------------------------------------------------------------------

sub unlock_close {

	local(*FILE) = @_;
	if ($lock) {
		eval("flock(FILE, 8)"); # 8=LOCK_UN
	}
	close(FILE);

}

# -------------------------------------------------------------------------
# 現在日時を得るサブルーチン
# -------------------------------------------------------------------------

sub get_date_string {

	local(@week) = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat");
	local($sec, $min, $hour, $day, $mon, $year, $weekday) = localtime(time);
	$year += 1900;
	$mon++;
	
# 文字列化する --------------------------------------------------

	$weekstr = $week[$weekday];
#	return "$year/$mon/$day ($weekstr) $hour:$min";
	return "$year&$mon&$day&$weekstr&$hour&$min";
}

# -------------------------------------------------------------------------
# パスワード暗号化のサブルーチン
# -------------------------------------------------------------------------

sub encode_pwd {

	local($sec, $min, $hour, $day, $mon, $year, $weekday) = localtime(time);
	local(@token) = ('0'..'9', 'A'..'Z', 'a'..'z');
	local($pass) = @_;
	local($encpass, $salt1, $salt2);
	$salt1 = $token[(time | $$) % scalar(@token)];
	$salt2 = $token[($sec + $min*60 + $hour*60*60) % scalar(@token)];
	$encpass = crypt($pass, "$salt1$salt2");
	return $encpass;

}

# -------------------------------------------------------------------------
# クッキーの有効期限設定のサブルーチン
# -------------------------------------------------------------------------

sub get_expire_date_string {

	local($days) = @_;
	local(@month) = ( "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" );
	local(@week) = ( "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat" );
	local($sec, $min, $hour, $day, $mon, $year, $weekday) = gmtime(time + $days * 24 * 60 * 60);
	local($expiredate);
	$year += 1900;
	# 文字列化する_________________________________________________
	if ($hour < 10) {
		$hour = "0$hour";
	}
	if ($min < 10) {
		$min = "0$min";
	}
	if ($sec < 10) {
		$sec = "0$sec";
	}
	$weekstr = $week[$weekday];
	$monstr = $month[$mon];
	$expiredate = "$weekstr, $day-$monstr-$year $hour:$min:$sec GMT";
	return $expiredate;

}

# -------------------------------------------------------------------------
# クッキー取得のサブルーチン
# -------------------------------------------------------------------------

sub get_cookie {

	local($cookiename) = @_;
	local($key, $value, @pairs, $pair);
	@sqpairs = split(/;\s/, $ENV{'HTTP_COOKIE'});
	foreach $sqpair (@sqpairs) {
		($sqkey, $sqvalue) = split(/=/, $sqpair);
		if ($sqkey eq $cookiename) {
			$sqvalue =~ s/:/; /g;
			$sqvalue =~ s/_/=/g;
			@pairs = split(/;\s/, $sqvalue);
			foreach $pair (@pairs) {
				($key, $value) = split(/=/, $pair);
				$value =~ tr/+/ /;
				$key   =~ s/%([A-Fa-f0-9][A-Fa-f0-9])/pack("C", hex($1))/eg;
				$value =~ s/%([A-Fa-f0-9][A-Fa-f0-9])/pack("C", hex($1))/eg;
				$cookie{$key} = $value;
			}
			last;
		}
	}

}

# -------------------------------------------------------------------------
# クッキーを作るサブルーチン
# -------------------------------------------------------------------------

sub make_cookie {

	local($cookiename) = @_;
	local(@sqcookie, $sqstr);
	local($encode) = '\%\+\;\,\=\&\_\:';
	while (($key, $value) = each %cookie) {
		$key   =~ s/([$encode])/'%'.unpack("H2", $1)/eg;
		$value =~ s/([$encode])/'%'.unpack("H2", $1)/eg;
		$key   =~ s/\s/\+/g;
		$value =~ s/\s/\+/g;
		push(@sqcookie, "${key}_${value}");
	}
	$sqstr = join(':', @sqcookie);
	return "$cookiename=$sqstr; ";

}

# -------------------------------------------------------------------------
# クッキー表示のサブルーチン
# -------------------------------------------------------------------------

sub print_cookie {

	local($cookiename, $days, $domain) = @_;
	local($cookiestr) = &make_cookie($cookiename);
	local($expdate) = &get_expire_date_string($days);
	print "Set-Cookie: $cookiestr;";
	print " expires=$expdate;";
	if ($domain) {
		print " domain=$domain;";
	}
	print "\n";

}

# -------------------------------------------------------------------------
# メッセージを探すサブルーチン
# -------------------------------------------------------------------------

sub find_msg {

	local($i, $foundindex, $dispid);
	$foundindex = -1;
	for ($i = 0; $i < @txt; $i++) {
		($dispid) = split(/,/, $txt[$i]);
		if ($tgtid == $dispid) {
			$foundindex = $i;
			last;
		}
	}
	return $foundindex;

}

# -------------------------------------------------------------------------
# パスワード照合のサブルーチン
# -------------------------------------------------------------------------

sub mismatch_password {

	local($pass, $encodedpass) = @_;
	if ($encodedpass ne crypt($pass, $encodedpass)) {
		return 1;
	} else {
		return 0;
	}

}

# -------------------------------------------------------------------------
# PROXY チェックのサブルーチン
# -------------------------------------------------------------------------

sub chkproxy {

	$pstatus = 0;
	
# PROXY 経由のアクセスかを判別 ----------------------------------

	if($ENV{'HTTP_VIA'} ne "" ){$pstatus = 2;}
	if($ENV{'HTTP_X_FORWARDED_FOR'} ne ""){$pstatus = 2;}
	if($ENV{'HTTP_FORWARDED'} ne ""){$pstatus = 2;}
	if($ENV{'HTTP_X_LOCKING'} ne ""){$pstatus = 2;}
	if($ENV{'HTTP_CACHE_INFO'} ne ""){$pstatus = 2;}
	if($ENV{'HTTP_CACHE_CONTROL'} ne ""){$pstatus = 2;}
	if($ENV{'HTTP_SP_HOST'} ne ""){$pstatus = 2;}
	if($ENV{'HTTP_FROM'} ne ""){$pstatus = 2;}
	if($ENV{'HTTP_PROXY_CONNECTION'} ne ""){$pstatus = 2;}

	if($ENV{'HTTP_USER_AGENT'} =~ /via|cache|proxy|delegate/i){$pstatus = 2;}
	if($ENV{'REMOTE_HOST'} =~ /proxy|cache|via|delegate|www|mail/i){$pstatus = 2;}

	if($pstatus == 2){

# PROXYからのアクセスなら、それが匿名であるかどうか判別 ---------

		if( $ENV{'HTTP_VIA'} =~ s/.*(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/){
			$proxyip = $ENV{'HTTP_VIA'};
			$pstatus = 1;
		}

		if( $ENV{'HTTP_X_FORWARDED_FOR'} =~ s/^(\d+)\.(\d+)\.(\d+)\.(\d+)(\D*).*/$1.$2.$3.$4/){
			$proxyip = $ENV{'HTTP_X_FORWARDED_FOR'};
			$pstatus = 1;
		}

		if( $ENV{'HTTP_FORWARDED'} =~ s/.*(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/){
			$proxyip = $ENV{'HTTP_FORWARDED'};
			$pstatus = 1;
		}

		if( $ENV{'HTTP_X_LOCKING'} =~ s/.*(\d+)\.(\d+)\.(\d+)\.(\d+).*/$1.$2.$3.$4/){
			$proxyip = $ENV{'HTTP_X_LOCKING'};
			$pstatus = 1;
		}

		if( $ENV{'HTTP_CACHE_INFO'} =~ s/.*(\d+)\.(\d+)\.(\d+)\.(\d+).*/$1.$2.$3.$4/ ){
			$proxyip = $ENV{'HTTP_CACHE_INFO'};
			$pstatus = 1;
		}

		if($pstatus == 1){
			if($proxyip=~/([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+)/){

				$pip="$1.$2.$3.$4";

# 匿名でない事を装った匿名 PROXY であるかどうかを判別 -----------
# 取り出した IP が無効な IP なら匿名 ----------------------------

				if($pip eq "127.0.0.1" || $pip eq "0.0.0.0" || $pip eq "255.255.255.255"){$pstatus = 2;}
				
# 取り出した IP とアクセスした IP が同じなら匿名 ----------------

				if($pip eq $ENV{'REMOTE_ADDR'}){$pstatus = 2;}

				if($pstatus == 1){
					$proxyaddr=(gethostbyaddr(pack('C4',$1,$2,$3,$4),2))[0];
					if($proxyaddr eq ""){$proxyaddr = $pip;}
					
# 取り出した IP も実質上 PROXY のようなら匿名 -------------------

					if($proxyaddr =~ /proxy|cache|via|delegate|www|mail/i){$pstatus = 2;}
				}

			}else{

# 正しく IP が取得できなかったので匿名 --------------------------

				$pstatus = 2;

			}
		}
	}
	return $pstatus;
}

# -------------------------------------------------------------------------
# 管理者用パスワード設定画面表示のサブルーチン
# -------------------------------------------------------------------------

sub show_setpwd {

	print "Content-type: text/html; charset=Shift_JIS\n";
	print "\n";
	print "<html>\n";
	print "<head>\n";
	print "<title>Master Password Setup</title>\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
	print "</head>\n";
	print "<body bgcolor=\"#FFFFFF\" text=\"#003366\">\n";
	print "<div align=\"center\">\n";
	print "<table width=\"90%\" height=\"90%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\n";
	print "<tr>\n";
	print "<td align=\"center\">\n";
	print "<form method=\"post\" action=\"$thisurl\">\n";
	print "<input type=\"hidden\" name=\"command\" value=\"setpwd\">\n";
	print "<h2>Master Password Setup</h2><br>\n";
	print "管理者用パスワードを設定して下さい。（英数半角 4 文字以上）<br><br>\n";
	print "<input type=\"password\" name=\"mpwd\" size=\"10\">";
	print "<input type=\"submit\" name=\"submit\" value=\"決定\">\n";
	print "</form>";
	print "</td>\n";
	print "</tr>\n";
	print "</table><br><br>\n";
	print "</div>\n";
	print "</body>\n";
	print "</html>\n";
	exit(0);

}

# -------------------------------------------------------------------------
# エラー表示のサブルーチン
# -------------------------------------------------------------------------

sub print_error {

	local($msg) = @_;
	print "Content-type: text/html; charset=Shift_JIS\n";
	print "\n";
	print "<html>\n";
	print "<head>\n";
	print "<title>$msg</title>\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
	print "</head>\n";
	print "<body bgcolor=\"#FFFFFF\" text=\"#003366\">\n";
	print "<div align=\"center\">\n";
	print "<table width=\"90%\" height=\"90%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\n";
	print "<tr>\n";
	print "<td align=\"center\">\n";
	print "<h2>$msg</h2><br>\n";
	print "再度試していただくか、";
	print "<a href=\"mailto:$admin\">$admin</a>";
	print "までお知らせください。<br><br>\n";
	print "<font color=\"#CC0000\">ブラウザのBackでお戻り下さい</font><br><br>";
	print "<a href=\"$indexurl\">Go TopPage</a>\n";
	print "</td>\n";
	print "</tr>\n";
	print "</table><br><br>\n";
	print "</div>\n";
	print "</body>\n";
	print "</html>\n";
	exit(0);

}

# End of Script
