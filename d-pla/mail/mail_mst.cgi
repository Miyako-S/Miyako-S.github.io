#!/usr/local/bin/perl

# =========================================================================
#
#            /////apeboard+ for webmaster Ver.1.05 (Shift_JIS)/////
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

&form_decord;

&get_cookie($mt_cookiename);
$ck_pwd  = $cookie{'pwd'};

$command = $FORMDATA{'command'};
$tgtid   = $FORMDATA{'target'};
$pwd     = $FORMDATA{'pwd'};
$msgnum  = $FORMDATA{'msgnum'};
$old_pwd = $FORMDATA{'old_pwd'};
$new_pwd = $FORMDATA{'new_pwd'};
$cknew_pwd=$FORMDATA{'cknew_pwd'};

if ($msgnum eq ''){
	$msgnum = 0;
}

if ($command eq 'read' || $command eq 'f_read'){
	&read_mes_res;
} elsif ($command eq 'res_mes'){
	&res_message;
	&read_mes_res;
} elsif ($command eq 'remove'){
	&remove_message;
	&read_mes_res;
} elsif ($command eq 'cg_mtpwd'){
	&shw_chpwd;
} elsif ($command eq 'cg_and_ck'){
	&check_change;
	&mt_login;
} else {
	&mt_login;
}
exit(0);

# -------------------------------------------------------------------------
# フォームデータをデコードするためのサブルーチン
# -------------------------------------------------------------------------

sub form_decord{

	local($query,@assocarray,$assoc,$property,$value);

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
}

# -------------------------------------------------------------------------
# レス用のメッセージ入力画面の表示
# -------------------------------------------------------------------------

sub read_mes_res {

# データファイルを読み込む --------------------------------------

	&lock_open(TXT, "+<$datafile");
	@txt = <TXT>;
	&unlock_close(TXT);
	
	($encoded_pass) = splice(@txt, 0, 1);
	chop($encoded_pass);
	
	if ($command ne 'f_read') {
		&get_cookie($mt_cookiename);
		$pwd  = $cookie{'pwd'};
	}
	
	if ($encoded_pass eq '' || &mismatch_password($pwd, $encoded_pass)) {
		&print_error("パスワードが不適切、もしくは正しく設定されていません。");
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

	
	if ($command eq 'f_read') {
		undef %cookie;
		$cookie{'pwd'}  = $pwd;

		&print_cookie($mt_cookiename, 1);

	}
	
	print "Content-type: text/html; charset=Shift_JIS\n\n";
	
# ヘッダ部分の作成と変換 ----------------------------------------

	print "<html>\n";
	print "<head>\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
	print "<title>For Webmaster</title>\n";
	print "</head>\n";

	print "<body>\n";
	print "<center>\n";
	print "　<br>\n";
	print "<b><font size=\"6\" face=\"Arial,Helvetica\">For Webmaster</font></b><br>\n";
	print "<form method=\"post\" action=\"$masterurl\">\n";
	print "ここは管理者用のページです。<br>管理者以外のアクセスを禁止します。<br>\n";
	print "<br>\n";
	print "<br>\n";
	print "<a href=\"$bbsurl\">管理用ページを終了し、表\示用ページに戻る。</a><br><br>\n";
	
# 投稿の表示 ----------------------------------------------------
	for ($i = $msgstart; $i < $msgend; $i++) {

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
		
# 名前にメールアドレスのリンクをはる ----------------------------

		if($dispmail ne '') {
			$dispname = '<a href="mailto:' . $dispmail . '">' . $dispname . '</a>';
		}
		
# URLにリンクをはる ---------------------------------------------

		if($dispurl ne '') {
			$dispurl = '- <a href="' . $dispurl . '" TARGET="_blank">' . Website . '</a>';
		}
		
# メイン部分の作成（親部分） ------------------------------------

		print "<table width=\"500\" border=\"0\" bgcolor=\"#FFFFFF\" cellpadding=\"5\" cellspacing=\"1\">\n";
		print "<tr>\n";
		print "<td bgcolor=\"#666666\" width=\"40\" align=\"center\" nowrap>\n";
		print "<input type=\"checkbox\" name=\"target\" value=\"$dispid\">\n";
		print "</td>\n";
		print "<td bgcolor=\"#CCCCCC\" width=\"458\">[$dispid] <b>$dispsubject　</b></td>\n";
		print "</tr>\n";
		print "<tr>\n";
		print "<td valign=\"top\" align=\"center\" bgcolor=\"#666666\" width=\"40\" nowrap><font color=\"#FFFFFF\">内容</font></td>\n";
		print "<td bgcolor=\"#CCCCCC\" width=\"458\">\n";
		print "<font size=\"2\"><font color=\"#CCOOOO\">&lt;$dat_tmp&gt;</font>[$disphost]</font> <br>\n";
		print "<b>$dispsubject</b> by $dispname $dispurl<br>\n";
		print "<p>$dispmsg</p>\n";
		print "</blockquote>\n";
		
# メイン部分の作成（子部分） ------------------

		open(RES, $res_file) || &print_error('レスファイルが開けません。');
		$reshtml = join('',<RES>);
		close(RES);
			
		@part_res = split(/:&:/, $dispres);
		$res_volume = scalar(@part_res);
			
		for ($j = 0; $j < $res_volume; $j++) {
			
			($dresnum,$dresname,$dresicon,$dresmail,$dresurl,$dresdate,$drespwd,$dressubject,$dresmsg,$dreshost) = split(/<>/, $part_res[$j]);
				
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
				
			# 名前にメールアドレスのリンクをはる ----------------------------
				
			if($dresmail ne '') {
				$dresname = '<a href="mailto:' . $dresmail . '">' . $dresname . '</a>';
			};
			
			# URLにリンクをはる ---------------------------------------------

			if($dresurl ne '') {
				$dresurl = '- <a href="' . $dresurl . '" TARGET="_blank">' . Website . '</a>';
			}
				
			print "<hr width=\"96%\">\n";
			print "　<font size=\"2\"><font color=\"#CCOOOO\">&lt;$res_dat_tmp&gt;</font>[$dreshost]<input type=\"checkbox\" name=\"target\" value=\"$dresnum\">-削除用</font> <br>\n";
			print "　<b>$dressubject</b> by $dresname $dresurl<br>\n";
			print "<blockquote>\n";
			print "<p>$dresmsg</p>\n";
			print "</blockquote>\n";
				
		}
			
		if ($reshtml =~ /ressubject<!--s-->/i){
			print "</td>\n";
			print "</tr>\n";
			print "<tr>\n";
			print "<td valign=\"top\" align=\"center\" bgcolor=\"#666666\" width=\"40\"><font color=\"#FFFFFF\">題名</font></td>\n";
			print "<td bgcolor=\"#CCCCCC\" width=\"458\">\n";
			print "<input type=\"text\" name=\"subject$dispid\" size=\"30\">\n";
		}
		print "</td>\n";
		print "</tr>\n";
		print "<tr>\n";
		print "<td valign=\"top\" align=\"center\" bgcolor=\"#666666\" width=\"40\" nowrap><font color=\"#FFFFFF\">レス</font></td>\n";
		print "<td bgcolor=\"#CCCCCC\" width=\"458\">\n";
		print "<textarea name=\"resp$dispid\" cols=\"60\" rows=\"4\"></textarea>\n";
		print "</td>\n";
		print "</tr>\n";
		print "</table><br>\n";
	}

# フッタの作成と文字列の変換 ------------------------------------

	$nextmsg = $msgend ;
	print "<table width=\"500\" border=\"0\" bgcolor=\"#666666\" cellpadding=\"5\">\n";
	print "<tr align=\"center\">\n";
	print "<td>\n";
	print "<select name=\"command\">\n";
	print "<option value=\"res_mes\" selected>レスをつける</option>\n";
	print "<option value=\"remove\">削除</option>\n";
	print "<option value=\"cg_mtpwd\">管理者用パスワード変更</option>\n";
	print "</select>\n";
	print "<input type=\"submit\" name=\"submit\" value=\"　　決　定　　\">\n";
	print "</td>\n";
	print "</tr>\n";
	print "</table>\n";
	print "</form>\n";
	print "<table width=\"500\" border=\"0\">";
	print "<tr>\n";
	print "<td><a href=\"$masterurl?command=read\"><font face=\"Arial,Helvetica\" size=\"4\"><B>&lt; TopLog</b></font></a></td>\n";
	if ($data_out + $msgnum + 1 > $volume) {
		print "<td align=\"right\"><font size=\"5\">　</font><td>\n";
	} else {
		print "<td align=\"right\"><a href=\"$masterurl?command=read&msgnum=$nextmsg\"><font face=\"Arial,Helvetica\" size=\"4\"><b>OldLog &gt;</b></font></a><td>\n";
	}
	print "</tr>\n";
	print "</table>\n";
	print "</center>\n";
	print "<p>　</p>\n";
	print "</body>\n";
	print "</html>\n";

	exit(0);
	
}

# -------------------------------------------------------------------------
# レスをデータファイルに書き込むサブルーチン
# -------------------------------------------------------------------------

sub res_message {

	if (!@RM) {
		&print_error('メッセージが指定されていません。<br>チェックボックスを確認して下さい。');
	}
	

# データファイルを読み込む --------------------------------------

	&get_cookie($mt_cookiename);
	$ck_pwd  = $cookie{'pwd'};

	&lock_open(TXT, "+<$datafile");
	@txt = <TXT>;
	($encoded_pass) = splice(@txt, 0, 1);
	chop($encoded_pass);
	
	if (&mismatch_password($ck_pwd, $encoded_pass)) {
		&unlock_close(TXT);
		&print_error("パスワードの有効期間が過ぎています。<br>再度ログインして下さい。");
	}

# レスの対象となる投稿を決定 ------------------------------------

	@tmp = @RM;
	foreach $tgtid(@tmp){
	
		if ($tgtid =~ /_/i){
		&print_error("レスを付ける際は親記事のみチェックして下さい。");
		}
			
		$index = &find_msg;

		if ($index < 0) {
			&unlock_close(TXT);
			&print_error("そのメッセージは存在しません。");
		}

		($dispid,$dispname,$dispicon,$dispmail,$dispurl,$dispdate,$disppwd,$dispsubject,$dispmsg,$disphost,$dispres) = split(/,/, $txt[$index]);

		chomp($dispres);

# レスのデータを整える ------------------------------------------

		$respnum = 'resp' . "$dispid";
		$subjnum = 'subject' . "$dispid";
		$resp = $FORMDATA{"$respnum"};
		$r_subj=$FORMDATA{"$subjnum"};
		
		$resp =~ s/\r/<br>/g;
		
# タグの使用不可の場合（URL にリンクをはる） --------------------

		if ($tagset eq 'off') {
			if ($autolink ne '') {
				$resp =~ s/(s?https?:\/\/[-_.!~*'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)/<a href="$1" target="_blank">$autolink<\/a>/ig;
			} else {
				$resp =~ s/(s?https?:\/\/[-_.!~*'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)/<a href="$1" target="_blank">$1<\/a>/ig;
			}
		}

# タグの使用可の場合の各処理 ------------------------------------

		if ($tagset eq 'on') {

			$resp =~ s/(&lt;[^&]*)<br>([^&]*&gt;)/$1$2/gi;
	
			if ($tagimg eq 'on') {
				$resp =~ s/(&lt;(img([^&]+))&gt;)/$1<img$3>/gi;
			}

			$resp .= "</a>" x (
				($resp =~ s/(&lt;(a href=([^&]+))&gt;)/<a href=$3>/gi)
				- ($resp =~ s/&lt;\/a&gt;/<\/a>/gi)
			);
	
			if ($tagfnt eq 'on') {
				$resp .= "</font>" x (
					($resp =~ s/(&lt;(font([^&]*))&gt;)/<font$3>/gi)
					- ($resp =~ s/&lt;\/font&gt;/<\/font>/gi)
				);
			}
	
			$resp .= "</b>" x (
				($resp =~ s/&lt;b&gt;/<b>/gi)
				- ($resp =~ s/&lt;\/b&gt;/<\/b>/gi)
			);
	
			$resp .= "</i>" x (
				($resp =~ s/&lt;i&gt;/<i>/gi)
				- ($resp =~ s/&lt;\/i&gt;/<\/i>/gi)
			);
	
			$resp =~ s/("[^ "<>]+)>/$1">/gi;
		}
		

# 作業の分岐 ----------------------------------------------------

		@part_res = split(/:&:/, $dispres);

# 日付の取得 ----------------------------------------------------

		$datestr = &get_date_string;

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

# host 情報の取得 -----------------------------------------------

		$host = $ENV{'REMOTE_HOST'};
		$addr = $ENV{'REMOTE_ADDR'};
		if ($host eq $addr) { 
			$host = gethostbyaddr(pack('C4',split(/\./,$host)),2) || $addr;
		}
			
# 書き込む情報の整列 --------------------------------------------

		$encpwd = &encode_pwd($ck_pwd);
		$oneline = "$dispid,$dispname,$dispicon,$dispmail,$dispurl,$dispdate,$disppwd,$dispsubject,$dispmsg,$disphost,$dispres$id<>$master_name<>master<>$admin<>$indexurl<>$datestr<>$encpwd<>$r_subj<>$resp<>$host:&:\n";
	

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
	}
	print TXT @txt;
	
	&unlock_close(TXT);


}

# -------------------------------------------------------------------------
# メッセージを削除するサブルーチン
# -------------------------------------------------------------------------

sub remove_message {

	if (!@RM) {
		&print_error('メッセージが指定されていません。<br>チェックボックスを確認して下さい。');
	}
	
	&get_cookie($mt_cookiename);
	$ck_pwd  = $cookie{'pwd'};

	&lock_open(TXT, "+<$datafile");
	@txt = <TXT>;
	($encoded_pass) = splice(@txt, 0, 1);
	chop($encoded_pass);
	
	if (&mismatch_password($ck_pwd, $encoded_pass)) {
		&unlock_close(TXT);
		&print_error("パスワードの有効期間が過ぎています。<br>再度ログインして下さい。");
	}
	
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
					splice(@part_res, $i, 1);
					$dispres = join(':&:',@part_res);
					$oneline = "$dispid,$dispname,$dispicon,$dispmail,$dispurl,$dispdate,$disppwd,$dispsubject,$dispmsg,$disphost,$dispres:&:\n";
					$oneline =~ s/,:&:/,/i;
					splice(@txt, $index, 1, $oneline);
					last;
				}
			}
		} else {
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
# 管理者用パスワード入力画面の表示
# -------------------------------------------------------------------------

sub mt_login {

	print "Content-type: text/html; charset=Shift_JIS\n";
	print "\n";
	print "<html>\n";
	print "<head>\n";
	print "<title>apeboard for webmaster</title>\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
	print "</head>\n";
	print "<body bgcolor=\"#FFFFFF\" text=\"#003366\">\n";
	print "<div align=\"center\">\n";
	print "<table width=\"90%\" height=\"90%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\n";
	print "<tr>\n";
	print "<td align=\"center\">\n";
	print "<form method=\"post\" action=\"$masterurl\">\n";
	print "<input type=\"hidden\" name=\"command\" value=\"f_read\">\n";
	print "<b><font size=\"4\" color=\"#CC0000\" face=\"Arial,Helvetica\">For Webmaster only!</font></b><br><br>\n";
	print "管理者用パスワードを入力して下さい。<br><br>\n";
	print "<input type=\"password\" name=\"pwd\" size=\"10\">&nbsp;&nbsp;";
	print "<input type=\"submit\" name=\"submit\" value=\"- Login -\">\n";
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
# 管理者用パスワード変更画面の表示
# -------------------------------------------------------------------------

sub shw_chpwd {

	print "Content-type: text/html; charset=Shift_JIS\n";
	print "\n";
	print "<html>\n";
	print "<head>\n";
	print "<title>apeboard for webmaster</title>\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
	print "</head>\n";
	print "<body bgcolor=\"#FFFFFF\" text=\"#003366\">\n";
	print "<div align=\"center\">\n";
	print "<table width=\"90%\" height=\"90%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\n";
	print "<tr>\n";
	print "<td align=\"center\">\n";
	print "<form method=\"post\" action=\"$masterurl\">\n";
	print "<input type=\"hidden\" name=\"command\" value=\"cg_and_ck\">\n";
	print "<b><font size=\"4\" color=\"#CC0000\" face=\"Arial,Helvetica\">For Webmaster only!</font></b><br><br>\n";
	print "パスワードは半角英数 4 文字以上で指定<br><br>\n";
	print "現在の管理者用パスワード：\n";
	print "<input type=\"password\" name=\"old_pwd\" size=\"10\"><br><br>";
	print "新しい管理者用パスワード：\n";
	print "<input type=\"password\" name=\"new_pwd\" size=\"10\"><br><br>";
	print "確認用にもう一度<br><br>\n";
	print "新しい管理者用パスワード：\n";
	print "<input type=\"password\" name=\"cknew_pwd\" size=\"10\"><br><br>";
	print "<input type=\"submit\" name=\"submit\" value=\"　　変　更　　\">\n";
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
# 管理者用パスワードのチェックと変更
# -------------------------------------------------------------------------

sub check_change {

	&lock_open(TXT, "+<$datafile");
	@txt = <TXT>;

	($encoded_pass) = splice(@txt, 0, 1);
	chop($encoded_pass);
	
	if ($encoded_pass eq '' || &mismatch_password($old_pwd, $encoded_pass)) {
		&unlock_close(TXT);
		&print_error("現在のパスワードが不適切、もしくは正しく設定されていません。");
	}
	
	if ($new_pwd ne $cknew_pwd) {
		&unlock_close(TXT);
		&print_error('新しいパスワードが確認用に入力されたものと一致しません。');
	}
	
	if ($new_pwd eq '' || length($new_pwd) < 4) {
		&unlock_close(TXT);
		&print_error('パスワードが入力されていないか、短すぎます。');
	}
	

	$encmaster = &encode_pwd($new_pwd);
	seek(TXT, 0, 0);
	print TXT "$encmaster\n";

	&unlock_close(TXT);
		
	print "Content-type: text/html; charset=Shift_JIS\n";
	print "\n";
	print "<html>\n";
	print "<head>\n";
	print "<title>- 変更完了 -</title>\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
	print "</head>\n";
	print "<body bgcolor=\"#FFFFFF\" text=\"#003366\">\n";
	print "<div align=\"center\">\n";
	print "<table width=\"90%\" height=\"90%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\n";
	print "<tr>\n";
	print "<td align=\"center\">\n";
	print "<form method=\"post\" action=\"$masterurl\">\n";
	print "<input type=\"hidden\" name=\"command\" value=\"f_read\">\n";
	print "<b><font size=\"4\" color=\"#0000CC\" face=\"Arial,Helvetica\">Password has changed.</font></b><br><br>\n";
	print "管理者用パスワードを変更しました。<br>\n";
	print "新しいパスワードで再ログインして下さい。<br><br>\n";
	print "<input type=\"password\" name=\"pwd\" size=\"10\">&nbsp;&nbsp;";
	print "<input type=\"submit\" name=\"submit\" value=\"- Login -\">\n";
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
#ファイルアンロックのサブルーチン
# -------------------------------------------------------------------------

sub unlock_close {

	local(*FILE) = @_;
	if ($lock) {
		eval("flock(FILE, 8)"); # 8=LOCK_UN
	}
	close(FILE);
	
}

# -------------------------------------------------------------------------
# パスワードの暗号化
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
# パスワードの照合
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
# クッキー取得のサブルーチン
# -------------------------------------------------------------------------

sub get_cookie {

	local($mt_cookiename) = @_;
	local($key, $value, @pairs, $pair);
	@sqpairs = split(/;\s/, $ENV{'HTTP_COOKIE'});
	foreach $sqpair (@sqpairs) {
		($sqkey, $sqvalue) = split(/=/, $sqpair);
		if ($sqkey eq $mt_cookiename) {
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

	local($mt_cookiename) = @_;
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
	return "$mt_cookiename=$sqstr; ";
	
}

# -------------------------------------------------------------------------
# クッキー表示のサブルーチン
# -------------------------------------------------------------------------

sub print_cookie {

	local($mt_cookiename, $hours, $domain) = @_;
	local($cookiestr) = &make_cookie($mt_cookiename);
	print "Set-Cookie: $cookiestr;";
	if ($domain) {
		print " domain=$domain;";
	}
	print "\n";
	
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
