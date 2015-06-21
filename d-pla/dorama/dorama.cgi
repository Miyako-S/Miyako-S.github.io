#!/usr/bin/perl

#| WeB DoRaMa Version 1.30.08
#| This script is free.
#|
#| Author Shigeto Nakazawa.(1996/11/27)
#| HomePageUrl http://www7.big.or.jp/~jawa/
#|
#| Special Thanks おかぴ
#| HomePgaeUrl ???

# //////////////////////////////////////////////////////////
# オプションの設定を変更することができます。
# 変更する場合は、readme.htm をご覧になってから行ってください。
# 設定変更には充分注意してください。
# //////////////////////////////////////////////////////////

# ----------------------------------------------------------
# ドラマの管理者（あなた）の情報です。
# ----------------------------------------------------------

$admin_name = '虎の穴伸治';               # あなたの名前(ハンドルネーム)
$admin_email = 'indigodays@deen.ne.jp'; # あなたのメールアドレス
$master = 'cosmos';               # 管理用のパスワード

# ----------------------------------------------------------
# ドラマのカスタマイズ項目です。
# ----------------------------------------------------------
# 〇 基本項目

$cgi_title    = 'DEEN days';       # ドラマのタイトル（タグはダメ！）

$body_text    = '#000000';          # <BODY> タグの設定
$body_link    = '#0066ff';          # リンクの色
$body_alink   = '#9933FF';          # クリック中のリンクの色
$body_vlink   = '#FF0099';          # 既にクリック済みのリンクの色
$body_bgcolor = '#ffffff';          # 背景の色
$body_back    = '/dorama/bsflyw.jpg';                 # 背景画像

$back_url = "reco/apeboard_plus.cgi";
                                    # ↑帰りの URL（絶対URL推奨）
$image_dorama = '/dorama/dorama.gif';
                                    # ↑ドラマの画像のある URL

$emb_color = '#FF0000';                                 # 強調色（主に時刻の色）

$limit_log = 200;                   # ログの最大登録数
$view      = 13;                     # 始めに表示するドラマの数
$page      = 80;                    # １ページに表示するドラマの数(^-^;;

$ip_check = 0;                      # IPアドレスの表示 （0:表示しない  1:表示する）
$rh_check = 0;                      # リモートホストの表示 （0:表示しない  1:表示する）

$actedit_pass   = 'guest';          # 出演者エディタのゲストパスワード
$actedit_add    = 1;                # 出演者エディタでゲストが追加できるか(0:できない 1:できる)
$actedit_delete = 0;                # 出演者エディタでゲストが削除できるか(0:できない 1:できる)

# 〇 システム関連項目
                                    # ファイル関連の設定
                                    # 通常はこのままで良い
$method    = 'POST';                # METHOD の設定('POST' or 'GET')
$tz        = 'JST-9';               # TimeZone
$jcode     = './jcode.pl';          # jcode.pl のある場所
$savetype = 0;                      # ログの記録方式 0:Openのみ 1:Temp利用
$logdir    = './';                  # 記録用ファイルの置くディレクトリへのパス（URLじゃないよ）
$logfile   = 'dorama.log';          # 記録用ファイル名
$actfile   = 'dorama.act';          # 出演者用ファイル名
$lock_flag = 1;                     # ロック機構 1:使用 0:不使用

# 〇 セキュリティー項目

@BAD_WORD = ('');
                                    # ↑禁止ワード
$check_url = "http://www.d-planets.org/dorama/dorama.cgi";    # ここにこのCGIの正確な URL (http://～) を書いておくと他サイトから
                    # 不正に投稿されたものを拒否できます。
                    # （イタズラされて、初めて利用すること！）

@check_ipad = (61.26.102.222);   # ここに 登録されたくない方の IPアドレスを書いておくと、
                    # その IPアドレスからの全ての投稿を拒否します。
                    # （イタズラされて、初めて利用すること！）

$check_proxy = 0;   # ここの値を 1 にすると、プロクシ経由で来る匿名な訪問者を
                    # 排除ですきますが、通常の方を排除する可能性もあります。
                    # （イタズラされて、初めて利用すること！）
# 〇 ＨＴＭＬオプション
                                    # HTML関連の設定
# --------------------              # タイトル部分の HTML文
$HTML_TITLE=<<"_EOF_";

<BR>
<CENTER>
<H1><FONT COLOR=$emb_color>●</FONT>
 <I>DEEN days</I>
<FONT COLOR=$emb_color>●</FONT>
</H1></CENTER>
<BR>

_EOF_
# ↑ この _EOF_ はこのままにしておくこと！
# --------------------              # 説明部分の HTML文（上）
$HTML_INFO_TOP =<<"_EOF_";

<CENTER>
<TABLE><TD><TT>
平穏無事だけがいいと限らない？！<Br>
何でもアリの精神で突っ走ろう♪<br>
注:ドラマは上でなく下に続いていきます。<Br>
投稿すると過去のドラマを読むことが出来ます。
</TT></TD></TABLE>
</CENTER>

_EOF_
# ↑ _EOF_ は必須です。

# --------------------              # 説明部分の HTML文（下）
$HTML_INFO_BOTTOM =<<"_EOF_";

<CENTER>
<TABLE><TD><TT><FONT COLOR=$emb_color>
〇 <B>注意</B><BR>
タグを使ったり、全角150字を超えると登録されません。<BR>
同じ出演者が続けて発言することはできません。
</FONT></TT></TD></TABLE>
</CENTER>

_EOF_
# ↑ _EOF_ は必須です。

# --------------------              # サンクス画面の部分の HTML文
$HTML_THANKS =<<"_EOF_";

<BR>
<CENTER>
<TABLE><TD><TT>
執筆ありがとう！<BR>
これまでのストーリーをご覧ください。<BR>
今後、どうなっていくのか楽しみですね。
</TT></TD></TABLE>
</CENTER>
<BR>

_EOF_

# --------------------              # 独自の JavaScript や スタイルシートはここに
$HTML_HEAD=<<"_EOF_";

<STYLE TYPE="text/css">
<!-- // CGI-StaTion StyleSheet for Web DoRaMa
TD,TH { font-size:10pt; font-family:'ＭＳ　Ｐゴシック' }
body{
    font-size: 12px;
    font-color: black;
    font-family: 'ＭＳ　Ｐゴシック','Osaka';
    background-color="white"
}
body{scrollbar-3dlight-color:#000000;
   scrollbar-arrow-color:#00ccff;
   scrollbar-base-color:#ffffff;
   scrollbar-darkshadow-color:#ffffff;
   scrollbar-face-color:#ffffff;
   scrollbar-highlight-color:#ffffff;
   scrollbar-shadow-color:#000000;
   scrollbar-track-color:#ffffff:}
a{ color:#0066ff;text-decoration:none ; cursor: w-resize;}
 a:visited { color:#FF0099;text-decoration:none ; } 
a:active { color:#9933FF; text-decoration:none ; }
 a:hover { background:#99ffff; color:#ff33cc; text-decoration:none ; }

H1         { font-size:24pt;}

-->
</STYLE>

_EOF_

# --------------------              # 上にバナー（広告）をつける必要があるならここに
$HTML_TOPBANNER=<<"_EOF_";

<!-- バナー広告をつける場所 -->

_EOF_
# ↑ この _EOF_ はこのままにしておくこと！

# --------------------              # 下にバナー（広告）をつける必要があるならここに
$HTML_BOTTOMBANNER=<<"_EOF_";

<!-- バナー広告をつける場所 -->

_EOF_
# ↑ この _EOF_ はこのままにしておくこと！

# ==========================================================
# オプションの設定はここまでです。
# 以下は CGI のプログラムです。
# 書き換えは個人の責任で行って下さい。
# ==========================================================

# --- 初期化処理
$logdir  =~ s/\/$//;
$logfile = "$logdir/$logfile";
__FILE__ =~ /([^\/]*)\/([^\/]*)$/; $cginame = $2 ? $2 : __FILE__;
$cginame =~ /([^\\]*)\\([^\\]*)$/; $cginame = $2 ? $2 : $cginame;
if ($limit_log <   30) { $limit_log =   30; }
if ($limit_log > 9900) { $limit_log = 9900;  }
&error(1,"管理用パスワードが設定されてません。") unless ($master);
&error(1,"ゲストパスワードが設定されてません。") unless ($actedit_pass);
&check_code;
&read_form;
&get_actor;

# --- 条件分岐
if ($FORM{'pass'} eq $master) {
    &read_file($logfile);
    &edit_editor;
    &html_editor;
    exit 1;
}
if ($FORM{'mode'} eq 'test')  { &check_mode; }
if ($FORM{'mode'} eq 'actor') { &actor_edit; }
if ($FORM{'mode'} eq 'admin') { &html_admin_enter; }
if ($FORM{'mode'} eq 'regist'){ &regist_dorama; &html_view; }
if ($FORM{'mode'} eq 'view')  { &html_view; }
if ($FORM{'mode'} eq '')      { &html_default; }

exit 1;

# [ HTMLヘッダー部 ]
#

sub html_header{
    print<<"_EOF_";
<HTML><HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=$charset_code"></META>
<TITLE>$cgi_title</TITLE>
$HTML_HEAD
</HEAD>
<BODY TEXT=$body_text LINK=$body_link ALINK=$body_alink VLINK=$body_vlink BGCOLOR=$body_bgcolor BACKGROUND=$body_back onLoad='defaultStatus="$cgi_title"'>
$HTML_TOPBANNER
<DIV ALIGN=right><TT>
[<A HREF="$cginame?mode=admin" onMouseOver='status="管理人専用です"'>$admin_name専用</A>]
[<A HREF="$cginame?mode=actor" onMouseOver='status="要パスワード"'>出演者エディタ</A>]
[<A HREF="$back_url" onMouseOver='status="戻ります。"'>ドラマから戻る</A>]<BR>
</TT></DIV>
_EOF_
}

# [ 著作権の表示（書き換えずに、必ず表示すること） ]
#

sub html_footer{
    print<<"_EOF_";
<BR>
<DIV ALIGN="right"><TT>
<!-- ここは書き換え禁止です。 -->
WeB DoRaMa Version 1.30.08<BR>
[
管理者：<A HREF="mailto:$admin_email">$admin_name</A>
配布元：<A HREF="http://www7.big.or.jp/~jawa/" TARGET=_top onMouseOver='status="●○● CGI-StaTion ●○●"; return true;'>ShigetoNakazawa</A>
]
</TT></DIV>
$HTML_BOTTOMBANNER
</BODY></HTML>
_EOF_
}

# [ DefaultHTML 出力 ]
#

sub html_default {
    # 最近登録されたものを取得する
    &read_file($logfile,0,$view);
    ($no,$date,$dorama,$actor,$rhost,$ipad,$time) = split(/<>/,$FILE[0]);

    # HTML出力
    print "Content-type: text/html\n\n";
    &html_header;
    print $HTML_TITLE.$HTML_INFO_TOP;
    print "<BR><BR><BLOCKQUOTE><FONT SIZE=3>\n";
    &html_dorama($view);
    print "</FONT><BR><BR></BLOCKQUOTE>\n";
    print "<CENTER>\n";
    print "<FORM METHOD=\"post\" ACTION=\"$cginame\">\n";
    print "<INPUT TYPE=\"hidden\" NAME=\"mode\" VALUE=\"regist\">\n";
    print "<INPUT TYPE=\"hidden\" NAME=\"no\" VALUE=\"$no\">\n";
    print "<SELECT NAME=\"actor\">\n";
    for ($i=0;$i<@actors;$i++) {
        print "<OPTION VALUE=\"$i\">$actors[$i]\n" if ($actor != $i || $i == 0);
    }
    print "</SELECT>\n";
    print "<INPUT TYPE=text NAME=\"dorama\" SIZE=50 MAXLENGTH=300><BR>\n";
    print "<INPUT TYPE=submit VALUE=\"投稿する\">\n";
    print "<INPUT TYPE=reset VALUE=\"書き直す\">\n";
    print "</FORM>\n";
    print "</CENTER>\n";
    print $HTML_INFO_BOTTOM;
    &html_footer;
}

# [ ViewHTML 出力 ]
#

sub html_view {
    if ($FORM{'page'} < 0) { $FORM{'page'} = 0; }
    $start = $FORM{'page'}; $end = $start + ($page - 1);
    $lastline = &read_file($logfile,$start,$end);
    print "Content-type: text/html\n\n";
    &html_header;
    print $HTML_TITLE;
    print "<CENTER><IMG SRC=\"$image_dorama\"></CENTER>\n";
    print $HTML_THANKS;
    print "<CENTER><IMG SRC=\"$image_dorama\"></CENTER>\n";
    if ($end >= $lastline) { $end = $lastline; }
    else {
        print "<DIV ALIGN=right><TT>\n";
        print "<A HREF=\"$cginame?mode=view&page=$end\">[過去のストーリー]</A>\n";
        print "</TT></DIV>\n";
    }
    &html_dorama($end - $start + 1,1);
    &html_footer;
}

# [ ドラマ内容 出力 ]
#

sub html_dorama {
    for ($i=$_[0]-1;$i>=0;$i--) {
        ($no,$date,$dorama,$actor,$rhost,$ipad) = split(/<>/,$FILE[$i]);
        print "<HR><TT><FONT COLOR=\"$emb_color\" SIZE=2>$date</FONT></TT>" if ($_[1]);
        print "<IMG SRC=\"$icon[$actor]\">\n" if ($icon[$actor]);
        if ($actor < 1 || $actor > @actors) {
            print " ？？？「$dorama」";
        } else {
            print " $actors[$actor]<FONT COLOR=\"$colors[$actor]\">「$dorama」</FONT>";
        }
        if ($ip_check || $rh_check) {
            print " <FONT COLOR=$emb_color><TT>(";
            print $ipad if ($ip_check);
            print " / " if ($ip_check && $rh_check);
            print $rhost if ($rh_check);
            print ")</TT></FONT>";
        }
        print "<BR>\n" unless ($_[1]);
    }
}

# [ ドラマ登録処理 ]
#

sub regist_dorama {
    &read_file($logfile);
    ($no,$date,$dorama,$actor,$rhost,$ipad,$time) = split(/<>/,$FILE[0]);
    $FORM{'no'} = ++$FORM{'no'} % 9999;
    local($ipad,$rhost,$ref_url) = ($ENV{'REMOTE_ADDR'},$ENV{'REMOTE_HOST'},$ENV{'HTTP_REFERER'});
    $rhost = $rhost eq $ipad?gethostbyaddr(pack('C4',split(/\./,$ipad)),2)||'':$rhost;
    $ref_url =~ s/\?(.|\n)*//ig; $ref_url =~ s/\%7E/\~/ig;
    if($check_url && ($ref_url !~ /$check_url/i)){
        &error(1,"不正なアクセスです。<BR>$ref_urlからはアクセスできません。");
    }
    foreach (@check_ipad) {
        if ($ipad =~ /^$_/) { &error(1,"$ipad からの投稿は拒否されてます。\n"); }
    }
    if ($check_proxy) {
        local($envkey,$envvalue) = ();
        while(($envkey,$envvalue) = each(%ENV)){
            if($envkey =~ /proxy/i || $envvalue =~ /proxy/i){
                &error("プロクシ経由でのアクセスは禁止されてます。");
            }
        }
    }
    if (length($FORM{'dorama'}) < 2) {
        &error(1,"投稿内容が確認できませんでした。<BR>もう一度、やり直してください。");
    }
    if ($FORM{'no'} != $no + 1) {
        &error(1,"先に他の人が執筆してしまいました。<BR>もう一度、やり直してください。");
    }
    if ($actor == $FORM{'actor'}) {
        &error(1,"出演者は続けて発言できません。<BR>出演者を変更してください。");
    }
    if ($FORM{'actor'} < 1 || $FORM{'actor'} > $#actors) {
        &error(1,"出演者が決まってません。<BR>出演者を変更してください。");
    }
    if (length($FORM{'dorama'}) > 300) {
        &error(1,"セリフが制限を越えています。<BR>もう一度、やり直してください。");
    }
    # --- ここの下三行のコメントを外すと連続投稿を拒否できます。 ---
#    if ($ipad eq $ENV{'REMOTE_ADDR'} && $^T - $time < 120) {
#        &error(1,"連続投稿はできません。<BR>時間をおいてご利用ください。");
#    }
    # タグ制限チェック
    if ($FORM{'dorama'} =~ /<[A-Z]+[^>]*>/) {
        &error(1,"タグを使ってはいけません。<BR>もう一度、やり直してください。");
    }
    $FORM{'dorama'} =~ s/</&lt;/g; $FORM{'dorama'} =~ s/>/&gt;/g;
    # 禁止ワードチェック
    foreach(@BAD_WORD) {
        if (index($FORM{'dorama'},$_) >= 0 && $_) {
            &error(1,"登録できない単語が含まれてます。<BR>もう一度、連想しなおしてください。");
        }
    }
    ($year,$mon,$day,$hour,$min,$sec,$youbi) = &get_date($tz);
    unshift(@FILE,"$FORM{'no'}<>$mon/$day $hour:$min<>$FORM{'dorama'}<>$FORM{'actor'}<>$rhost<>$ipad<>$^T\n");
    while(@FILE > $limit_log) { pop(@FILE); }
    &write_file($logfile,@FILE);
}

# [ 出演者エディタ ]
#

sub actor_edit {
    # わかりにくい構造になってしまった(^^;

    # 入り口
    unless (($FORM{'acpass'} eq $actedit_pass && ($actedit_add || $actedit_delete))
             || $FORM{'acpass'} eq $master) {
        print "Content-type: text/html\n\n";
        print<<"_EOF_";
<HTML><HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=$charset_code"></META>
<TITLE>WeB DoRaMa Actors' Editor</TITLE>
</HEAD>
<BODY TEXT=black BGCOLOR=white>
<BR><BR><BR>
<CENTER><TT>
<P>管理用パスワードかゲストパスワードを入力してください。</P>
<P><FORM METHOD="$method" ACTION="$cginame">
<INPUT TYPE="hidden" NAME="mode" VALUE="actor">
<INPUT TYPE="password" NAME="acpass" SIZE=10>
<INPUT TYPE="submit" VALUE="起動する">
</FORM></P>
<P>（出演者エディタを使用するためには、上記パスワードが必要です。）</P>
</TT></CENTER>
</BODY></HTML>
_EOF_
    exit;
    }
    # 追加処理
    $flag = 0;
    undef(@new);
    push(@new,"$actors[0]<><>\n");
    if ($FORM{'action'} eq 'add' &&
        (($FORM{'acpass'} eq $actedit_pass && $actedit_add) ||
        $FORM{'acpass'} eq $master)){
        $FORM{'actor'} =~ s/</&lt;/g; $FORM{'actor'} =~ s/>/&gt;/g;
        if (!$FORM{'actor'} || length($FORM{'actor'}) > 30) {
            &error(1,"出演者の名前が不正です");
        }
        if ($FORM{'color'} !~ /^#/ || length($FORM{'color'}) > 7) {
            &error(1,"出演者の色が不正です");
        }
        $icon = $FORM{'icon'};
        $icon =~ s/^http\:\/\///;
        if ($icon && ($icon !~ /\.gif$/i && $icon !~ /\.jpg$/i && $icon !~ /\.jpeg$/i)) {
            &error(1,"出演者のアイコンが不正です");
        }
        $FORM{'icon'} = '' unless ($icon);
        push(@actors,$FORM{'actor'});
        push(@colors,$FORM{'color'});
        push(@icon,$FORM{'icon'});
        for($i=1;$i<@actors;$i++) { push(@new,"$actors[$i]<>$colors[$i]<>$icon[$i]\n"); }
        $flag = 1;
    }
    # 削除処理
    if ($FORM{'action'} eq 'del' &&
        (($FORM{'acpass'} eq $actedit_pass && $actedit_delete) ||
        $FORM{'acpass'} eq $master)){
        pop(@actors);
        for($i=1;$i<@actors;$i++) { push(@new,"$actors[$i]<>$colors[$i]<>$icon[$i]\n"); }
        $flag = 1;
    }

    # 更新
    if ($flag) {
        &write_file($actfile,@new);
        &get_actor;
    }
    undef (@new);

    # メインＨＴＭＬ
    print "Content-type: text/html\n\n";
    print<<"_EOF_";
<HTML><HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=$charset_code"></META>
<TITLE>WeB DoRaMa Actors' Editor</TITLE>
</HEAD>
<BODY TEXT=black BGCOLOR=white>
<DIV ALIGN="right"><TT>[<A HREF="$cginame">エディタをやめる</A>]</TT></DIV>
<CENTER>
<H2>WeB DoRaMa Actors Editor</H2>

<TABLE CELLPADDING=5 CELLSPACING=4>
<TD BGCOLOR=#FFEEEE><TT>
〇 追加する時はフォームに出演者の内容を書いて、<BR>
[出演者を追加する]ボタンを押します<BR><BR>
〇 削除する時は[出演者を削除する]ボタンを押します
</TT></TD>
</TABLE>
_EOF_
    if (!$actedit_add && $FORM{'acpass'} ne $master) {
        print "<FONT COLOR=#FF0000><TT>※ 現在、ゲストパスワードでは追加できません</TT></FONT><BR>\n";
    }
    if (!$actedit_delete && $FORM{'acpass'} ne $master) {
        print "<FONT COLOR=#FF0000><TT>※ 現在、ゲストパスワードでは削除できません</TT></FONT><BR>\n";
    }
    print <<"_EOF_";
<TABLE CELLPADDING=3 CELLSPACING=0 BGCOLOR="#EEFFEE">
<FORM METHOD="$method" ACTION="$cginame">
<INPUT TYPE="hidden" NAME="mode" VALUE="actor">
<INPUT TYPE="hidden" NAME="action" VALUE="add">
<INPUT TYPE="hidden" NAME="acpass" VALUE="$FORM{'acpass'}">
<TR><TD ALIGN=right><TT>出演者名:</TT></TD>
<TD COLSPAN=2><INPUT TYPE=text NAME=actor SIZE=34 MAXLENGTH=30></TD></TR>
<TR><TD ALIGN=right><TT>色:</TT></TD>
<TD COLSPAN=2><INPUT TYPE=text NAME=color SIZE=10 MAXLENGTH=7 VALUE="#000000"></TD></TR>
<TR><TD ALIGN=right><TT>アイコン:</TT></TD>
<TD COLSPAN=2><INPUT TYPE=text NAME=icon SIZE=60 MAXLENGTH=180 VALUE="http://"></TD></TR>
<TR><TD></TD>
<TD ALIGN=right>
<INPUT TYPE=submit VALUE="出演者を追加">
</TD>
</FORM>
<FORM METHOD="$method" ACTION="$cginame">
<INPUT TYPE="hidden" NAME="mode" VALUE="actor">
<INPUT TYPE="hidden" NAME="action" VALUE="del">
<INPUT TYPE="hidden" NAME="acpass" VALUE="$FORM{'acpass'}">
<TD ALIGN=left>
<INPUT TYPE=submit VALUE="出演者を削除">
</TD>
</FORM>
</TR>
</TABLE>
<BR>
_EOF_
    print <<"_EOF_";
<TABLE CELLPADDING=2 CELLSPACING=4>
<TR>
\<TD WIDTH=60% BGCOLOR=#EEEEFF><TT>出演者一覧</TT></TD>
<TD BGCOLOR=#EEEEFF><TT>アイコン</TT></TD>
</TR>
<TR>
<TD BGCOLOR=#EEEEFF><TT><FONT COLOR=$colors[0]>$actors[0]</FONT></TT></TD>
<TD BGCOLOR=#EEEEFF><TT>なし</TT></TD>
</TR>

_EOF_
    for ($i=1;$i<@actors;$i++) {
        print "<TR>\n";
        print "<TD BGCOLOR=#EEEEFF><TT><FONT COLOR=$colors[$i]>$actors[$i]</FONT></TT></TD>\n";
        print "<TD BGCOLOR=#EEEEFF><IMG SRC=\"$icon[$i]\"></TD>\n" if ($icon[$i]);
        print "<TD BGCOLOR=#EEEEFF><TT>なし</TT></TD>\n" unless ($icon[$i]);
        print "</TR>\n";
    }
    print<<"_EOF_";
</TABLE></FORM>
</CENTER>
</BODY></HTML>
_EOF_
}

# [ 管理人入り口 ]
#

sub html_admin_enter {
    print "Content-type: text/html\n\n";
    print<<"_EOF_";
<HTML><HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=$charset_code"></META>
<TITLE>WeB DoRaMa Editor</TITLE>
</HEAD>
<BODY TEXT=black BGCOLOR=white>
<BR><BR><BR>
<CENTER><TT>
<P>管理用パスワードを入力してください。</P>
<P><FORM METHOD="$method" ACTION="$cginame">
<INPUT TYPE="password" NAME="pass" SIZE=10>
<INPUT TYPE="submit" VALUE="起動する">
</FORM></P>
<P>（管理用のエディタを使用するためには、管理用パスワードが必要です。）</P>
</TT></CENTER>
</BODY></HTML>
_EOF_
}

# [ エディター表示 ]
#

sub html_editor {
    $kiji = @FILE;
    $size = (stat($logfile))[7];
    print "Content-type: text/html\n\n";
    print<<"_EOF_";
<HTML><HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=$charset_code"></META>
<TITLE>WeB DoRaMa Editor</TITLE>
</HEAD>
<BODY TEXT=black BGCOLOR=white>
<DIV ALIGN="right"><TT>[<A HREF="$cginame">エディタをやめる</A>]</TT></DIV>
<CENTER>
<H2><I>WeB DoRaMa Editor</I></H2>
<TT>･ 現在 $kiji 件の記事があり、ログファイルは $size バイトになってます</TT><BR>
</CENTER>
<BLOCKQUOTE><TT>
<FONT COLOR="#FF0000">★使い方★</FONT><BR><BR>
1.編集する項目をチェックします。（複数の場合は全て書き換えます）<BR>
2.編集内容を書きます（このとき、何も書かなかった場合、削除されます）<BR>
3.[編集開始]で書き換えられます。<BR>
</TT></BLOCKQUOTE>
<BR>
<CENTER>
<FORM METHOD="$method" ACTION="$cginame">
<INPUT TYPE="hidden" NAME="pass" VALUE="$FORM{'pass'}">
<TABLE><TR><TD><TT>編集内容：</TT>
<SELECT NAME="actor">
_EOF_
    for ($i=0;$i<@actors;$i++) { print "<OPTION VALUE=\"$i\">$actors[$i]\n"; }
    print<<"_EOF_";
</SELECT>
<INPUT TYPE=text NAME="dorama" SIZE=50 MAXLENGTH=300>
</TD></TR><TR><TD ALIGN="right"><TT>
良ければ：<INPUT TYPE=submit VALUE="開始する">
　やめるなら：<INPUT TYPE=reset VALUE="取り消し">
</TT></TD></TR></TABLE>
</CENTER>
<HR SIZE=1>
_EOF_
    if ($FILE[0]) {
        for ($i=$#FILE;$i>-1;$i--) {
            ($no,$date,$dorama,$actor,$rhost,$ipad,$time) = split(/<>/,$FILE[$i]);
            print "<INPUT TYPE=checkbox NAME=\"del\" VALUE=$no>\n";
            print " $actors[$actor]<FONT COLOR=\"$colors[$actor]\">「$dorama」</FONT> <TT>　(<FONT COLOR=\"$emb_color\">$date</FONT>) [$rhost $ipad]</TT><BR>\n";
        }
    } else {
        print "<CENTER>ログは空っぽです。</CENTER>";
    }
    print "<HR SIZE=1>\n";
    print "</FORM>\n";
}

# [ エディット ]

sub edit_editor {
    $flag = 0;
    foreach (@FILE) {
        local($no,$date,$dorama,$actor,$rhost,$ipad,$time) = split(/<>/,$_);
        if ($del{$no}) {
            $flag = 1;
            if ($FORM{'dorama'}) {
                push (@new,"$no<>$date<>$FORM{'dorama'}<>$FORM{'actor'}<>$rhost<>$ipad<>$time");
            }
        } else { push (@new,$_); }
    }
    if ($flag) {
        undef (@FILE);
        @FILE = &write_file($logfile,@new);
    }
    undef (@new);
}

# [ 出演者を取得する ]

sub get_actor {
    &read_file($actfile);
    undef(@actors); undef(@colors); undef(@icon);
    unless ($FILE[0]) {
        $FILE[0] = "誰のセリフ<><>\n";
        &write_file($actfile,$FILE[0]);
    }
    for($i=0;$i<@FILE;$i++) {
        ($actors[$i],$colors[$i],$icon[$i]) = split(/<>/,$FILE[$i]);
        $icon[$i] =~ s/\r$|\n$//g;
    }
}

# [ CGI動作チェック ]
#

sub check_mode {
    $axslog = "Not Found" unless (-f $logfile);
    $axslog = "r" if (-r $logfile);
    $axslog .= "w" if (-w $logfile);
    $axsact = "Not Found" unless (-f $actfile);
    $axsact = "r" if (-r $actfile);
    $axsact .= "w" if (-w $actfile);
    print "Content-type: text/html\n\n";
    print<<"_EOF_";
<HTML><BODY TEXT=black BGCOLOR=white><PRE>
WeB DoRaMa Version 1.30.08 -TestMode-<BR>
[Option]
logfile[$axslog] actfile[$axsact] LockFlag:$lock_flag SaveType:$savetype
Method:$method FileName:$cginame TimeZone:$tz
Owner:$admin_name ($admin_email)<P>
[Perl]
Path:#!$^X
Version:$]<P>
[TestForm]
TestFormText:$FORM{'test'}
</PRE>
<FORM ACTION="$cginame" METHOD="$method">
<INPUT TYPE=hidden NAME=mode VALUE=test>
<INPUT TYPE=text NAME=test SIZE=20 VALUE="Test Message">
<INPUT TYPE=submit VALUE="Test">
</FORM>
</BODY></HTML>
_EOF_
    exit;
}

# [ 記録ファイルの処理 ]
#

sub read_file {
    local($logfile,$start,$end) = @_;
    local($count) = 0; undef(@FILE);
    $start = 0 if ($start < 0);
    $end = $limit_log if ($end eq '');
    &error(1,"記録ファイル($logfile)の読み込み不可") unless (open(IN,$logfile));
    foreach (<IN>) {
        push (@FILE,$_) if ($start <= $count && $count <= $end);
        $count++;
    }
    close(IN);
    return $count - 1;
}
sub write_file {
    local($logfile,@log) = @_;
    &error(1,"現在ロックされてます。<BR>しばらく利用できません。") unless (&dubble_lock_file);
    unless ($savetype) {
        # 標準タイプ 全 OS 共通
        unless (open(OUT,">$logfile")) {
            &dubble_unlock_file;
            &error(1,"記録ファイル($logfile)の書き込みができません");
        }
        print OUT @log;
        close(OUT);
    } else {
        # 改良タイプ chmod 使用（プロバイダによっては使えない）
        $tmpfile = "$$\.tmp";
        unless (open(OUT,">$tmpfile")) {
            &dubble_unlock_file;
            &error(1,"Temp方式未対応です。<BR>ログの記録方式を変えてください");
        }
        close(OUT);
        unless (chmod 0666,$tmpfile) {
            &error(1,"chmod利用できません。<BR>ログの記録方式を変えてください");
        }
        &error(1,"不明なエラーです。") unless (open(OUT,">$tmpfile"));
        print OUT @log;
        close(OUT);
        rename($tmpfile,$logfile);
        if (-e $tmpfile) { unlink($tmpfile); }
    }
    &dubble_unlock_file;
    return @log;
}

# [ ロック機構 ]
#
sub dubble_lock_file {
    return 0 unless (&lock_file("$cginame.loc1"));
    return 0 unless (&lock_file("$cginame.loc2"));
    return 1;
}
sub dubble_unlock_file {
    &unlock_file("$cginame.loc2"); &unlock_file("$cginame.loc1");
}
sub lock_file {
    local($lockfile) = $_[0];
    return 1 unless ($lock_flag);
    local($retry) = 2;
    while (-f $lockfile) {
        if ($retry-- <= 0) {
            local($mtime) = (stat($lockfile))[9];
            unless ($mtime < time()-60*15) { return 0; }
            &unlock_file($lockfile);
            return 1;
        }
        sleep 1;
    }
    unless (open (LOCK,">$lockfile")) {
        &error(1,"ロック機構\を使えません。<BR>ロック機構\を使わないようにしてください。");
    }
    close(LOCK);
    return 1;
}
sub unlock_file {
    local($lockfile) = $_[0];
    unlink($lockfile);
}

# [ 日付を取得する ]
#

sub get_date {
    $ENV{'TZ'} = $_[0] ? $_[0] : $tz;
    local($sec,$min,$hour,$day,$mon,$year,$youbi) = localtime(time);
    $mon++;
    if ($sec  < 10) { $sec  = "0$sec";  }
    if ($min  < 10) { $min  = "0$min";  }
    if ($hour < 10) { $hour = "0$hour"; }
    if ($day  < 10) { $day  = "0$day";  }
    if ($mon  < 10) { $mon  = "0$mon";  }
    $year += 1900;
    $youbi = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$youbi];
    return ($year,$mon,$day,$hour,$min,$sec,$youbi);
}

# [ フォームからデータ取得 ]
#

sub read_form {
    # 標準入力からデータもらう
    if ($ENV{'REQUEST_METHOD'} eq "POST") {
        &error(1,"書きこみすぎのため投稿できません！") if ($ENV{'CONTENT_LENGTH'} > 1024 * 99);
        read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
    } else { $buffer = $ENV{'QUERY_STRING'}; }
    # デコードする
    foreach (split(/&/,$buffer)) {
        local($name,$value) = split(/=/,$_);
        $value =~ tr/+/ /;
        $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
        $value =~ s/<>/&lt;&gt;/g;
        $value =~ s/\"/&quot;/g;
        $value =~ s/\r\n$//;
        $value =~ s/\r$|\n$//;
        if ($name eq 'del') { $del{$value} = 1; }
        else { $FORM{$name} = &change_code($value); }
    }
}

# [ 文字コード関連 ]
#

sub check_code {
    unless (-r $jcode) { &error(1,"jcode.pl がみつかりません。"); }
    require $jcode;
    local($text) = ord(substr("中澤重人＝じゃわ(^-^;;",0,1));
    if ($text == 0xc3) { $mojicode = "euc"; $charset_code = "x-euc-jp"; }
    elsif ($text == 0x92) { $mojicode = "sjis";$charset_code = "x-sjis"; }
    else { &error(1,"サポートされていない文字コードです。"); }
}
sub change_code {
    local($text)=$_[0];
    &jcode'convert(*text,$mojicode);
    if ($mojicode eq 'sjis') { &jcode'h2z_sjis(*text); }
    if ($mojicode eq 'euc')  { &jcode'h2z_euc(*text); }
    return $text;
}

# [ エラー処理 ]
#

sub error {
    print "Content-type: text/html\n\n<HTML><BODY>\n" if ($_[0]);
    print<<"_EOF_";
<HR NOSHADE>
<TABLE BGCOLOR=#FFEEEE CELLPADDING=5 WIDTH=100%><TD ALIGN=center><TT>
-エラーになりました-<BR><BR>
<FONT COLOR=#FF0000>$_[1]</FONT><BR><BR>
<B>[ <A HREF="$cginame?">WeB DoRaMa</A> ]</B>
</TT></TD></TABLE>
<HR NOSHADE>
</BODY></HTML>
_EOF_
    exit;
}
