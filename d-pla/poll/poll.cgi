#!/usr/local/bin/perl

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃Petit Poll Stylish Edition ver 4.3 (2003/10/07)
#┃Copyright(C) 2002-2003 9TST4. All Rights Reserved.
#┃URL：http://paxs.hp.infoseek.co.jp/
#┃E-mail：axs@cocoa.freemail.ne.jp
#┃Web Master：高見将智(Masatomo Takami)
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#┌─────────────────────────────────────────────────────────┐
#│【SE ver4.0以降のバージョンから乗り換える方】
#│
#│　　１：poll.cgiを差し替えるだけでご利用いただけます。
#│
#│
#│【SE ver4.0以前のバージョンから乗り換える方】
#│
#│　　１：新バージョンのログディレクトリ内に「使用中のログ」を移します。
#│　　２：管理モードへアクセスして、WEB上から設定変更を行ってください。
#│
#│
#│【Petit Pollから乗り換える方】
#│
#│　　１：新バージョンのログディレクトリ内に「使用中のログ」を移します。
#│　　２：同梱のck.cgi（設定変更済み）を一度だけ呼び出します。
#│　　３：管理モードへアクセスして、WEB上から設定変更を行ってください。
#│
#└─────────────────────────────────────────────────────────┘

require './jcode.pl';
my ($fpath, $ldir, $idir, @GAZOU, $qs_img, $rs_img, $od_img, $dw_img, $wn_img, $ad_img, $nw_img, $ptname, $lock, $web);

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃ファイル名の設定
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#このファイルへのパス（httpから）
$fpath = "http://www.d-planets.org/poll/poll.cgi";


#ログディレクトリへのパス（必ず任意の名前に変更。最後を「/」で閉じる）
$ldir  = "./log_d/";


#画像ディレクトリへのパス（httpから）
$idir  = "http://www.d-planets.org/poll/image/";


#バー画像（指定分だけ複数画像を使用）
@GAZOU = ("bar2.gif");


#質問アイコン
$qs_img = "q.gif";


#結果アイコン
$rs_img = "res.gif";


#過去アイコン
$od_img = "old.gif";


#配布元アイコン
$dw_img = "down.gif";


#管理アイコン
$ad_img = "ad.gif";


#拡縮アイコン
$wn_img = "win.gif";


#新着アイコン
$nw_img = "new.gif";


#以下は特に変更の必要はありません――――――――――――――――
$ptname = "pt.log";
$lock   = "lock";
$web    = "http://paxs.hp.infoseek.co.jp/";



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃デコード処理
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
my ($time, $pflag, $date, $datesize, @DATE, %FORMS, @DEL, @EDIT);

$ENV{'TZ'} = "JST-9";
$time = time;

if ($ENV{'REQUEST_METHOD'} eq "POST") {
	read (STDIN, $date, $ENV{'CONTENT_LENGTH'});
	$pflag = 1;
} else {
	$date = $ENV{'QUERY_STRING'};
}

if ($datesize and ($datesize != $ENV{'CONTENT_LENGTH'})) {
	undef ($datesize);
	&error ("データを正しく受け取れませんでした");
}

@DATE = split (/&/, $date);

foreach (@DATE) {
	my ($key, $val) = split (/=/);
	$val =~ tr/+/ /;
	$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;

	#&jcode::h2z_sjis (\$val);
	&jcode::convert (\$val, "sjis", "", "z");

	$val =~ s/&/&amp;/g;
	$val =~ s/"/&quot;/g;
	$val =~ s/</&lt;/g;
	$val =~ s/>/&gt;/g;

	#選択肢のみ改行処理
	if ($key eq "sel") {
		$val =~ s/\r\n/<BR>/g;
		$val =~ s/\r/<BR>/g;
		$val =~ s/\n/<BR>/g;
	} elsif ($key eq "hkick") {
		$val =~ s/\r\n/;/g;
		$val =~ s/\r/;/g;
		$val =~ s/\n/;/g;
	} else {
		$val =~ s/\r\n//g;
		$val =~ s/\r//g;
		$val =~ s/\n//g;
	}

	#削除コメントを配列へ
	if ($key eq "delarray") { push (@DEL, $val); }

	$FORMS{$key} = $val;

	if ($key eq "pass") {
		if (!$val) {
			&error ("パスワードが入力されていません");
		}
	} elsif ($key =~ /whi|cleng|nmark/) {
		if (!$val) {
			&error ("送信内容に記入漏れがあります");
		} elsif ($val =~ /\D/) {
			&error ("送信内容に全角数字が含まれています");
		}
	}

	push (@EDIT, "$key=$val\n");
}

undef (@DATE);



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃設定ファイル読み込み
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
my $set = $ldir . "set.dat";
my %SET = ();
my $now_lock = 0;

if (!open (SET, "< $set")) { &error ("設定ファイルを開けませんでした"); }
	while (chomp ($_ = <SET>)) {
		my ($key, $val) = split (/=/);

		$SET{$key} = $val;
	}
close (SET);

#設定変更後に色指定を反映するための措置
if ($FORMS{'temp'}) {
	$SET{'bback'} = $FORMS{'bback'};
	$SET{'bfont'} = $FORMS{'bfont'};
	$SET{'hback'} = $FORMS{'hback'};
	$SET{'hfont'} = $FORMS{'hfont'};
	$SET{'alink'} = $FORMS{'alink'};
	$SET{'vlink'} = $FORMS{'vlink'};
	$SET{'hlink'} = $FORMS{'hlink'};
	$SET{'efont'} = $FORMS{'efont'};
	
	undef ($FORMS{'temp'});
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃モード分岐
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
if (!$FORMS{'mode'}) {
	&head (1, "管理パスワード認証画面");
	&adcheck;
	&foot (1);
} elsif ($FORMS{'mode'} eq "adcheck") {
	&head (1, "管理パスワード認証画面");
	&adcheck;
	&foot (1);
} elsif ($FORMS{'mode'} eq "on") {
	&on_poll;
} elsif ($FORMS{'mode'} eq "result") {
	&result;
} elsif ($FORMS{'mode'} eq "cview") {
	&com_view;
} elsif ($FORMS{'mode'} eq "old") {
	&old;
} 

#以下モードはクエリ排除
if (!$pflag) { &error ("不正なアクセスです"); }

if ($FORMS{'mode'} eq "admin") {
	if (!$FORMS{'pass'} or $FORMS{'pass'} ne $SET{'pass'}) {
		&error ("管理パスワードが認証されませんでした");
	} else {
		&admin;
		&foot (1);
	}
} elsif ($FORMS{'mode'} eq "set") {
	&head (1, "設定変更フォーム");
	&set_form;
	&foot (1);
} elsif ($FORMS{'mode'} eq "s_edt") {
	&set_edit;
} elsif ($FORMS{'mode'} eq "new") {
	&head (1, "新規投票作成フォーム");
	&form;
	&foot (1);
} elsif ($FORMS{'mode'} eq "pre") {
	&pre;
	&foot (1);
} elsif ($FORMS{'mode'} eq "nmk") {
	&new_make;
} elsif ($FORMS{'mode'} eq "maint") {
	&maint;
} elsif ($FORMS{'mode'} eq "edit") {
	if ($FORMS{'ing'} != 1) { &error ("設定変更は進行中の投票しか行えません"); }
	&head (1, "設定変更フォーム");
	&form;
	&foot (1);
} elsif ($FORMS{'mode'} eq "rel") {
	&relog;
} elsif ($FORMS{'mode'} eq "comdel") {
	&com_delete;
} elsif ($FORMS{'mode'} eq "re_set") {
	&re_set;
} elsif ($FORMS{'mode'} eq "p_end") {
	&poll_end;
} elsif ($FORMS{'mode'} eq "p_del") {
	&poll_del;
} elsif ($FORMS{'mode'} eq "u_end") {
	&use_end;
} else {
	&error ("不正なアクセスです");
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃管理モード 認証画面
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub adcheck {
my ($p_edt);

$p_edt = qq|
<DIV style="width:400px;border:solid 1px #ccc;padding:6px;">
<BR>
<SPAN class="em_font" style="font-weight:bold;">！！！</SPAN>
<BR>
<BR>
管理パスワードは『0123』です。早急に設定変更を行って下さい。
<BR>
<BR>
</DIV>
<BR>
|;

#パス0123は警告
if ($SET{'pass'} ne "0123") { $p_edt = "管理パスワードを入力してください<BR>"; }

print <<EOF;
$p_edt
<BR>

<FORM method="POST" action="$fpath">
<INPUT type="password" name="pass" size="8">
<INPUT type="hidden" name="mode" value="admin">
<INPUT type="hidden" name="act" value="1">
<INPUT type="submit" value="認証">
</FORM>

EOF
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃投票管理画面
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub admin {
#再入室キーを取得
if (!$FORMS{'act'}) { $FORMS{'pass'} = $_[0]; }

#ディレクトリをチェック
unless (-e $ldir) { &error ("ログディレクトリを作成してください"); }

#投票タイトルログ
my $ptlog = $ldir . $ptname;

#投票タイトルログをチェック
unless (-e $ptlog) {
	if (!open (PT, ">$ptlog")) { &error ("投票タイトルログの作成に失敗しました"); }
	close (PT);
	chmod (0666, "$ptlog");
}


my $p_edt = qq|
<BR>
*初めてのアクセス時には「設定変更」から管理パスワードを変更して下さい。
|;

if ($FORMS{'pass'} ne "0123") { undef ($p_edt); }


#投票タイトルを取得
if (!open (PT, "<$ptlog")) { &error ("投票タイトルログが開けませんでした"); }

&head (1, "投票管理画面");

print <<EOF;
<DIV style="text-align:left;width:440px;">
*メンテナンス画面へ進むには、タイトルの前のボタンにチェックを入れて下さい。
<BR>
*「投票を全削除」すると、作成した投票がすべて削除されます。
$p_edt
</DIV>
<BR>
<BR>

<FORM method="POST" action="$fpath">
<DIV class="pframe">
<TABLE cellpadding="3" cellspacing="1" border="0" summary="リスト">
<TR>
<TD class="pline1" style="width:40px;">ID</TD>
<TD class="pline1" style="width:40px;">メンテ</TD>
<TD class="pline1" style="width:400px;">投票タイトル</TD>
</TR>

EOF

my $idno = 1;	#新規作成時のIDナンバー
my $exflag = 0;	#投票存在フラグ

#投票タイトルを取得
while (chomp ($_ = <PT>)) {
	my ($id, $ptitle, $ing) = split (/<>/);

	print qq|<TR><TD class="pline2">$id</TD>|;

		if ($ing == 1) {
			print qq|<TD class="pline2"><INPUT type="radio" name="id" value="$id"></TD>|;
			print qq|<TD class="pline2">$ptitle</TD>|;
		} elsif ($ing == 2) {
			print qq|<TD class="pline2"><INPUT type="radio" name="id" value="$id"></TD>|;
			print qq|<TD class="pline2">$ptitle<SPAN style="color:$SET{'efont'};">（終了）</SPAN></TD>|;
		} elsif (!$ing) {
			print qq|<TD class="pline2">-</TD>|;
			print qq|<TD class="pline2">$ptitle<SPAN style="color:$SET{'efont'};">（削除）</SPAN></TD>|;
		}

	print qq|</TR>|;

	$idno ++;
	$exflag = 1;
}

close (PT);

#リスト分岐
if (!$exflag) {
	print qq|
	<TR>
	<TD class="pline2">-</TD>
	<TD class="pline2">-</TD>
	<TD class="pline2">現在行われている投票はありません</TD>
	</TR>
	</TABLE>
	</DIV>
	|;
} else {
	print "</TABLE></DIV>\n";
}

print <<EOF;
<BR>
<BR>
<TABLE cellpadding="1" cellspacing="2" border="0" summary="メニュー">
<TR>
<TD>
<INPUT type="hidden" name="mode" value="maint">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="hidden" name="act" value="1">
<INPUT type="submit" value="チェック項目を編集">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="id" value="$idno">
<INPUT type="hidden" name="mode" value="new">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="投票を作成">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="u_end">
<INPUT type="submit" value="投票を全削除">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="set">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="設定変更">
</FORM>
</TD>
</TR>
</TABLE>

EOF

}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃設定ファイル フォーム
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub set_form {
my (%CHECK);
#表示形式
if (!$SET{'rtype'}) {
	$CHECK{'rtp_0'} = " checked";
} else {
	$CHECK{'rtp_1'} = " checked";
}

#コメント閲覧
if (!$SET{'ctype'}) {
	$CHECK{'ctp_0'} = " checked";
} else {
	$CHECK{'ctp_1'} = " checked";
}

#ソート方式
if (!$SET{'stype'}) {
	$CHECK{'stp_0'} = " checked";
} elsif ($SET{'stype'} == 1) {
	$CHECK{'stp_1'} = " checked";
} elsif ($SET{'stype'} == 2) {
	$CHECK{'stp_2'} = " checked";
}

#ファイルロック
if (!$SET{'lkey'}) {
	$CHECK{'lky_0'} = " checked";
} else {
	$CHECK{'lky_1'} = " checked";
}

print <<EOF;
<DIV style="text-align:left;width:460px;line-height:16px;">
*全投票共通の設定です。
<BR>
*色指定に漏れ・誤りがあると、色が正常に反映されませんのでご注意ください。
<BR>
*結果表\示・小窓サイズ・色指定を変更した場合、ソ\ースを交換して下さい。
<BR>
*ホスト制限は最後の部分を省いて下さい。（127.0.0.1  -&gt;  127.0.0）
</DIV>

<FORM method="POST" action="$fpath">
<DIV class="fframe">
<TABLE cellpadding="5" cellspacing="1" border="0">
<TR>
<TD class="fleft">投票全体のタイトル</TD>
<TD class="fright">
<INPUT type="text" name="title" size="50" value="$SET{'title'}">
</TD>
</TR>

<TR>
<TD class="fleft">ホームページ</TD>
<TD class="fright">
<INPUT type="text" name="home" size="50" value="$SET{'home'}">
</TD>
</TR>

<TR>
<TD class="fleft">管理パスワード</TD>
<TD class="fright">
<INPUT type="text" name="pass" size="8" value="$SET{'pass'}">
<SPAN class="em_font">※半角英数字のみ</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft">結果表\示</TD>
<TD class="fright">
<INPUT type="radio" name="rtype" value="0"$CHECK{'rtp_0'}>小窓で開く
<INPUT type="radio" name="rtype" value="1"$CHECK{'rtp_1'}>既存のウィンドウで開く
</TD>
</TR>

<TR>
<TD class="fleft">コメント閲覧制限</TD>
<TD class="fright">
<INPUT type="radio" name="ctype" value="0"$CHECK{'ctp_0'}>誰でも可
<INPUT type="radio" name="ctype" value="1"$CHECK{'ctp_1'}>管理者のみ
</TD>
</TR>

<TR>
<TD class="fleft">投票結果のソ\ート</TD>
<TD class="fright">
<INPUT type="radio" name="stype" value="0"$CHECK{'stp_0'}>行わない
<INPUT type="radio" name="stype" value="1"$CHECK{'stp_1'}>昇順
<INPUT type="radio" name="stype" value="2"$CHECK{'stp_2'}>降順
</TD>
</TR>

<TR>
<TD class="fleft">小窓の高さ</TD>
<TD class="fright">
<INPUT type="text" name="whi" size="4" value="$SET{'whi'}">
<SPAN class="em_font">※半角数字のみ/標準：302（選択肢4つ）</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft">コメントの長さ</TD>
<TD class="fright">
<INPUT type="text" name="cleng" size="4" value="$SET{'cleng'}">
<SPAN class="em_font">※半角数字のみ/機\能\利用時に取得できる文字長（全角換算）</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft">コメントの新着マーク</TD>
<TD class="fright">
<INPUT type="text" name="nmark" size="4" value="$SET{'nmark'}">時間以内
<SPAN class="em_font">※半角数字のみ</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft">ファイルロック</TD>
<TD class="fright">
<INPUT type="radio" name="lkey" value="0"$CHECK{'lky_0'}>ロックしない
<INPUT type="radio" name="lkey" value="1"$CHECK{'lky_1'}>ロックする
</TD>
</TR>

<TR>
<TD class="fleft">ホスト制限</TD>
<TD class="fright">
<TEXTAREA cols="20" rows="3" name="hkick">
EOF

foreach (split (/;/, $SET{'hkick'})) {
	print "$_\n";
}

print <<EOF;
</TEXTAREA>
<SPAN class="em_font">※一行に一件ずつ</SPAN>
</TD>
</TR>
</TABLE>
</DIV>
<BR>

<DIV class="fframe">
<TABLE cellpadding="5" cellspacing="1" border="0">
<TR>
<TD class="fleft2">全体の背景色とフォント色</TD>
<TD class="fright2">
<INPUT type="text" name="bback" size="8" value="$SET{'bback'}">/
<INPUT type="text" name="bfont" size="8" value="$SET{'bfont'}">
<SPAN class="em_font">（背景/フォント）</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft2">ヘッダーの下地とフォント色</TD>
<TD class="fright2">
<INPUT type="text" name="hback" size="8" value="$SET{'hback'}">/
<INPUT type="text" name="hfont" size="8" value="$SET{'hfont'}">
<SPAN class="em_font">（下地/フォント）</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft2">リンク</TD>
<TD class="fright2">
<INPUT type="text" name="alink" size="8" value="$SET{'alink'}">/
<INPUT type="text" name="vlink" size="8" value="$SET{'vlink'}">/
<INPUT type="text" name="hlink" size="8" value="$SET{'hlink'}">
<SPAN class="em_font">（通常/訪問済み/マウスオーバー）</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft2">投票フレーム色とフォント色</TD>
<TD class="fright2">
<INPUT type="text" name="rback1" size="8" value="$SET{'rback1'}">/
<INPUT type="text" name="rfont1" size="8" value="$SET{'rfont1'}">
<SPAN class="em_font">（フレーム/フォント）</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft2">投票データ部の下地とフォント色</TD>
<TD class="fright2">
<INPUT type="text" name="rback2" size="8" value="$SET{'rback2'}">/
<INPUT type="text" name="rfont2" size="8" value="$SET{'rfont2'}">
<SPAN class="em_font">（下地/フォント）</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft2">投票フレームの影</TD>
<TD class="fright2">
<INPUT type="text" name="rshadow" size="8" value="$SET{'rshadow'}">
<SPAN class="em_font">（投票データ部の下地と同じ色でも良）</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft2">強調フォント色</TD>
<TD class="fright2">
<INPUT type="text" name="efont" size="8" value="$SET{'efont'}">
<SPAN class="em_font">（注釈ほか、投票期間などの色）</SPAN>
</TD>
</TR>
</TABLE>
</DIV>
<BR>
<BR>
<BR>

<INPUT type="hidden" name="mode" value="s_edt">
<INPUT type="hidden" name="temp" value="1">
<INPUT type="button" value="戻る" onClick="JavaScript:history.back()">
<INPUT type="submit" value="変更を反映する">
</FORM>

EOF
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃設定ファイル 作成
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub set_edit {
#modeとtempを削除
pop (@EDIT);
pop (@EDIT);

#変更不可能な事項を追加
push (@EDIT, "bhi=$SET{'bhi'}\n");

if ($SET{'lkey'}) { if (!&lock_on) { &error ("サーバーが混み合っています"); } }
$now_lock = 1;

if (!open (SET, "+< $set")) { &error ("設定ファイルを開けませんでした"); }
seek (SET, 0, 0);
print SET @EDIT;
truncate (SET, tell);
close (SET);

if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

#削除後対策のため、再入室キーを削除
undef ($FORMS{'act'});

&admin ($FORMS{'pass'});
&foot (1);
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃投票作成フォーム
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub form {
my ($setline);

if ($FORMS{'mode'} eq "new") {
	print qq|
		<DIV style="width:400px;text-align:left;line-height:18px;">
		*設定は各投票ごとに区別されます。<BR>
		*コメントは限界数を超えると「古い方から順」に削除されます。<BR>
		*投票の自動終了は「条件に一致した方」が優先されます。
		</DIV>
		<BR>\n
		|;
} else {
	my $idlog = $ldir . $FORMS{'id'} . ".log";

	if (!open (ID, "<$idlog")) { &error ("投票ログが開けませんでした"); }

	$setline = <ID>;

	close (ID);
}

#投票数/質問/閲覧制限/コメント取得/コメント限界/連禁/連禁期間/連禁単位/終了秒数/限界投票/開始時刻/終了時刻/ingフラグ
my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split (/<>/, $setline) if ($setline);

#フォーム内容の定義（設定変更時用）
my (%CHECK);
if ($FORMS{'mode'} ne "new") {
	#閲覧制限
	if ($reye) {
		$CHECK{'rch_1'} = " checked";
	} else {
		$CHECK{'rch_0'} = " checked";
	}

	#コメント取得
	if (!$cget) {
		$CHECK{'cgt_0'} = " checked";
	} elsif ($cget == 1) {
		$CHECK{'cgt_1'} = " checked";
	} elsif ($cget == 2) {
		$CHECK{'cgt_2'} = " checked";
	}

	#連続投票禁止
	if (!$pkick) {
		$CHECK{'pkc_0'} = " checked";
	} elsif ($pkick == 1) {
		$CHECK{'pkc_1'} = " checked";
	}

	#連続投票禁止
	if (!$kunit) {
		$CHECK{'kut_0'} = " checked";
	} elsif ($kunit == 1) {
		$CHECK{'kut_1'} = " checked";
	} elsif ($kunit == 2) {
		$CHECK{'kut_2'} = " checked";
	}

	#残り日数
	my $p_bef = sprintf ("%.1f", ($period - $time) / 86400);
	$period = (int ($p_bef) == $p_bef) ? sprintf ("%d", $p_bef) : int ($p_bef) + 1;

	if (!$cget)   { undef ($climit); }
	if (!$kval)   { undef ($kval); }
	if (!$plimit) { undef ($plimit); }
	if ($end eq "無期限") { undef ($period); }
} else {
	$CHECK{'rch_1'} = " checked";
	$CHECK{'cgt_0'} = " checked";
	$CHECK{'pkc_0'} = " checked";
	$CHECK{'kut_0'} = " checked";
}

print <<EOF;
<FORM method="POST" action="$fpath">
<DIV class="fframe">
<TABLE cellpadding="5" cellspacing="1" border="0">
EOF

if ($FORMS{'mode'} eq "new") {
	print qq|
	<TR>
	<TD class="fleft">質問内容</TD>
	<TD class="fright"><INPUT type="text" name="qst" size="50"></TD>
	</TR>
	
	<TR>
	<TD class="fleft">選択肢</TD>
	<TD class="fright">
	<TEXTAREA cols="40" rows="5" name="sel"></TEXTAREA><BR>
	<DIV class="em_font">・選択肢は1行につき一つずつ記入してください（点や英数字は要りません）</DIV>
	<DIV class="em_font">・選択肢は最低2つ以上用意してください</DIV>
	</TD>
	</TR>
	|;
}

#新規作成、設定変更共用フォーム
print <<EOF;
<TR>
<TD class="fleft">結果閲覧</TD>
<TD class="fright">
<INPUT type="radio" name="reye" value="0"$CHECK{'rch_0'}>未投票時は不可
<INPUT type="radio" name="reye" value="1"$CHECK{'rch_1'}>いつでも可
</TD>
</TR>

<TR>
<TD class="fleft">コメント取得</TD>
<TD class="fright">
<INPUT type="radio" name="cget" value="0"$CHECK{'cgt_0'}>未使用
<INPUT type="radio" name="cget" value="1"$CHECK{'cgt_1'}>任意
<INPUT type="radio" name="cget" value="2"$CHECK{'cgt_2'}>必須
</TD>
</TR>

<TR>
<TD class="fleft">コメント限界数</TD>
<TD class="fright">
選択肢一つにつき<INPUT type="text" name="climit" size="4" value="$climit">個まで
<DIV class="em_font">（半角数字、0か未記入なら5個まで、機\能\使用時のみ反映）</DIV>
</TD>
</TR>

<TR>
<TD class="fleft">連続投票禁止機\能\</TD>
<TD class="fright">
<INPUT type="radio" name="pkick" value="0"$CHECK{'pkc_0'}>未使用
<INPUT type="radio" name="pkick" value="1"$CHECK{'pkc_1'}>使用
</TD>
</TR>

<TR>
<TD class="fleft">連続投票禁止期間</TD>
<TD class="fright">
<INPUT type="text" name="kval" size="4" value="$kval">
<INPUT type="radio" name="kunit" value="0"$CHECK{'kut_0'}>分
<INPUT type="radio" name="kunit" value="1"$CHECK{'kut_1'}>時間
<INPUT type="radio" name="kunit" value="2"$CHECK{'kut_2'}>日
<DIV class="em_font">（左/半角数字、右/単位、0か未記入なら一人一回、機\能\使用時のみ反映）</DIV>
</TD>
</TR>

<TR>
<TD class="fleft">投票期間</TD>
<TD class="fright">
<INPUT type="text" name="period" size="4" value="$period">日間
<DIV class="em_font">（半角数字、0か未記入なら無期限、指定期間で自動終了）</DIV>
</TD>
</TR>

<TR>
<TD class="fleft">限界投票数</TD>
<TD class="fright">
<INPUT type="text" name="plimit" size="4" value="$plimit">票
<DIV class="em_font">（半角数字、0か未記入なら無期限、指定票で自動終了）</DIV>
</TD>
</TR>
EOF

if ($FORMS{'mode'} eq "new") {
	print qq|
		</TABLE>
		</DIV>
		<BR>
		<BR>
		<BR>
		
		<INPUT type="hidden" name="id" value="$FORMS{'id'}">
		<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
		<INPUT type="hidden" name="mode" value="pre">
		<INPUT type="button" value="戻る" onClick="JavaScript:history.back()">
		<INPUT type="submit" value="この内容で確認する">
		</FORM>
		|;
} else {
	print qq|
		</TABLE>
		</DIV>
		<BR>
		<BR>
		<BR>
		
		<INPUT type="hidden" name="id" value="$FORMS{'id'}">
		<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
		<INPUT type="hidden" name="mode" value="rel">
		<INPUT type="button" value="戻る" onClick="JavaScript:history.back()">
		<INPUT type="submit" value="変更を反映する">
		</FORM>
		|;
}
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃投票作成 確認
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub pre {
my ($sel_d, @SEL, $ing_ms);

if ($FORMS{'mode'} eq "pre") {
	#選択肢の内容は送信用と確認用を用意
	$sel_d = $FORMS{'sel'};

	#確認用の選択肢を配列に代入
	@SEL = split (/<BR>/, $FORMS{'sel'});

	#送信内容確認
	if (!$FORMS{'qst'}) {
		&error ("質問内容が記入されていません");
	} elsif (!$SEL[1]) {
		&error ("選択肢は最低2つ以上用意してください");
	}
	#投票状況
	$ing_ms = "進行中";
} else {
	my ($reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = @_;

	$FORMS{'reye'}   = $reye;
	$FORMS{'cget'}   = $cget;
	$FORMS{'climit'} = $climit;
	$FORMS{'pkick'}  = $pkick;
	$FORMS{'kval'}   = $kval;
	$FORMS{'kunit'}  = $kunit;
	$FORMS{'plimit'} = $plimit;
	$FORMS{'start'}  = $start;
	$FORMS{'end'}    = $end;
	
	if ($ing == 1) { $ing_ms ="進行中"; } else { $ing_ms ="終了"; }
}

#結果閲覧フラグ（添え字は$FORMS{'reye'}）
my @REYE = qw (未投票時は不可 いつでも可);

#結果表示タイプ / コメント閲覧制限
my @RTYPE = qw (小窓を開く 小窓を開かない);
my @CTYPE = qw (誰でも可 管理者のみ);

#投票期間
if ($FORMS{'period'} =~ /\D/) { &error ("投票期間に無効な数値が含まれています"); }

#開始日と終了日
if ($FORMS{'mode'} eq "pre") { &opening; &finale; }

#コメント取得（$FORMS{'cget'} = 使用未使用 / $FORMS{'climit'} = 取得数）
my ($c_ms, $c_lt);
if ($FORMS{'climit'} =~ /\D/) {
	&error ("限界コメント数に無効な数値が含まれています");
} elsif (!$FORMS{'climit'}) {
	$FORMS{'climit'} = 5;
}

if (!$FORMS{'cget'}) { 
	$c_ms = "未使用";
	$c_lt = "未設定";
} elsif ($FORMS{'cget'} == 1) {
	$c_ms = "任意";
	$c_lt = "各$FORMS{'climit'}個まで";
} elsif ($FORMS{'cget'} == 2) {
	$c_ms = "必須";
	$c_lt = "各$FORMS{'climit'}個まで";
}

#連禁期間（添え字は$FORMS{'kunit'}）
my ($k_ms);
my @KUNIT = qw (分 時間 日);
if(!$FORMS{'pkick'}) {
	$k_ms = "未設定";
	$FORMS{'kval'} = 0;
} else {
	if (!$FORMS{'kval'}) {
		$k_ms = "一人一回";
		$FORMS{'kval'} = 0;
	} else {
		$k_ms = "$FORMS{'pkick'}$KUNIT[$FORMS{'kunit'}]に一回";
	}
}

#限界投票
my $pl_ms;
if ($FORMS{'plimit'} =~ /\D/) {
	&error ("限界投票数に無効な数値が含まれています");
} elsif (!$FORMS{'plimit'}) {
	$pl_ms = "未設定";
} else  {
	$pl_ms = "$FORMS{'plimit'}票まで";
}

if ($FORMS{'mode'} eq "pre") {
	&head (1, "新規投票作成確認画面");

	print qq|
	<DIV style="width:400px;text-align:left;line-height:18px;">
	*下記の内容でよろしければ、「この内容で作成する」ボタンを押してください。<BR>
	*内容に訂正があれば「戻る」ボタンを押してください。<BR>
	*作成後に質問、選択肢の内容を変えることはできません。<BR>
	*設定、フォームデザインは設置後でも自由に変更することができます。
	</DIV>
	<BR>
	<BR>\n
	|;
}

#設定テーブル
print <<EOF;
<DIV class="fframe">
<TABLE cellpadding="5" cellspacing="1" border="0">
<TR>
<TD class="sleft">投票状況</TD>
<TD class="sright">$ing_ms</TD>
<TD class="sleft">開始日</TD>
<TD class="sright">$FORMS{'start'}</TD>
<TD class="sleft">終了日</TD>
<TD class="sright">$FORMS{'end'}</TD>
</TR>

<TR>
<TD class="sleft">限界投票数</TD>
<TD class="sright">$pl_ms</TD>
<TD class="sleft">コメント取得</TD>
<TD class="sright">$c_ms</TD>
<TD class="sleft">コメント限界数</TD>
<TD class="sright">$c_lt</TD>
</TR>

<TR>
<TD class="sleft">連投禁止期間</TD>
<TD class="sright">$k_ms</TD>
<TD class="sleft">結果閲覧</TD>
<TD class="sright">$REYE[$FORMS{'reye'}]</TD>
<TD class="sleft">コメント閲覧</TD>
<TD class="sright">$CTYPE[$SET{'$ctype'}]</TD>
</TR>

<TR>
<TD class="sleft">結果表\示</TD>
<TD class="sright">$RTYPE[$SET{'rtype'}]</TD>
<TD class="sleft">&nbsp;</TD>
<TD class="sright">&nbsp;</TD>
<TD class="sleft">&nbsp;</TD>
<TD class="sright">&nbsp;</TD>
</TR>
</TABLE>
</DIV>
<BR>
<BR>

EOF

if ($FORMS{'mode'} eq "pre") {
	#投票フォームサンプル
	print qq|
	<FORM>
	<DIV style="font-size:13px;width:180px;background-color:$SET{'rback1'};border:solid 1px $SET{'rback2'};padding:3px;">
	<DIV style="width:100%;color:$SET{'rfont1'};text-align:left;padding-bottom:3px;">
	<IMG src="$idir$qs_img"> $FORMS{'qst'}
	</DIV>
	<DIV style="width:100%;text-align:left;background-color:$SET{'rback2'};color:$SET{'rfont2'};border-top:solid 2px $SET{'rshadow'};border-left:solid 2px $SET{'rshadow'};padding:3px;">
	\n
	|;

	#選択肢部を展開
	my $no = 1;
	foreach (0 .. $#SEL) {
		my $check = " checked" if ($no == 1);
		print qq|<DIV style="padding:3px;"><INPUT type="radio" name="poll" value="$no"$check>$SEL[$_]</DIV>\n|;
		$no ++;
		undef ($check);
	}

	print qq|<DIV align="center"><BR>|;
	
	#コメントフォームを展開
	if ($FORMS{'cget'}) {
		print qq|
		コメント<BR>
		<INPUT type="text" size="25" name="com"><BR><BR>
		|;
	}

	print qq|
	<INPUT type="button" value="投票"><BR><BR>
	</DIV>
	</DIV>
	<SPAN style="width:100%;text-align:right;padding-top:3px;">
	<IMG src="$idir$rs_img" border="0" alt="結果" title="結果">
	<IMG src="$idir$od_img" border="0" alt="過去の投票" title="過去の投票">
	<IMG src="$idir$dw_img" border="0" alt="Petit Poll SE ダウンロード">
	<IMG src="$idir$ad_img" border="0" alt="管理" title="管理">
	</SPAN>
	</DIV>
	</FORM>
	<BR>
	<BR>
	
	<FORM method="POST" action="$fpath">
	<INPUT type="hidden" name="mode" value="nmk">
	<INPUT type="hidden" name="id" value="$FORMS{'id'}">
	<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
	<INPUT type="hidden" name="qst" value="$FORMS{'qst'}">
	<INPUT type="hidden" name="sel" value="$sel_d">
	<INPUT type="hidden" name="reye" value="$FORMS{'reye'}">
	<INPUT type="hidden" name="cget" value="$FORMS{'cget'}">
	<INPUT type="hidden" name="climit" value="$FORMS{'climit'}">
	<INPUT type="hidden" name="pkick" value="$FORMS{'pkick'}">
	<INPUT type="hidden" name="kval" value="$FORMS{'kval'}">
	<INPUT type="hidden" name="kunit" value="$FORMS{'kunit'}">
	<INPUT type="hidden" name="period" value="$FORMS{'period'}">
	<INPUT type="hidden" name="plimit" value="$FORMS{'plimit'}">
	<INPUT type="hidden" name="start" value="$FORMS{'start'}">
	<INPUT type="hidden" name="end" value="$FORMS{'end'}">
	<INPUT type="button" value="戻る" onClick="JavaScript:history.back()">
	<INPUT type="submit" value="この内容で作成する">
	</FORM>\n
	|;
}
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃投票作成 更新
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub new_make {
#ログを定義
my $ptlog = $ldir . $ptname;
my $idlog = $ldir . $FORMS{'id'} . ".log";

if ($SET{'lkey'}) { if (!&lock_on) { &error ("サーバーが混み合っています"); } }
$now_lock = 1;

#投票タイトルログを開く
if (!open (PT, "+<$ptlog")) { &error ("投票タイトルログが開けませんでした"); }

my @PNEW = ();
while (chomp ($_ = <PT>)) {
	my ($id, $qst, $ing) = split (/<>/, $_);

	#二重作成チェック
	if ($id eq $FORMS{'id'}) {
		&error ("既に投票作成が完了しています");
	} elsif ($qst eq $FORMS{'qst'}) {
		&error ("同じ質問の投票が作成済みです");
	}

	push (@PNEW, "$_\n");
}

#新規配列追加
push (@PNEW, "$FORMS{'id'}<>$FORMS{'qst'}<>1\n");
seek (PT, 0, 0);
print PT @PNEW;
truncate (PT, tell);
close(PT);

#IDログを作成
if (!open (ID, ">$idlog")) { &error ("投票ログの作成に失敗しました"); }
	seek (ID, 0, 0);

	#投票数/質問/閲覧制限/コメント取得/コメント限界/連禁/連禁期間/連禁単位/終了秒数/限界投票/開始時刻/終了時刻/ingフラグ
	print ID "0<>$FORMS{'qst'}<>$FORMS{'reye'}<>$FORMS{'cget'}<>$FORMS{'climit'}<>$FORMS{'pkick'}<>$FORMS{'kval'}<>$FORMS{'kunit'}<>$FORMS{'period'}<>$FORMS{'plimit'}<>$FORMS{'start'}<>$FORMS{'end'}<>1\n";

	my $no = 1;
	my @SEL = split (/&lt;BR&gt;/, $FORMS{'sel'});

	foreach (0 .. $#SEL) {
		print ID "$no<><>$SEL[$_]<><><>0\n";
		$no++;
	}

	truncate (ID, tell);
close (ID);
chmod (0666, "$idlog");

if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

&head (1, "投票フォーム ソ\ース");

print <<EOF;
<DIV style="width:400px;text-align:left;line-height:18px;">
*下のソ\ースをコピーして、設置したいHTMLファイルに\貼\り付けてください。<BR>
*こちらのソ\ースは、メンテナンスモードでいつでも確認ができます。
</DIV>
<BR>
<BR>
EOF

&sourse (0, 0, @SEL);
&foot (1);

}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃ソース
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub sourse {
my ($qst, $cget, @SEL) = @_;
$FORMS{'qst'} ||= $qst;

my ($front, $button, $rslink);
#小窓使用未使用の分岐（前FORM / 投票ボタン / 結果リンク）
if ($SET{'rtype'}) {
	$front  = "&lt;FORM method=&quot;POST&quot; action=&quot;$fpath&quot;&gt;";
	$button = "&lt;INPUT type=&quot;submit&quot; value=&quot;投票&quot;&gt;";
	$rslink = "&lt;A href=&quot;$fpath?mode=result&amp;id=$FORMS{'id'}&quot;&gt;<BR>&lt;IMG src=&quot;$idir$rs_img&quot; alt=&quot;結果&quot; border=&quot;0&quot;&gt;&lt;/A&gt;";
} else {
	$front  = "&lt;FORM name=&quot;pollform$FORMS{'id'}&quot;&gt;";
	$button = "&lt;INPUT type=&quot;button&quot; value=&quot;投票&quot;onClick=&quot;OpenWin$FORMS{'id'}()&quot;&gt;";
	$rslink = "&lt;A href=&quot;JavaScript:ResultWin('$FORMS{'id'}')&quot;&gt;<BR>&lt;IMG src=&quot;$idir$rs_img&quot; alt=&quot;結果&quot; border=&quot;0&quot;&gt;&lt;/A&gt;";
}

print qq|<DIV class="sourse">\n|;

#小窓使用未使用＆コメント有無の分岐
if (!$SET{'rtype'}) {
	print qq|
		&lt;!-- Petit Poll JavaScript ID$FORMS{'id'}--&gt;<BR>
		&lt;SCRIPT type=&quot;text/javascript&quot;&gt;<BR>
		&lt;!--<BR>
		function OpenWin$FORMS{'id'}() {<BR>
		var id = document.pollform$FORMS{'id'}.id.value;<BR>
		|;

	if ($FORMS{'cget'} or $cget) {
	print qq|
		var com = document.pollform$FORMS{'id'}.com.value;<BR><BR>
		if (com == &quot;&quot;) {<BR>
		document.pollform$FORMS{'id'}.com.value = \'none\';<BR>
		com = document.pollform$FORMS{'id'}.com.value;<BR>
		} else {<BR>
		com = document.pollform$FORMS{'id'}.com.value;<BR>
		}<BR>
		<BR>
		|;
	}

	print qq|
		var poll = 0;<BR><BR>
		for (var i=0; i < document.pollform$FORMS{'id'}.poll.length; i++) {<BR>
		if (document.pollform$FORMS{'id'}.poll[i].checked) {<BR>
		poll = document.pollform$FORMS{'id'}.poll[i].value;<BR>
		}<BR>
		}<BR>
		<BR>
		if (poll == 0) {<BR>
		alert (&quot;項目がチェックされていません！&quot;);<BR>
		} else {<BR>
		|;

	if ($FORMS{'cget'} or $cget) {
		print qq|window.open (\'$fpath?mode=on&amp;id=\'+id+\'&amp;poll=\'+poll+\'&amp;com=\'+com, \'newwin\', \'menubar=no, scrollbars=yes, width=330, height=$SET{'whi'}\');<BR>\n|;
	} else {
		print qq|window.open(\'$fpath?mode=on&amp;id=\'+id+\'&amp;poll=\'+poll, \'newwin\', \'menubar=no, scrollbars=yes, width=330, height=$SET{'whi'}\');<BR>\n|;
	}

	print qq|
		}<BR>
		}<BR>
		<BR>
		function ResultWin (Id) {<BR>
		window.open(\'$fpath?mode=result&amp;id=\'+Id,\'newwin\',\'menubar=no, scrollbars=yes, width=330, height=$SET{'whi'}\');<BR>
		}<BR>
		//--&gt;<BR>
		&lt;/SCRIPT&gt;<BR>
		&lt;!-- Petit Poll JavaScript ID$FORMS{'id'} END --&gt;<BR><BR>
		|;
}

#投票フォームサンプル
print <<EOF;
&lt;!-- 投票フォーム ID$FORMS{'id'}--&gt;<BR>
$front<BR>
&lt;DIV style=&quot;font-size:13px;width:180px;background-color:$SET{'rback1'};border:solid 1px $SET{'rback2'};padding:3px;&quot;&gt;<BR>
&lt;DIV style=&quot;width:100%;color:$SET{'rfont1'};text-align:left;padding-bottom:3px;&quot;&gt;<BR>
&lt;IMG src=&quot;$idir$qs_img&quot; alt=&quot;質問&quot;&gt; $FORMS{'qst'}<BR>
&lt;/DIV&gt;<BR>
&lt;DIV style=&quot;width:100%;text-align:left;background-color:$SET{'rback2'};color:$SET{'rfont2'};border-top:solid 2px $SET{'rshadow'};border-left:solid 2px $SET{'rshadow'};padding:3px;&quot;&gt;<BR>
EOF

#選択肢部を展開
my $no = 1;
foreach (0 .. $#SEL) {
	my $check = " checked" if ($no == 1);
	print qq|&lt;DIV style=&quot;padding:3px;&quot;&gt;&lt;INPUT type=&quot;radio&quot; name=&quot;poll&quot; value=&quot;$no&quot;$check&gt;$SEL[$_]&lt;/DIV&gt;<BR>\n|;
	$no ++;
	undef ($check);
}


print qq|
	&lt;DIV align=&quot;center&quot;&gt;&lt;BR&gt;<BR>
	&lt;INPUT type=&quot;hidden&quot; name=&quot;id&quot; value=&quot;$FORMS{'id'}&quot;&gt;<BR>
	|;

if ($SET{'rtype'}) {
	print "&lt;INPUT type=&quot;hidden&quot; name=&quot;mode&quot; value=&quot;on&quot;&gt;";
}

#コメントフォームを展開
if ($FORMS{'cget'} or $cget) {
	print qq|
	コメント&lt;BR&gt;<BR>
	&lt;INPUT type=&quot;text&quot; size=&quot;25&quot; name=&quot;com&quot;&gt;&lt;BR&gt;&lt;BR&gt;<BR>
	|;
}

print <<EOF;
$button&lt;BR&gt;&lt;BR&gt;<BR>
&lt;/DIV&gt;<BR>
&lt;/DIV&gt;<BR>
&lt;SPAN style=&quot;width:100%;text-align:right;padding-top:3px;&quot;&gt;<BR>
$rslink<BR>
&lt;A href=&quot;$fpath?mode=old&quot;&gt;<BR>
&lt;IMG src=&quot;$idir$od_img&quot; border=&quot;0&quot; alt=&quot;過去の投票&quot; title=&quot;過去の投票&quot;&gt;&lt;/A&gt<BR>
&lt;A href=&quot;$web&quot; target=&quot;_blank&quot;&gt;<BR>
&lt;IMG src=&quot;$idir$dw_img&quot; border=&quot;0&quot; alt=&quot;Petit Poll SE ダウンロード&quot;&gt;&lt;/A&gt<BR>
&lt;A href=&quot;$fpath&quot;&gt;<BR>
&lt;IMG src=&quot;$idir$ad_img&quot; border=&quot;0&quot; alt=&quot;管理&quot; title=&quot;管理&quot;&gt;&lt;/A&gt<BR>
&lt;/SPAN&gt;<BR>
&lt;/DIV&gt;<BR>
&lt;/FORM&gt;<BR>
<BR>
</DIV>
EOF

if ($FORMS{'mode'} eq "nmk") {
	print qq|
	<FORM method="POST" action="$fpath">
	<INPUT type="hidden" name="mode" value="admin">
	<INPUT type="hidden" name="act" value="1">
	<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
	<INPUT type="submit" value="戻る">
	</FORM>
	|;
}
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃投票処理
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub on_poll {
#ログを定義
my $ptlog = $ldir . $ptname;
my $idlog = $ldir . $FORMS{'id'} . ".log";

unless (-e $idlog) { &error ("呼び出された投票は削除されています"); }

if ($SET{'lkey'}) { if (!&lock_on) { &error ("サーバーが混み合っています"); } }
$now_lock = 1;

if (!open (ID, "<$idlog")) { &error ("投票ログが開けませんでした"); }

my @OLDID = <ID>;

close (ID);

#設定ラインを抜く
chomp (my $setline = shift (@OLDID));

#投票数/質問/閲覧制限/コメント取得/コメント限界/連禁/連禁期間/連禁単位/終了秒数/限界投票/開始時刻/終了時刻/ingフラグ
my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split(/<>/, $setline);

#投票期間チェック
if ($period and ($ing == 1) and ($time >= $period)) {
	#投票タイトルログ更新
	my @NEWPT=();
	if (!open (PT, "+<$ptlog")) { &error("投票タイトルログが開けませんでした"); }
		while (chomp ($_ = <PT>)){
			my ($id, $ptitle, $ing) = split(/<>/);
			if ($FORMS{'id'} eq $id) {
				push (@NEWPT, "$id<>$ptitle<>2\n");
			} else {
				push (@NEWPT, "$_\n");
			}
		}

	#IDログ更新
	if (!open (ID, "+<$idlog")) { &error ("投票ログが開けませんでした"); }
	seek (ID, 0, 0);
	print ID "$count<>$qst<>$reye<>$cget<>$climit<>$pkick<>$kval<>$kunit<>$period<>$plimit<>$start<>$end<>2\n";
	print ID @OLDID;
	truncate (ID, tell);
	close (ID);

	seek (PT, 0, 0);
	print PT @NEWPT;
	truncate (PT, tell);
	close (PT);

	if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

	&error ("この投票は終了しました");
}

#進行状況チェック
if ($ing == 2) { &error ("この投票は終了しました"); }

#投票項目チェック
if (!$FORMS{'poll'}) { &error ("投票項目がチェックされていません"); }

#アクセス拒否
my $ip  = $ENV{'REMOTE_ADDR'};
my $ip2 = $ip;
$ip2 =~ s/(\d+\.\d+\.\d+)\.\w+/$1/;

if ($SET{'hkick'} =~ /$ip2/) { &error ("投票が許可されていません"); }

#コメントチェック
if ($FORMS{'com'} eq "undefined" or !$FORMS{'com'}) {
	$FORMS{'com'} = "none";
}
if (($cget == 2) and ($FORMS{'com'} eq "none")) {
	&error ("選択項目へのコメントは必須です");
}
if (length ($FORMS{'com'}) > ($SET{'cleng'} * 2)) {
	&error ("コメントは全角で$SET{'cleng'}字以内までです");
}
if ($FORMS{'com'} eq "none") {
	undef ($FORMS{'com'});
}

#閲覧制限＆連続投票チェック
my ($getcook) = &get_cook (1, $pkick, $kval, $kunit) if (!$reye or $pkick);

#投票数
$count ++;

my $com_ct = 0;		#コメント数
my @ID = ();

#選択項目をインクリ＆コメント追加
while (chomp ($_ = shift (@OLDID))) {
	#ID親/ID子/選択肢orコメント/投票時間/ホスト/投票数orコメント＃
	my ($idno, $idsel, $idq, $idj, $idh, $idct) = split(/<>/);

	#投票先を捜索
	if (($idno eq $FORMS{'poll'}) or ($idsel eq $FORMS{'poll'})) {
		#選択肢ライン更新（親）
		if ($idno eq $FORMS{'poll'}) {
			$idct ++;
			push (@ID, "$idno<><>$idq<><><>$idct\n");
	
			#コメント追加
			if ($FORMS{'com'}) {
				push (@ID, "<>$idno<>$FORMS{'com'}<>$time<>$ip<>$count\n");
				$com_ct = 1;		#コメントカウント
			}
		}else{
			#コメントライン追加（子）＆コメント限界チェック
			if ($climit > $com_ct) {
				push (@ID, "$_\n");
				$com_ct ++;
			}
		}
	} else {
		#無投票配列
		push (@ID, "$_\n");
	}
}

#限界投票チェック
if ($plimit and ($count >= $plimit)){
	my @NEWPT=();
	if (!open (PT, "+<$ptlog")) { &error("投票タイトルログが開けませんでした"); }
		while (chomp ($_ = <PT>)){
			my ($id, $ptitle, $ing) = split(/<>/, $_);

			if ($id eq $FORMS{'id'}) {
				push (@NEWPT, "$id<>$ptitle<>2\n");
			} else {
				push (@NEWPT, "$_\n");
			}
		}

	#終了日を定義
	&opening;

	#結果表示用の日付
	$end = $FORMS{'start'};

	if (!open (ID, "+<$idlog")) { &error ("投票ログが開けませんでした"); }
	seek (ID, 0, 0);
	print ID "$count<>$qst<>$reye<>$cget<>$climit<>$pkick<>$kval<>$kunit<>$period<>$plimit<>$start<>$end<>2\n";
	print ID @ID;
	truncate(ID,tell);
	close(ID);

	seek (PT, 0, 0);
	print PT @NEWPT;
	truncate (PT, tell);
	close (PT);
} else {
	#通常更新
	if (!open (ID, "+<$idlog")) { &error ("投票ログが開けませんでした"); }
	seek (ID, 0, 0);
	print ID "$count<>$qst<>$reye<>$cget<>$climit<>$pkick<>$kval<>$kunit<>$period<>$plimit<>$start<>$end<>$ing\n";
	print ID @ID;
	truncate(ID,tell);
	close(ID);
}

if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

#クッキー設定
if (!$reye or $pkick) { &set_cook ($getcook); }

if ($SET{'stype'} == 1) {
	my @TMP = map {(split /<>/)[5]} @ID;
	@ID = @ID[sort{$TMP[$b] <=> $TMP[$a]} 0 .. $#TMP];
} elsif ($SET{'stype'} == 2) {
	my @TMP = map {(split /<>/)[5]} @ID;
	@ID = @ID[sort{$TMP[$a] <=> $TMP[$b]} 0 .. $#TMP];
}

#小窓使用未使用の分岐
my $cpflag = 0;
if ($SET{'rtype'}) {
	&head (1, "投票結果");
	$cpflag = 1;
} else {
	&head (0);
}

&rs_table_top ($count, $qst, $start, $end);

print qq|<OL type="A">\n|;

my ($num);
while (chomp ($_ = shift (@ID))) {
	#選択肢＃（親） / 選択肢＃（子） / 選択肢 / 投票秒数 / ホスト / 投票数 or 投票番号
	my ($idno, $idsel, $idq, $idj, $idh, $idct) = split(/<>/);

	my $rate = 1.7;
	if ($SET{'rtype'}) { $rate = 3; }
	my $per = sprintf ("%.1f", ($idct * 100) / $count);		#パーセンテージ
	my $wid = sprintf ("%d", $per * $rate);				#画像幅
	if (!$GAZOU[$num]) { $num = 0; }				#バー画像＃

	#親のみ展開
	if ($idno) {
		print "<LI>$idq<BR>\n";
		if ($wid >= 0) {
			if ($wid <= 0) { $wid = 1; }
			print qq|
				<IMG src="$idir$GAZOU[$num]" width="$wid" height="$SET{'bhi'}" alt="$per\%">
				<SPAN style="font-size:12px;">($idct票/$per%)</SPAN><BR><BR></LI>\n
				|;
		} else {
			print qq|
				<IMG src="$idir$GAZOU[$num]" width="1" height="$SET{'bhi'}" alt="0\%">
				<SPAN style="font-size:12px;">(0票/0%)</SPAN><BR><BR></LI>\n
				|;
		}
		$num++;
	}
}

print "</OL>\n";

&rs_table_bottom ($FORMS{'id'}, $cget, 1);

print "</DIV></DIV>\n";

&foot ($cpflag);
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃投票結果
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub result {
#ログを定義
my $ptlog = $ldir . $ptname;
my $idlog = $ldir . $FORMS{'id'} . ".log";

unless (-e $idlog) { &error ("呼び出された投票は削除されています"); }

if (!open (ID, "+<$idlog")) { &error("投票ログを開けませんでした"); }

my @ID = <ID>;

#設定ラインを抽出
chomp (my $setline = shift (@ID));

#投票数/質問/閲覧制限/コメント取得/コメント限界/連禁/連禁期間/連禁単位/終了秒数/限界投票/開始時刻/終了時刻/ingフラグ
my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split (/<>/, $setline);

#閲覧制限チェック
my ($getcook, $ckflag) = &get_cook if (!$reye and $ing == 1);

if (!$reye and !$ckflag and !$FORMS{'r'} and $ing ==1) { &error ("投票前の結果の閲覧が制限されています"); }

#投票期間チェック
if ($ing == 1 and $period and $time >= $period and !$FORMS{'r'}){
	if ($SET{'lkey'}) { if (!&lock_on) { &error ("サーバーが混み合っています"); } }
	$now_lock = 1;

	my @NEWPT = ();
	if (!open (PT, "+<$ptlog")) { &error("投票タイトルログが開けませんでした"); }
		while (chomp ($_ = <PT>)){
			my ($id, $ptitle, $ing) = split(/<>/);

			if ($id eq $FORMS{'id'}) {
				push (@NEWPT, "$id<>$ptitle<>2\n");
			} else {
				push (@NEWPT, "$_\n");
			}
		}
		seek (PT, 0, 0);
		print PT @NEWPT;
		truncate (PT, tell);
	close(PT);

	#IDログ更新
	seek(ID, 0, 0);
	print ID "$count<>$qst<>$reye<>$cget<>$climit<>$pkick<>$kval<>$kunit<>$period<>$plimit<>$start<>$end<>2\n";
	print ID @ID;
	truncate (ID, tell);
	close (ID);

	if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }
}

if ($SET{'stype'} == 1) {
	my @TMP = map {(split /<>/)[5]} @ID;
	@ID = @ID[sort{$TMP[$b] <=> $TMP[$a]} 0 .. $#TMP];
} elsif ($SET{'stype'} == 2) {
	my @TMP = map {(split /<>/)[5]} @ID;
	@ID = @ID[sort{$TMP[$a] <=> $TMP[$b]} 0 .. $#TMP];
}

#小窓使用未使用の分岐
my $cpflag = 0;
if ($SET{'rtype'} or $FORMS{'r'}) {
	&head (1, "投票結果");
	$cpflag = 1;
} else {
	&head (0);
}

&rs_table_top ($count, $qst, $start, $end);

print qq|<OL type="A">\n|;

$count ||= 1;

my ($num);
while (chomp ($_ = shift (@ID))) {
	#選択肢＃（親） / 選択肢＃（子） / 選択肢 / 投票秒数 / ホスト / 投票数 or 投票番号
	my ($idno, $idsel, $idq, $idj, $idh, $idct) = split(/<>/);

	my $rate = 1.7;
	if ($SET{'rtype'} or $FORMS{'wide'} or $FORMS{'r'}) { $rate = 3; }

	my $per = sprintf ("%.1f", ($idct * 100) / $count);		#パーセンテージ
	my $wid = sprintf ("%d", $per * $rate);				#画像幅
	if (!$GAZOU[$num]) { $num = 0; }				#バー画像＃

	#親のみ展開
	if ($idno) {
		print "<LI>$idq<BR>\n";
		if ($wid >= 0) {
			if ($wid <= 0) { $wid = 1; }
			print qq|
				<IMG src="$idir$GAZOU[$num]" width="$wid" height="$SET{'bhi'}" alt="$per\%">
				<SPAN style="font-size:12px;">($idct票/$per%)</SPAN><BR><BR></LI>\n
				|;
		} else {
			print qq|
				<IMG src="$idir$GAZOU[$num]" width="1" height="$SET{'bhi'}" alt="0\%">
				<SPAN style="font-size:12px;">(0票/0%)</SPAN><BR><BR></LI>\n
				|;
		}
		$num++;
	}
}

print "</OL>\n";

&rs_table_bottom ($FORMS{'id'}, $cget, 1);

print "</DIV></DIV>\n";

&foot ($cpflag);
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃投票結果テーブル
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub rs_table_top {
my ($count, $qst, $start, $end, $mikey) = @_;

#拡大縮小アイコン
my $wd_icon = <<WIDE;
<SPAN style="text-align:right;width:100%">
<A href="javascript:WideWin('$FORMS{'id'}');"><IMG src="$idir$wn_img" border="0" alt="拡大縮小"></A>
</SPAN>
WIDE

my ($wwid);
if ($mikey) {
	$wwid = "330px";
	undef ($wd_icon);
} elsif ($SET{'rtype'} or $FORMS{'cdkey'} or $FORMS{'r'}) {
	$wwid = "500px";
	undef ($wd_icon);
} else {
	$wwid = "100%";
}

print <<EOF;
<DIV style="font-size:13px;width:$wwid;background-color:$SET{'rback1'};border:solid 1px $SET{'rback2'};padding:3px;">
<DIV style="width:100%;color:$SET{'rfont1'};text-align:left;padding-bottom:3px;">
<SPAN style="width:90%;text-align:left;float:left;">
<IMG src="$idir$qs_img" alt="質問">
$qst
</SPAN>
$wd_icon
</DIV>
<DIV style="clear:left;width:100%;text-align:left;background-color:$SET{'rback2'};color:$SET{'rfont2'};border-top:solid 2px $SET{'rshadow'};border-left:solid 2px $SET{'rshadow'};padding:3px;">
<DIV class="period">[投票期間] $start ～ $end [投票数] $count票</DIV>

EOF
}

sub rs_table_bottom {
my ($id, $cget, $cvflag) = @_;

print <<EOF;
<FORM action="$fpath" method="POST">
<DIV align="center">
EOF

#過去ログ閲覧キー/通常時CLOSE/戻るボタン
my ($root, $back, $p, $close);
if ($FORMS{'r'}) {
	$root = qq|<INPUT type="hidden" name="r" value="1">|;
	$back = qq|<INPUT type="button" value="戻る" onClick="javascript:history.back()">|;
} else {
	if (!$SET{'rtype'}) {
		$close = qq|<INPUT type="button" value="閉じる" onClick="javascript:window.close();">|;
	} else {
		$back = qq|<INPUT type="button" value="戻る" onClick="javascript:history.back()">|;
	}
}

#コメントボタン
if (!$SET{'ctype'} and $cget and $cvflag) {
	print qq|
		<INPUT type="hidden" name="mode" value="cview">
		<INPUT type="hidden" name="id" value="$id">
		<INPUT type="hidden" name="wide" value="$FORMS{'wide'}">
		$root
		<INPUT type="submit" value="コメントを見る">
		$back
		|;
} elsif ($FORMS{'mode'} eq "cview" and !$FORMS{'r'} and !$SET{'rtype'}) {
	print qq|
		<INPUT type="hidden" name="mode" value="result">
		<INPUT type="hidden" name="id" value="$id">
		<INPUT type="hidden" name="wide" value="$FORMS{'wide'}">
		$root
		<INPUT type="submit" value="戻る">
		|;
} elsif ($back) {
	print "$back\n";
}

#著作権部削除・改編厳禁！！
print <<EOF;
$close
</FORM>
</DIV>
<SPAN style="text-align:right;width:100%;">
<A href="$web" target="_blank"><IMG src="$idir$dw_img" alt="Petit Poll SE ダウンロード" border="0"></A>
</SPAN>

EOF
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃コメント閲覧
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub com_view {
if (!$FORMS{'id'}) { ($FORMS{'id'}, $FORMS{'pass'}, $FORMS{'cdkey'}) = @_; }

if ($SET{'ctype'} and !$FORMS{'cdkey'}) { &error ("コメントは管理者しか見ることができません"); }

#ログを定義
my $idlog = $ldir . $FORMS{'id'} . ".log";

if (!open (ID, "+<$idlog")) { &error("投票ログを開けませんでした"); }

#設定ラインを抽出
chomp (my $setline = <ID>);

#投票数/質問/閲覧制限/コメント取得/コメント限界/連禁/連禁期間/連禁単位/終了秒数/限界投票/開始時刻/終了時刻/ingフラグ
my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split (/<>/, $setline);

if (!$cget) { &error ("コメント取得機\能\は使用していません"); }

#小窓使用未使用の分岐
my $cpflag = 0;
if ($FORMS{'cdkey'}) {
	&head (1, "コメント削除画面");
	$cpflag = 1;
} elsif ($SET{'rtype'} or $FORMS{'r'}) {
	&head (1, "コメント閲覧");
	$cpflag = 1;
} else {
	&head (0);
}

#削除モード 前タグ挿入
if ($FORMS{'cdkey'}) {
	print qq|
		<DIV style="width:400px;text-align:left;line-height:18px;">
		*削除したいコメントをチェックして削除ボタンを押すと削除することが出来ます。<BR>
		*ホスト制限を行いたい場合、削除前にカッコ内の数字をメモしておいて下さい。<BR>
		*送信後のやり直しはできませんので注意してください。（確認画面は出ません）
		</DIV>
		<BR>
		<BR>

		<FORM method="POST" action="$fpath">\n
		|;
}

&rs_table_top ($count, $qst, $start, $end);
$count ||= 1;

my ($r, $chflag, $new_com, $del_box, $host);

while (chomp ($_ = <ID>)) {
	#選択肢＃（親） / 選択肢＃（子） / 選択肢 / 投票秒数 / ホスト / 投票数 or 投票番号
	my ($idno, $idsel, $idq, $idj, $idh, $idct) = split(/<>/);

	if (!$r and $idno) {
		#先頭
		print qq|
			<BR><BR>
			<DIV class="com1">■$idq</DIV>
			<OL type="disc">
			|;
		$r = $idno;
	} elsif ($idno) {
		if ($chflag) {
			#次親（前親にコメント有り）
			print qq|
				</OL>
				|;
		} else {
			#次親（前親にコメント無し）
			print qq|
				<LI class="com2">コメントはまだありません</LI>
				</OL>
				|;
		}

		print qq|
			<BR><BR>
			<DIV class="com1">■$idq</DIV>
			<OL type="disc">
			|;

		#ルート更新、フラグゼロ
		$r = $idno;
		$chflag = 0;
		next;
	} elsif ($r eq $idsel) {
		#コメント
		if ($time < ($idj + ($SET{'nmark'} * 60 * 60))) {
			$new_com = qq |<IMG src="$idir$nw_img" alt="新着">|;
		}

		#削除モード専用ボタン＆ホスト表示
		if ($FORMS{'cdkey'}) {
			$del_box = qq|<INPUT type="checkbox" name="delarray" value="$idct">|;
			$host = qq|<SPAN class="em_font">（$idh）</SPAN>|;
		}

		print qq|<LI class="com2">$del_box $idq $host $new_com</LI>\n|;
		$chflag = 1;
		undef ($new_com);
	}

}

close (ID);

if (!$chflag) {
	print qq|
		<LI class="com2">コメントはまだありません</LI>
		</OL><BR><BR>
		|;
} else {
	print "</OL><BR><BR>\n";
}

if (!$FORMS{'cdkey'}) {
	&rs_table_bottom ($FORMS{'id'}, $cget, 0);
} else {
	#削除モード 後タグ挿入
	print qq|
		<DIV align="center">
		<TABLE cellpadding="0" cellspacing="3" border="0" summary="ボタン">
		<TR><TD>
		<INPUT type="hidden" name="mode" value="comdel">
		<INPUT type="hidden" name="id" value="$FORMS{'id'}">
		<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
		<INPUT type="hidden" name="cdkey" value="$FORMS{'cdkey'}">
		<INPUT type="submit" value="コメント削除">
		</FORM>
		</TD><TD>
		<FORM method="POST" action="$fpath">
		<INPUT type="hidden" name="mode" value="maint">
		<INPUT type="hidden" name="id" value="$FORMS{'id'}">
		<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
		<INPUT type="submit" value="メンテナンス画面">
		</FORM>
		</TABLE>
		</DIV>\n
		|;
}

print "</DIV></DIV>\n";

&foot ($cpflag);
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃メンテナンス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub maint {
#再入室キーを取得
my ($id, $pass) = @_ if (!$FORMS{'act'});

#再入室対策でモードを固定
$FORMS{'mode'} = "maint";

if ($FORMS{'pass'} ne $SET{'pass'}) {
	&error("不正なアクセスです");
} elsif (!$FORMS{'id'}) {
	&error ("編集ボタンにチェックが入っていません");
}

#ログを定義
my $idlog = $ldir . $FORMS{'id'} . ".log";

unless (-e $idlog) { &error ("呼び出された投票は削除されています"); }

if (!open (ID, "+<$idlog")) { &error("投票ログが開けませんでした"); }

chomp (my $setline = <ID>);

#投票数/質問/閲覧制限/コメント取得/コメント限界/連禁/連禁期間/連禁単位/終了秒数/限界投票/開始時刻/終了時刻/ingフラグ
my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split (/<>/, $setline);

&head (1, "メンテナンス画面");

print <<EOF;
<SPAN style="width:500px;text-align:left;line-height:18px;">
*「設定変更」から、各種設定を変更するためのフォームへ行くことが出来ます。<BR>
*「コメント削除画面」では、コメントの閲覧、削除を行うことが出来ます。<BR>
*コメントの有無を変更した場合、小窓の使用未使用を変更した場合は\ソ\ースを交換してください。<BR>
*「投票リセット」すると、投票作成時の状態に戻します。（投票数ゼロで設定はデフォルト）<BR>
*「投票終了」すると、この場で過去ログ化することができます。<BR>
*「投票削除」すると、この投票が完全に削除されます。<BR>
*送信後のやり直しはできませんのでご注意ください。（確認画面は出ません）<BR>
</SPAN>
<BR>
<BR>
<BR>

<TABLE cellpadding="0" cellspacing="3" botder="0" summary="設定メニュー">
<TR>
<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="admin">
<INPUT type="hidden" name="act" value="1">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="管理ホーム">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="edit">
<INPUT type="hidden" name="ing" value="$ing">
<INPUT type="hidden" name="id" value="$FORMS{'id'}">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="設定変更">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="cview">
<INPUT type="hidden" name="cdkey" value="1">
<INPUT type="hidden" name="id" value="$FORMS{'id'}">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="コメント削除画面">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="re_set">
<INPUT type="hidden" name="id" value="$FORMS{'id'}">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="投票リセット">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="p_end">
<INPUT type="hidden" name="id" value="$FORMS{'id'}">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="投票終了">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="p_del">
<INPUT type="hidden" name="id" value="$FORMS{'id'}">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="投票削除">
</FORM>
</TD>
</TR>
</TABLE>
<BR>

EOF

&pre ($reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing);

&rs_table_top ($count, $qst, $start, $end, 1);

print qq|<OL type="A">\n|;

$count ||= 1;

my ($num, @SEL);
while (chomp ($_ = <ID>)) {
	#選択肢＃（親） / 選択肢＃（子） / 選択肢 / 投票秒数 / ホスト / 投票数 or 投票番号
	my ($idno, $idsel, $idq, $idj, $idh, $idct) = split(/<>/);

	my $per = sprintf ("%.1f", ($idct * 100) / $count);		#パーセンテージ
	my $wid = sprintf ("%d", $per * 1.7);				#画像幅
	if (!$GAZOU[$num]) { $num = 0; }				#バー画像＃

	#親のみ展開
	if ($idno) {
		print "<LI>$idq<BR>\n";
		if ($wid >= 0) {
			if ($wid <= 0) { $wid = 1; }
			print qq|
				<IMG src="$idir$GAZOU[$num]" width="$wid" height="$SET{'bhi'}" alt="$per\%">
				<SPAN style="font-size:12px;">($idct票/$per%)</SPAN><BR><BR></LI>\n
				|;
		} else {
			print qq|
				<IMG src="$idir$GAZOU[$num]" width="1" height="$SET{'bhi'}" alt="0\%">
				<SPAN style="font-size:12px;">(0票/0%)</SPAN><BR><BR></LI>\n
				|;
		}
		$num++;
		push (@SEL, "$idq\n");
	}
}

print <<EOF;
</OL>
</DIV></DIV>

<BR>
<BR>
<SCRIPT type="text/javascript">
<!--
function conversion (ID) {
	answer=document.getElementById(ID);
	if(answer.className == "offbox"){
		answer.className = "onbox";
	}else{
		answer.className = "offbox";
	}
}
//-->
</SCRIPT>

<HR style="height:1px;color:$SET{'hfont'};width:85%">
<SPAN onclick="conversion('on')" onMouseover="this.style.color=\'$SET{'hlink'}\'" onMouseout="this.style.color=\'$SET{'alink'}\'" style="color:$SET{'alink'};cursor:hand;">
&lt;ソ\ースを表\示する&gt;
</SPAN><BR>
<DIV id="on" class="offbox">
EOF

&sourse ($qst, $cget, @SEL);

print <<EOF;
</DIV>
<HR style="height:1px;color:$SET{'hfont'};width:85%">
EOF

&foot (1);
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃設定変更
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub relog {
if ($FORMS{'climit'} =~ /\D/) { &error ("限界コメント数に無効な数値が含まれています"); }
if ($FORMS{'plimit'} =~ /\D/) { &error ("限界投票数に無効な数値が含まれています"); }
if ($FORMS{'kval'}   =~ /\D/) { &error ("連続投票禁止期間に無効な数値が含まれています");}

my $idlog = $ldir . $FORMS{'id'} . ".log";

if ($SET{'lkey'}) { if (!&lock_on) { &error ("サーバーが混み合っています"); } }
$now_lock = 1;

if (!open (ID, "+<$idlog")) { &error("投票ログが開けませんでした"); }

my @ID = <ID>;

chomp (my $setline = shift (@ID));

#投票数/質問/閲覧制限/コメント取得/コメント限界/連禁/連禁期間/連禁単位/終了秒数/限界投票/開始時刻/終了時刻/ingフラグ
my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split (/<>/, $setline);

#終了日
&finale;

#限界コメント
if (!$FORMS{'climit'}) { $FORMS{'climit'} = 5;}

#限界投票数のチェック
if ($FORMS{'plimit'} and $FORMS{'plimit'} < $count) { &error ("指定された限界投票数は既に超えています"); }

#コメントラインのチェックと削除
my (@NEWID, $ct);
if ($FORMS{'cget'} and ($climit >= $FORMS{'climit'})) {
	while (chomp ($_ = shift (@ID))) {
		my ($idno, $idsel, $idq, $idj, $idh, $idct) = split (/<>/);

		if ($idno) {
			push (@NEWID, "$_\n");
			$ct = 0;
		} elsif ($idsel and ($ct < $FORMS{'climit'})) {
			push (@NEWID, "$_\n");
			$ct ++;
		} else {
			next;
		}
	}

	seek (ID, 0, 0);
	print ID "$count<>$qst<>$FORMS{'reye'}<>$FORMS{'cget'}<>$FORMS{'climit'}<>$FORMS{'pkick'}<>$FORMS{'kval'}<>$FORMS{'kunit'}<>$FORMS{'period'}<>$FORMS{'plimit'}<>$start<>$FORMS{'end'}<>1\n";
	print ID @NEWID;
	truncate (ID, tell);
	close (ID);

	if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

	&maint ($FORMS{'id'}, $FORMS{'pass'});
}

seek (ID, 0, 0);
print ID "$count<>$qst<>$FORMS{'reye'}<>$FORMS{'cget'}<>$FORMS{'climit'}<>$FORMS{'pkick'}<>$FORMS{'kval'}<>$FORMS{'kunit'}<>$FORMS{'period'}<>$FORMS{'plimit'}<>$start<>$FORMS{'end'}<>1\n";
print ID @ID;
truncate (ID, tell);
close (ID);

if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

&maint ($FORMS{'id'}, $FORMS{'pass'});
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃コメント削除処理
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub com_delete {
my $idlog = $ldir . $FORMS{'id'} . ".log";

if ($SET{'lkey'}) { if (!&lock_on) { &error ("サーバーが混み合っています"); } }
$now_lock = 1;

if (!open (ID, "+<$idlog")) { &error ("投票ログが開けませんでした"); }

chomp (my $setline = <ID>);

my (@NEWID, $dlflag, $val);
while (chomp ($_ = <ID>)) {
	my ($idno, $selid, $idq, $idj, $idh, $idct) = split(/<>/);

	#コメントのみ削除
	if (!$idno) {
		foreach $val (@DEL) {
			if ($idct eq $val){
				$dlflag = 1;
				last;
			}
		}

		#対象外
		if (!$dlflag) { push (@NEWID, "$_\n"); }
	} else {
		#選択肢
		push (@NEWID, "$_\n");
	}

	undef ($dlflag);
}

seek (ID, 0, 0);
print ID "$setline\n";
print ID @NEWID;
truncate (ID, tell);
close (ID);

if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

&com_view ($FORMS{'id'}, $FORMS{'pass'}, $FORMS{'cdkey'});
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃投票リセット
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub re_set {
my $ptlog = $ldir . $ptname;
my $idlog = $ldir . $FORMS{'id'} . ".log";

if ($SET{'lkey'}) { if (!&lock_on) { &error ("サーバーが混み合っています"); } }
$now_lock = 1;

if (!open (ID, "+<$idlog")) { &error ("投票ログが開けませんでした"); }

chomp (my $setline = <ID>);

#投票数/質問/閲覧制限/コメント取得/コメント限界/連禁/連禁期間/連禁単位/終了秒数/限界投票/開始時刻/終了時刻/ingフラグ
my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split (/<>/, $setline);

#開始日
&opening;

#選択肢取得
my @ID = ();
while (chomp ($_ = <ID>)) {
	my ($idno, $selid, $idq, $idj, $idh,  $idc) = split (/<>/);

	if ($idno) { push (@ID, "$idno<><>$idq<><><>0\n"); }
}

#投票タイトルログ更新
if ($ing != 0) {
	my @PT = ();
	if (!open (PT, "+<$ptlog")) { &error ("投票タイトルログが開けませんでした"); }
		while (chomp ($_ = <PT>)){
			my ($id, $ptitle, $ing) = split (/<>/, $_);
	
			if ($id eq $FORMS{'id'}) {
				push (@PT, "$id<>$ptitle<>1\n");
			} else {
				push (@PT, "$_\n");
			}
		}
	
	seek (PT, 0, 0);
	print PT @PT;
	truncate (PT, tell);
	close (PT);
}

seek (ID, 0, 0);
print ID "0<>$qst<>1<>0<>5<>0<>0<>0<>0<>0<>$FORMS{'start'}<>無期限<>1\n";
print ID @ID;
truncate (ID, tell);

close (ID);

if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

&maint ($FORMS{'id'}, $FORMS{'pass'});
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃投票終了
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub poll_end {
my $ptlog = $ldir . $ptname;
my $idlog = $ldir . $FORMS{'id'} . ".log";

if ($SET{'lkey'}) { if (!&lock_on) { &error ("サーバーが混み合っています"); } }
$now_lock = 1;

#PTログ更新
my @PT = ();
if (!open (PT, "+<$ptlog")) { &error("投票タイトルログが開けませんでした"); }
	while (chomp ($_ = <PT>)) {
		my ($id, $ptitle, $ing) = split(/<>/);

		if ($id eq $FORMS{'id'}) {
			push (@PT, "$id<>$ptitle<>2\n");
		} else {
			push (@PT, "$_\n");
		}
	}

	#IDログ更新
	if (!open (ID, "+<$idlog")) { &error("投票ログが開けませんでした"); }

	my @ID = <ID>;
	
	chomp (my $setline = shift (@ID));
	
	#投票数/質問/閲覧制限/コメント取得/コメント限界/連禁/連禁期間/連禁単位/終了秒数/限界投票/開始時刻/終了時刻/ingフラグ
	my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split (/<>/, $setline);

	#終了日を定義
	&opening;

	seek (ID, 0, 0);
	print ID "$count<>$qst<>$reye<>$cget<>$climit<>$pkick<>$kval<>$kunit<>$period<>$plimit<>$start<>$FORMS{'start'}<>2\n";
	print ID @ID;
	truncate (ID, tell);
	close (ID);

seek (PT, 0, 0);
print PT @PT;
truncate(PT, tell);
close (PT);

if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

&maint ($FORMS{'id'}, $FORMS{'pass'});
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃投票削除
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub poll_del {
my $ptlog = $ldir . $ptname;
my $idlog = $ldir . $FORMS{'id'} . ".log";

if ($SET{'lkey'}) { if (!&lock_on) { &error ("サーバーが混み合っています"); } }
$now_lock = 1;

my @PT = ();
if (!open (PT, "+<$ptlog")) { &error ("投票タイトルログが開けませんでした"); }
	while (chomp ($_ = <PT>)) {
		my ($id, $ptitle, $ing) = split (/<>/);

		if ($id eq $FORMS{'id'}) {
			push (@PT, "$id<>$ptitle<>0\n");

			if (-e $idlog) { unlink ("$idlog"); }
		} else {
			push (@PT, "$_\n");
		}
	}

seek (PT, 0, 0);
print PT @PT;
truncate (PT, tell);
close(PT);

if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

#削除後対策のため、再入室キーを削除
undef ($FORMS{'act'});

&admin ($FORMS{'pass'});
&foot (1);
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃過去ログ
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub old {
my $ptlog = $ldir . $ptname;

unless (-e $ptlog) { &error ("この投票の利用は休止されています"); }

#現在行われている投票タイトルを取得
if (!open(PT, "<$ptlog")) { &error ("過去ログが開けませんでした"); }

&head (1, "過去投票");

print <<EOF;
*投票タイトルをクリックすると最終結果をご覧になれます。
<BR>
<BR>

<DIV class="oframe">
<TABLE cellpadding="3" cellspacing="1" border="0" summary="リスト">
<TR>
<TD class="pline1" style="width:40px;">ID</TD>
<TD class="pline1" style="width:400px;">投票タイトル</TD>
</TR>
EOF

my $odflag = 0;
while (chomp ($_ = <PT>)) {
	my ($id, $ptitle, $ing) = split (/<>/);

	if ($ing == 2) {
		print qq|<TR><TD class="pline2">$id</TD>|;
		print qq|<TD class="pline2"><A href="$fpath?mode=result&amp;id=$id&amp;r=old">$ptitle</TD></TR>|;

		$odflag= 1;
	}
}

close(PT);

if (!$odflag) {
	print qq|
		<TR><TD class="pline2">-</TD>
		<TD class="pline2">終了した投票はありません</TD></TR>
		</TABLE>
		</DIV>
		|;
}

print <<EOF;
</TABLE></DIV>
<BR>
<BR>
<FORM>
<DIV align="center">
<INPUT type="button" value="戻る" onClick="javascript:history.back()">
</DIV>
</FORM>

EOF

&foot (1);
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃投票全削除
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub use_end {
my $ptlog = $ldir . $ptname;

if ($SET{'lkey'}) { if (!&lock_on) { &error ("サーバーが混み合っています"); } }
$now_lock = 1;

#投票タイトルログを初期化
if (!open (PT, "+<$ptlog")) { &error ("投票タイトルログを開けませんでした"); }

my @PT = <PT>;
my $on = @PT;

seek (PT, 0, 0);
truncate (PT, tell);
close (PT);

#各投票ログを全削除
my ($i);
for ($i = 1; $i <= $on; $i ++) {
	my $idlog = $ldir . $i . ".log";
	if (-e $idlog) { unlink ("$idlog"); }
	undef ($idlog);
}

if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

#削除後対策のため、再入室キーを削除
undef ($FORMS{'act'});

&admin ($FORMS{'pass'});
&foot (1);
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃開始日
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub opening {
my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime ($time);

$mon++;
$year += 1900;
$year = substr ("$year", 2);

$FORMS{'start'} = sprintf ("%s/%02d/%02d", $year, $mon, $mday);
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃終了日
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub finale {
if (!$FORMS{'period'}) {
	$FORMS{'end'} = "無期限";
	$FORMS{'period'} = 0;
} else {
	$FORMS{'period'} = $time + (60 * 24 * 60 * $FORMS{'period'});
	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime ($FORMS{'period'});

	$mon++;
	$year += 1900;
	$year = substr ("$year", 2);

	$FORMS{'end'} = sprintf ("%s/%02d/%02d", $year, $mon, $mday);
}
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃クッキー取得
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub get_cook {
my ($pcflag, $pkick, $kval, $kunit) = @_;
my ($tani, $kakeru, %COOKIE, $ckflag, $getcook);

if ($pcflag) {
	if (!$kunit) {
		$tani = "分"; $kakeru = 60;
	} elsif ($kunit == 1) {
		$tani = "時間"; $kakeru = 3600;
	} elsif ($kunit == 2) {
		$tani = "日"; $kakeru = 86800;
	}
}

foreach (split (/;/, $ENV{'HTTP_COOKIE'})) {
	my ($key, $val) = split (/=/);
	$COOKIE{$key} = $val;
}

foreach (split (/,/, $COOKIE{'PPSE'})) {
	my ($key, $val) = split (/<>/);

	if ($key eq $FORMS{'id'}) {
		if ($pcflag) {
			if ($pkick and !$kval) {
				&error ("投票は一人一回しかできません");
			} elsif ($val + ($kval * $kakeru) < $time) {
				$val = $time;
			} else {
				&error ("投票は$kval$taniに一回しかできません");
			}
		}

		$ckflag = 1;
	}

	$getcook .= "$key<>$val,";
}

if (!$ckflag and $pcflag) { $getcook .= "$FORMS{'id'}<>$time,"; }

return ($getcook, $ckflag);
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃クッキー設定
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub set_cook {
my ($getcook) = @_;
my @GMT = gmtime (time);
my @MONTH = qw (Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
my @WEEK = qw (Sun Mon Tue Wed Thu Fri Sat);
my $gmt = sprintf ("%s,%02d-%s-%04d %02d:%02d:%02d GMT",
	$WEEK[$GMT[6]], $GMT[3] += 1, $MONTH[$GMT[4]], $GMT[5] += 2000, $GMT[2], $GMT[1], $GMT[0]);

#my $cpath = $ENV{SCRIPT_NAME};
#$cpath =~ s/[^\/]*$//;; path=$cpath

print "Set-Cookie: PPSE=$getcook; expires=$gmt\n";
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃ファイルロック ON
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub lock_on {
my $ngflag = 0;
my $retry = 5;

if (-e $lock and ((stat ($lock))[9] < time - 60)) { rmdir ($lock); }

while (!mkdir ($lock, 0755)) {
	if (--$retry <= 0) { $ngflag = 1; last; }
	sleep (1);
}

if ($ngflag) { return (0); }
else { return (1); }
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃エラー
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub error {
if ($now_lock) { rmdir ($lock); }

print "Content-type:text/html\n\n";

print <<EOF;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML lang="ja">
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<META name="robots" content="NOINDEX, NOFOLLOW">
<META http-equiv="Content-Style-Type" content="text/css">
<TITLE>$_[0]</TITLE>
</HEAD>
<BODY>
<DIV align="center">
<BR><BR>
<DIV style="width:280px;border:solid 1px #666;font-size:13px;color:#666;padding:5px;">
<BR>
ERROR！
<BR><BR>
$_[0]
<BR><BR>
</DIV>
<BR><BR><BR><BR><BR><BR><BR><BR><BR>
</DIV>
</BODY>
</HTML>
EOF

exit;
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃ヘッダー
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub head {
#$hdflag=ヘッダー / $room=ルームネーム
my ($hdflag, $room)= @_;

#ページヘッダー
my $hdline =<<HEAD;
<BR>
<SPAN style="text-align:left;width:85%;"><A href="$SET{'home'}">▼ホームページ▲</A></SPAN>

<DIV class="head">$room</DIV>
<BR>
<BR>

HEAD

#ルームネームとマージン
my ($margin);
if (!$hdflag) {
	undef ($hdline);
	$margin = 0;
} else {
	$margin = 13;
}

#ワイドウィンドウ
my ($wact, $wname, $wkey, $wwin);
if (!$FORMS{'wide'}) {
	$wname = "wide";
	$wkey  = 1;
	$wwin  = 500;
} else {
	$wname = "def";
	$wkey  = 0;
	$wwin  = 330;
}

if ($FORMS{'mode'} eq "cview") {
	$wact = "cview";
} else {
	$wact = "result";
}

print "Content-type:text/html\n\n";

print <<EOF;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML lang="ja">
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<TITLE>$SET{'title'}</TITLE>
<SCRIPT type="text/javascript">
<!--
function WideWin (Id) {
window.open("$fpath?mode=$wact&amp;id="+Id+"&amp;wide=$wkey","$wname","menubar=no, scrollbars=yes, width=$wwin, height=$SET{'whi'}");
window.close();
}
//-->
</SCRIPT>
<STYLE type="text/css">
<!--
BODY {
	background-color:$SET{'bback'};
font-size:12px; color:#333333; font-family:Verdana,Chicago;
	margin:${margin}px;
}

td, th{font-size:12px; color:#333333; font-family:Verdana,Chicago;}

.em_font {
	color:$SET{'efont'};
}

.head {
	width:85%;
	background-color:$SET{'hback'};
	border:solid 1px $SET{'hfont'};
	color:$SET{'hfont'};
	font-weight:bold;
	padding:8px;
}

A{ color:#990000;text-decoration:underline ; cursor:crosshair;}
A:visited { color:#990000;text-decoration:underline ; }
A:active { color:#990000; text-decoration:underline ; }
A:hover { color:#9900FF; text-decoration:underline ; background:#99ffff;}

.oframe {
	width:440px;
	background-color:$SET{'hfont'};
}

.pframe {
	width:480px;
	background-color:$SET{'hfont'};
}

.pline1 {
	background-color:$SET{'hback'};
	color:$SET{'hfont'};
	text-align:center;
}

.pline2 {
	background-color:$SET{'bback'};
	color:$SET{'bfont'};
	text-align:center;
}

.fframe {
	width:600px;
	background-color:$SET{'hfont'};
}

.fleft {
	width:140px;
	background-color:$SET{'hback'};
	color:$SET{'hfont'};
}

.fright {
	width:460px;
	background-color:$SET{'bback'};
	color:$SET{'bfont'};
}

.fleft2 {
	width:190px;
	background-color:$SET{'hback'};
	color:$SET{'hfont'};
}

.fright2 {
	width:410px;
	background-color:$SET{'bback'};
	color:$SET{'bfont'};
}

.sleft {
	width:100px;
	background-color:$SET{'hback'};
	color:$SET{'hfont'};
	text-align:center;
}

.sright {
	width:100px;
	background-color:$SET{'bback'};
	color:$SET{'efont'};
	text-align:center;
}

.sourse {
	width:85%;
	border:solid 1px $SET{'bfont'};
	background-color:$SET{'bback'};
	color:$SET{'bfont'};
	text-align:left;
	padding:10px;
	word-break:break-all;
}

.period {
	width:100%;
	font-size:12px;
	color:$SET{'efont'};
	text-align:right;
}

.com1 {
	border-bottom:dotted 2px $SET{'rback1'};
	padding:3px;
	color:$SET{'rfont2'};
}

.com2 {
	padding:3pt;
	color:$SET{'rfont2'};
}

.onbox{
	display:block;
}

.offbox{
	display:none;
}

.cpstyle {
	width:85%;
	font-size:11px;
	font-family:Lucida Sans Unicode;
	text-align:right;
}
-->
</STYLE>
</HEAD>
<BODY>
<DIV align="center">

$hdline
EOF
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃フッター（削除・改編厳禁）
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub foot {
my ($cpflag) = @_;

#これより以下の部分は削除改変厳禁
if ($cpflag) {
	$cpflag = qq (<BR><DIV class="cpstyle"><A href="$web" target="_blank">Petit Poll SE ver 4.3</A></DIV><BR>);
} else {
	undef ($cpflag);
}

print <<EOF;
$cpflag
</DIV>
</BODY>
</HTML>
EOF

exit;
}



__END__