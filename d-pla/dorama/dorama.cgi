#!/usr/bin/perl

#| WeB DoRaMa Version 1.30.08
#| This script is free.
#|
#| Author Shigeto Nakazawa.(1996/11/27)
#| HomePageUrl http://www7.big.or.jp/~jawa/
#|
#| Special Thanks ������
#| HomePgaeUrl ???

# //////////////////////////////////////////////////////////
# �I�v�V�����̐ݒ��ύX���邱�Ƃ��ł��܂��B
# �ύX����ꍇ�́Areadme.htm �������ɂȂ��Ă���s���Ă��������B
# �ݒ�ύX�ɂ͏[�����ӂ��Ă��������B
# //////////////////////////////////////////////////////////

# ----------------------------------------------------------
# �h���}�̊Ǘ��ҁi���Ȃ��j�̏��ł��B
# ----------------------------------------------------------

$admin_name = '�Ղ̌��L��';               # ���Ȃ��̖��O(�n���h���l�[��)
$admin_email = 'indigodays@deen.ne.jp'; # ���Ȃ��̃��[���A�h���X
$master = 'cosmos';               # �Ǘ��p�̃p�X���[�h

# ----------------------------------------------------------
# �h���}�̃J�X�^�}�C�Y���ڂł��B
# ----------------------------------------------------------
# �Z ��{����

$cgi_title    = 'DEEN days';       # �h���}�̃^�C�g���i�^�O�̓_���I�j

$body_text    = '#000000';          # <BODY> �^�O�̐ݒ�
$body_link    = '#0066ff';          # �����N�̐F
$body_alink   = '#9933FF';          # �N���b�N���̃����N�̐F
$body_vlink   = '#FF0099';          # ���ɃN���b�N�ς݂̃����N�̐F
$body_bgcolor = '#ffffff';          # �w�i�̐F
$body_back    = '/dorama/bsflyw.jpg';                 # �w�i�摜

$back_url = "reco/apeboard_plus.cgi";
                                    # ���A��� URL�i���URL�����j
$image_dorama = '/dorama/dorama.gif';
                                    # ���h���}�̉摜�̂��� URL

$emb_color = '#FF0000';                                 # �����F�i��Ɏ����̐F�j

$limit_log = 200;                   # ���O�̍ő�o�^��
$view      = 13;                     # �n�߂ɕ\������h���}�̐�
$page      = 80;                    # �P�y�[�W�ɕ\������h���}�̐�(^-^;;

$ip_check = 0;                      # IP�A�h���X�̕\�� �i0:�\�����Ȃ�  1:�\������j
$rh_check = 0;                      # �����[�g�z�X�g�̕\�� �i0:�\�����Ȃ�  1:�\������j

$actedit_pass   = 'guest';          # �o���҃G�f�B�^�̃Q�X�g�p�X���[�h
$actedit_add    = 1;                # �o���҃G�f�B�^�ŃQ�X�g���ǉ��ł��邩(0:�ł��Ȃ� 1:�ł���)
$actedit_delete = 0;                # �o���҃G�f�B�^�ŃQ�X�g���폜�ł��邩(0:�ł��Ȃ� 1:�ł���)

# �Z �V�X�e���֘A����
                                    # �t�@�C���֘A�̐ݒ�
                                    # �ʏ�͂��̂܂܂ŗǂ�
$method    = 'POST';                # METHOD �̐ݒ�('POST' or 'GET')
$tz        = 'JST-9';               # TimeZone
$jcode     = './jcode.pl';          # jcode.pl �̂���ꏊ
$savetype = 0;                      # ���O�̋L�^���� 0:Open�̂� 1:Temp���p
$logdir    = './';                  # �L�^�p�t�@�C���̒u���f�B���N�g���ւ̃p�X�iURL����Ȃ���j
$logfile   = 'dorama.log';          # �L�^�p�t�@�C����
$actfile   = 'dorama.act';          # �o���җp�t�@�C����
$lock_flag = 1;                     # ���b�N�@�\ 1:�g�p 0:�s�g�p

# �Z �Z�L�����e�B�[����

@BAD_WORD = ('');
                                    # ���֎~���[�h
$check_url = "http://www.d-planets.org/dorama/dorama.cgi";    # �����ɂ���CGI�̐��m�� URL (http://�`) �������Ă����Ƒ��T�C�g����
                    # �s���ɓ��e���ꂽ���̂����ۂł��܂��B
                    # �i�C�^�Y������āA���߂ė��p���邱�ƁI�j

@check_ipad = (61.26.102.222);   # ������ �o�^���ꂽ���Ȃ����� IP�A�h���X�������Ă����ƁA
                    # ���� IP�A�h���X����̑S�Ă̓��e�����ۂ��܂��B
                    # �i�C�^�Y������āA���߂ė��p���邱�ƁI�j

$check_proxy = 0;   # �����̒l�� 1 �ɂ���ƁA�v���N�V�o�R�ŗ��铽���ȖK��҂�
                    # �r���ł����܂����A�ʏ�̕���r������\��������܂��B
                    # �i�C�^�Y������āA���߂ė��p���邱�ƁI�j
# �Z �g�s�l�k�I�v�V����
                                    # HTML�֘A�̐ݒ�
# --------------------              # �^�C�g�������� HTML��
$HTML_TITLE=<<"_EOF_";

<BR>
<CENTER>
<H1><FONT COLOR=$emb_color>��</FONT>
 <I>DEEN days</I>
<FONT COLOR=$emb_color>��</FONT>
</H1></CENTER>
<BR>

_EOF_
# �� ���� _EOF_ �͂��̂܂܂ɂ��Ă������ƁI
# --------------------              # ���������� HTML���i��j
$HTML_INFO_TOP =<<"_EOF_";

<CENTER>
<TABLE><TD><TT>
�������������������ƌ���Ȃ��H�I<Br>
���ł��A���̐��_�œ˂����낤��<br>
��:�h���}�͏�łȂ����ɑ����Ă����܂��B<Br>
���e����Ɖߋ��̃h���}��ǂނ��Ƃ��o���܂��B
</TT></TD></TABLE>
</CENTER>

_EOF_
# �� _EOF_ �͕K�{�ł��B

# --------------------              # ���������� HTML���i���j
$HTML_INFO_BOTTOM =<<"_EOF_";

<CENTER>
<TABLE><TD><TT><FONT COLOR=$emb_color>
�Z <B>����</B><BR>
�^�O���g������A�S�p150���𒴂���Ɠo�^����܂���B<BR>
�����o���҂������Ĕ������邱�Ƃ͂ł��܂���B
</FONT></TT></TD></TABLE>
</CENTER>

_EOF_
# �� _EOF_ �͕K�{�ł��B

# --------------------              # �T���N�X��ʂ̕����� HTML��
$HTML_THANKS =<<"_EOF_";

<BR>
<CENTER>
<TABLE><TD><TT>
���M���肪�Ƃ��I<BR>
����܂ł̃X�g�[���[���������������B<BR>
����A�ǂ��Ȃ��Ă����̂��y���݂ł��ˁB
</TT></TD></TABLE>
</CENTER>
<BR>

_EOF_

# --------------------              # �Ǝ��� JavaScript �� �X�^�C���V�[�g�͂�����
$HTML_HEAD=<<"_EOF_";

<STYLE TYPE="text/css">
<!-- // CGI-StaTion StyleSheet for Web DoRaMa
TD,TH { font-size:10pt; font-family:'�l�r�@�o�S�V�b�N' }
body{
    font-size: 12px;
    font-color: black;
    font-family: '�l�r�@�o�S�V�b�N','Osaka';
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

# --------------------              # ��Ƀo�i�[�i�L���j������K�v������Ȃ炱����
$HTML_TOPBANNER=<<"_EOF_";

<!-- �o�i�[�L��������ꏊ -->

_EOF_
# �� ���� _EOF_ �͂��̂܂܂ɂ��Ă������ƁI

# --------------------              # ���Ƀo�i�[�i�L���j������K�v������Ȃ炱����
$HTML_BOTTOMBANNER=<<"_EOF_";

<!-- �o�i�[�L��������ꏊ -->

_EOF_
# �� ���� _EOF_ �͂��̂܂܂ɂ��Ă������ƁI

# ==========================================================
# �I�v�V�����̐ݒ�͂����܂łł��B
# �ȉ��� CGI �̃v���O�����ł��B
# ���������͌l�̐ӔC�ōs���ĉ������B
# ==========================================================

# --- ����������
$logdir  =~ s/\/$//;
$logfile = "$logdir/$logfile";
__FILE__ =~ /([^\/]*)\/([^\/]*)$/; $cginame = $2 ? $2 : __FILE__;
$cginame =~ /([^\\]*)\\([^\\]*)$/; $cginame = $2 ? $2 : $cginame;
if ($limit_log <   30) { $limit_log =   30; }
if ($limit_log > 9900) { $limit_log = 9900;  }
&error(1,"�Ǘ��p�p�X���[�h���ݒ肳��Ă܂���B") unless ($master);
&error(1,"�Q�X�g�p�X���[�h���ݒ肳��Ă܂���B") unless ($actedit_pass);
&check_code;
&read_form;
&get_actor;

# --- ��������
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

# [ HTML�w�b�_�[�� ]
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
[<A HREF="$cginame?mode=admin" onMouseOver='status="�Ǘ��l��p�ł�"'>$admin_name��p</A>]
[<A HREF="$cginame?mode=actor" onMouseOver='status="�v�p�X���[�h"'>�o���҃G�f�B�^</A>]
[<A HREF="$back_url" onMouseOver='status="�߂�܂��B"'>�h���}����߂�</A>]<BR>
</TT></DIV>
_EOF_
}

# [ ���쌠�̕\���i�����������ɁA�K���\�����邱�Ɓj ]
#

sub html_footer{
    print<<"_EOF_";
<BR>
<DIV ALIGN="right"><TT>
<!-- �����͏��������֎~�ł��B -->
WeB DoRaMa Version 1.30.08<BR>
[
�Ǘ��ҁF<A HREF="mailto:$admin_email">$admin_name</A>
�z�z���F<A HREF="http://www7.big.or.jp/~jawa/" TARGET=_top onMouseOver='status="������ CGI-StaTion ������"; return true;'>ShigetoNakazawa</A>
]
</TT></DIV>
$HTML_BOTTOMBANNER
</BODY></HTML>
_EOF_
}

# [ DefaultHTML �o�� ]
#

sub html_default {
    # �ŋߓo�^���ꂽ���̂��擾����
    &read_file($logfile,0,$view);
    ($no,$date,$dorama,$actor,$rhost,$ipad,$time) = split(/<>/,$FILE[0]);

    # HTML�o��
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
    print "<INPUT TYPE=submit VALUE=\"���e����\">\n";
    print "<INPUT TYPE=reset VALUE=\"��������\">\n";
    print "</FORM>\n";
    print "</CENTER>\n";
    print $HTML_INFO_BOTTOM;
    &html_footer;
}

# [ ViewHTML �o�� ]
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
        print "<A HREF=\"$cginame?mode=view&page=$end\">[�ߋ��̃X�g�[���[]</A>\n";
        print "</TT></DIV>\n";
    }
    &html_dorama($end - $start + 1,1);
    &html_footer;
}

# [ �h���}���e �o�� ]
#

sub html_dorama {
    for ($i=$_[0]-1;$i>=0;$i--) {
        ($no,$date,$dorama,$actor,$rhost,$ipad) = split(/<>/,$FILE[$i]);
        print "<HR><TT><FONT COLOR=\"$emb_color\" SIZE=2>$date</FONT></TT>" if ($_[1]);
        print "<IMG SRC=\"$icon[$actor]\">\n" if ($icon[$actor]);
        if ($actor < 1 || $actor > @actors) {
            print " �H�H�H�u$dorama�v";
        } else {
            print " $actors[$actor]<FONT COLOR=\"$colors[$actor]\">�u$dorama�v</FONT>";
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

# [ �h���}�o�^���� ]
#

sub regist_dorama {
    &read_file($logfile);
    ($no,$date,$dorama,$actor,$rhost,$ipad,$time) = split(/<>/,$FILE[0]);
    $FORM{'no'} = ++$FORM{'no'} % 9999;
    local($ipad,$rhost,$ref_url) = ($ENV{'REMOTE_ADDR'},$ENV{'REMOTE_HOST'},$ENV{'HTTP_REFERER'});
    $rhost = $rhost eq $ipad?gethostbyaddr(pack('C4',split(/\./,$ipad)),2)||'':$rhost;
    $ref_url =~ s/\?(.|\n)*//ig; $ref_url =~ s/\%7E/\~/ig;
    if($check_url && ($ref_url !~ /$check_url/i)){
        &error(1,"�s���ȃA�N�Z�X�ł��B<BR>$ref_url����̓A�N�Z�X�ł��܂���B");
    }
    foreach (@check_ipad) {
        if ($ipad =~ /^$_/) { &error(1,"$ipad ����̓��e�͋��ۂ���Ă܂��B\n"); }
    }
    if ($check_proxy) {
        local($envkey,$envvalue) = ();
        while(($envkey,$envvalue) = each(%ENV)){
            if($envkey =~ /proxy/i || $envvalue =~ /proxy/i){
                &error("�v���N�V�o�R�ł̃A�N�Z�X�͋֎~����Ă܂��B");
            }
        }
    }
    if (length($FORM{'dorama'}) < 2) {
        &error(1,"���e���e���m�F�ł��܂���ł����B<BR>������x�A��蒼���Ă��������B");
    }
    if ($FORM{'no'} != $no + 1) {
        &error(1,"��ɑ��̐l�����M���Ă��܂��܂����B<BR>������x�A��蒼���Ă��������B");
    }
    if ($actor == $FORM{'actor'}) {
        &error(1,"�o���҂͑����Ĕ����ł��܂���B<BR>�o���҂�ύX���Ă��������B");
    }
    if ($FORM{'actor'} < 1 || $FORM{'actor'} > $#actors) {
        &error(1,"�o���҂����܂��Ă܂���B<BR>�o���҂�ύX���Ă��������B");
    }
    if (length($FORM{'dorama'}) > 300) {
        &error(1,"�Z���t���������z���Ă��܂��B<BR>������x�A��蒼���Ă��������B");
    }
    # --- �����̉��O�s�̃R�����g���O���ƘA�����e�����ۂł��܂��B ---
#    if ($ipad eq $ENV{'REMOTE_ADDR'} && $^T - $time < 120) {
#        &error(1,"�A�����e�͂ł��܂���B<BR>���Ԃ������Ă����p���������B");
#    }
    # �^�O�����`�F�b�N
    if ($FORM{'dorama'} =~ /<[A-Z]+[^>]*>/) {
        &error(1,"�^�O���g���Ă͂����܂���B<BR>������x�A��蒼���Ă��������B");
    }
    $FORM{'dorama'} =~ s/</&lt;/g; $FORM{'dorama'} =~ s/>/&gt;/g;
    # �֎~���[�h�`�F�b�N
    foreach(@BAD_WORD) {
        if (index($FORM{'dorama'},$_) >= 0 && $_) {
            &error(1,"�o�^�ł��Ȃ��P�ꂪ�܂܂�Ă܂��B<BR>������x�A�A�z���Ȃ����Ă��������B");
        }
    }
    ($year,$mon,$day,$hour,$min,$sec,$youbi) = &get_date($tz);
    unshift(@FILE,"$FORM{'no'}<>$mon/$day $hour:$min<>$FORM{'dorama'}<>$FORM{'actor'}<>$rhost<>$ipad<>$^T\n");
    while(@FILE > $limit_log) { pop(@FILE); }
    &write_file($logfile,@FILE);
}

# [ �o���҃G�f�B�^ ]
#

sub actor_edit {
    # �킩��ɂ����\���ɂȂ��Ă��܂���(^^;

    # �����
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
<P>�Ǘ��p�p�X���[�h���Q�X�g�p�X���[�h����͂��Ă��������B</P>
<P><FORM METHOD="$method" ACTION="$cginame">
<INPUT TYPE="hidden" NAME="mode" VALUE="actor">
<INPUT TYPE="password" NAME="acpass" SIZE=10>
<INPUT TYPE="submit" VALUE="�N������">
</FORM></P>
<P>�i�o���҃G�f�B�^���g�p���邽�߂ɂ́A��L�p�X���[�h���K�v�ł��B�j</P>
</TT></CENTER>
</BODY></HTML>
_EOF_
    exit;
    }
    # �ǉ�����
    $flag = 0;
    undef(@new);
    push(@new,"$actors[0]<><>\n");
    if ($FORM{'action'} eq 'add' &&
        (($FORM{'acpass'} eq $actedit_pass && $actedit_add) ||
        $FORM{'acpass'} eq $master)){
        $FORM{'actor'} =~ s/</&lt;/g; $FORM{'actor'} =~ s/>/&gt;/g;
        if (!$FORM{'actor'} || length($FORM{'actor'}) > 30) {
            &error(1,"�o���҂̖��O���s���ł�");
        }
        if ($FORM{'color'} !~ /^#/ || length($FORM{'color'}) > 7) {
            &error(1,"�o���҂̐F���s���ł�");
        }
        $icon = $FORM{'icon'};
        $icon =~ s/^http\:\/\///;
        if ($icon && ($icon !~ /\.gif$/i && $icon !~ /\.jpg$/i && $icon !~ /\.jpeg$/i)) {
            &error(1,"�o���҂̃A�C�R�����s���ł�");
        }
        $FORM{'icon'} = '' unless ($icon);
        push(@actors,$FORM{'actor'});
        push(@colors,$FORM{'color'});
        push(@icon,$FORM{'icon'});
        for($i=1;$i<@actors;$i++) { push(@new,"$actors[$i]<>$colors[$i]<>$icon[$i]\n"); }
        $flag = 1;
    }
    # �폜����
    if ($FORM{'action'} eq 'del' &&
        (($FORM{'acpass'} eq $actedit_pass && $actedit_delete) ||
        $FORM{'acpass'} eq $master)){
        pop(@actors);
        for($i=1;$i<@actors;$i++) { push(@new,"$actors[$i]<>$colors[$i]<>$icon[$i]\n"); }
        $flag = 1;
    }

    # �X�V
    if ($flag) {
        &write_file($actfile,@new);
        &get_actor;
    }
    undef (@new);

    # ���C���g�s�l�k
    print "Content-type: text/html\n\n";
    print<<"_EOF_";
<HTML><HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=$charset_code"></META>
<TITLE>WeB DoRaMa Actors' Editor</TITLE>
</HEAD>
<BODY TEXT=black BGCOLOR=white>
<DIV ALIGN="right"><TT>[<A HREF="$cginame">�G�f�B�^����߂�</A>]</TT></DIV>
<CENTER>
<H2>WeB DoRaMa Actors Editor</H2>

<TABLE CELLPADDING=5 CELLSPACING=4>
<TD BGCOLOR=#FFEEEE><TT>
�Z �ǉ����鎞�̓t�H�[���ɏo���҂̓��e�������āA<BR>
[�o���҂�ǉ�����]�{�^���������܂�<BR><BR>
�Z �폜���鎞��[�o���҂��폜����]�{�^���������܂�
</TT></TD>
</TABLE>
_EOF_
    if (!$actedit_add && $FORM{'acpass'} ne $master) {
        print "<FONT COLOR=#FF0000><TT>�� ���݁A�Q�X�g�p�X���[�h�ł͒ǉ��ł��܂���</TT></FONT><BR>\n";
    }
    if (!$actedit_delete && $FORM{'acpass'} ne $master) {
        print "<FONT COLOR=#FF0000><TT>�� ���݁A�Q�X�g�p�X���[�h�ł͍폜�ł��܂���</TT></FONT><BR>\n";
    }
    print <<"_EOF_";
<TABLE CELLPADDING=3 CELLSPACING=0 BGCOLOR="#EEFFEE">
<FORM METHOD="$method" ACTION="$cginame">
<INPUT TYPE="hidden" NAME="mode" VALUE="actor">
<INPUT TYPE="hidden" NAME="action" VALUE="add">
<INPUT TYPE="hidden" NAME="acpass" VALUE="$FORM{'acpass'}">
<TR><TD ALIGN=right><TT>�o���Җ�:</TT></TD>
<TD COLSPAN=2><INPUT TYPE=text NAME=actor SIZE=34 MAXLENGTH=30></TD></TR>
<TR><TD ALIGN=right><TT>�F:</TT></TD>
<TD COLSPAN=2><INPUT TYPE=text NAME=color SIZE=10 MAXLENGTH=7 VALUE="#000000"></TD></TR>
<TR><TD ALIGN=right><TT>�A�C�R��:</TT></TD>
<TD COLSPAN=2><INPUT TYPE=text NAME=icon SIZE=60 MAXLENGTH=180 VALUE="http://"></TD></TR>
<TR><TD></TD>
<TD ALIGN=right>
<INPUT TYPE=submit VALUE="�o���҂�ǉ�">
</TD>
</FORM>
<FORM METHOD="$method" ACTION="$cginame">
<INPUT TYPE="hidden" NAME="mode" VALUE="actor">
<INPUT TYPE="hidden" NAME="action" VALUE="del">
<INPUT TYPE="hidden" NAME="acpass" VALUE="$FORM{'acpass'}">
<TD ALIGN=left>
<INPUT TYPE=submit VALUE="�o���҂��폜">
</TD>
</FORM>
</TR>
</TABLE>
<BR>
_EOF_
    print <<"_EOF_";
<TABLE CELLPADDING=2 CELLSPACING=4>
<TR>
\<TD WIDTH=60% BGCOLOR=#EEEEFF><TT>�o���҈ꗗ</TT></TD>
<TD BGCOLOR=#EEEEFF><TT>�A�C�R��</TT></TD>
</TR>
<TR>
<TD BGCOLOR=#EEEEFF><TT><FONT COLOR=$colors[0]>$actors[0]</FONT></TT></TD>
<TD BGCOLOR=#EEEEFF><TT>�Ȃ�</TT></TD>
</TR>

_EOF_
    for ($i=1;$i<@actors;$i++) {
        print "<TR>\n";
        print "<TD BGCOLOR=#EEEEFF><TT><FONT COLOR=$colors[$i]>$actors[$i]</FONT></TT></TD>\n";
        print "<TD BGCOLOR=#EEEEFF><IMG SRC=\"$icon[$i]\"></TD>\n" if ($icon[$i]);
        print "<TD BGCOLOR=#EEEEFF><TT>�Ȃ�</TT></TD>\n" unless ($icon[$i]);
        print "</TR>\n";
    }
    print<<"_EOF_";
</TABLE></FORM>
</CENTER>
</BODY></HTML>
_EOF_
}

# [ �Ǘ��l����� ]
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
<P>�Ǘ��p�p�X���[�h����͂��Ă��������B</P>
<P><FORM METHOD="$method" ACTION="$cginame">
<INPUT TYPE="password" NAME="pass" SIZE=10>
<INPUT TYPE="submit" VALUE="�N������">
</FORM></P>
<P>�i�Ǘ��p�̃G�f�B�^���g�p���邽�߂ɂ́A�Ǘ��p�p�X���[�h���K�v�ł��B�j</P>
</TT></CENTER>
</BODY></HTML>
_EOF_
}

# [ �G�f�B�^�[�\�� ]
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
<DIV ALIGN="right"><TT>[<A HREF="$cginame">�G�f�B�^����߂�</A>]</TT></DIV>
<CENTER>
<H2><I>WeB DoRaMa Editor</I></H2>
<TT>� ���� $kiji ���̋L��������A���O�t�@�C���� $size �o�C�g�ɂȂ��Ă܂�</TT><BR>
</CENTER>
<BLOCKQUOTE><TT>
<FONT COLOR="#FF0000">���g������</FONT><BR><BR>
1.�ҏW���鍀�ڂ��`�F�b�N���܂��B�i�����̏ꍇ�͑S�ď��������܂��j<BR>
2.�ҏW���e�������܂��i���̂Ƃ��A���������Ȃ������ꍇ�A�폜����܂��j<BR>
3.[�ҏW�J�n]�ŏ����������܂��B<BR>
</TT></BLOCKQUOTE>
<BR>
<CENTER>
<FORM METHOD="$method" ACTION="$cginame">
<INPUT TYPE="hidden" NAME="pass" VALUE="$FORM{'pass'}">
<TABLE><TR><TD><TT>�ҏW���e�F</TT>
<SELECT NAME="actor">
_EOF_
    for ($i=0;$i<@actors;$i++) { print "<OPTION VALUE=\"$i\">$actors[$i]\n"; }
    print<<"_EOF_";
</SELECT>
<INPUT TYPE=text NAME="dorama" SIZE=50 MAXLENGTH=300>
</TD></TR><TR><TD ALIGN="right"><TT>
�ǂ���΁F<INPUT TYPE=submit VALUE="�J�n����">
�@��߂�Ȃ�F<INPUT TYPE=reset VALUE="������">
</TT></TD></TR></TABLE>
</CENTER>
<HR SIZE=1>
_EOF_
    if ($FILE[0]) {
        for ($i=$#FILE;$i>-1;$i--) {
            ($no,$date,$dorama,$actor,$rhost,$ipad,$time) = split(/<>/,$FILE[$i]);
            print "<INPUT TYPE=checkbox NAME=\"del\" VALUE=$no>\n";
            print " $actors[$actor]<FONT COLOR=\"$colors[$actor]\">�u$dorama�v</FONT> <TT>�@(<FONT COLOR=\"$emb_color\">$date</FONT>) [$rhost $ipad]</TT><BR>\n";
        }
    } else {
        print "<CENTER>���O�͋���ۂł��B</CENTER>";
    }
    print "<HR SIZE=1>\n";
    print "</FORM>\n";
}

# [ �G�f�B�b�g ]

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

# [ �o���҂��擾���� ]

sub get_actor {
    &read_file($actfile);
    undef(@actors); undef(@colors); undef(@icon);
    unless ($FILE[0]) {
        $FILE[0] = "�N�̃Z���t<><>\n";
        &write_file($actfile,$FILE[0]);
    }
    for($i=0;$i<@FILE;$i++) {
        ($actors[$i],$colors[$i],$icon[$i]) = split(/<>/,$FILE[$i]);
        $icon[$i] =~ s/\r$|\n$//g;
    }
}

# [ CGI����`�F�b�N ]
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

# [ �L�^�t�@�C���̏��� ]
#

sub read_file {
    local($logfile,$start,$end) = @_;
    local($count) = 0; undef(@FILE);
    $start = 0 if ($start < 0);
    $end = $limit_log if ($end eq '');
    &error(1,"�L�^�t�@�C��($logfile)�̓ǂݍ��ݕs��") unless (open(IN,$logfile));
    foreach (<IN>) {
        push (@FILE,$_) if ($start <= $count && $count <= $end);
        $count++;
    }
    close(IN);
    return $count - 1;
}
sub write_file {
    local($logfile,@log) = @_;
    &error(1,"���݃��b�N����Ă܂��B<BR>���΂炭���p�ł��܂���B") unless (&dubble_lock_file);
    unless ($savetype) {
        # �W���^�C�v �S OS ����
        unless (open(OUT,">$logfile")) {
            &dubble_unlock_file;
            &error(1,"�L�^�t�@�C��($logfile)�̏������݂��ł��܂���");
        }
        print OUT @log;
        close(OUT);
    } else {
        # ���ǃ^�C�v chmod �g�p�i�v���o�C�_�ɂ���Ă͎g���Ȃ��j
        $tmpfile = "$$\.tmp";
        unless (open(OUT,">$tmpfile")) {
            &dubble_unlock_file;
            &error(1,"Temp�������Ή��ł��B<BR>���O�̋L�^������ς��Ă�������");
        }
        close(OUT);
        unless (chmod 0666,$tmpfile) {
            &error(1,"chmod���p�ł��܂���B<BR>���O�̋L�^������ς��Ă�������");
        }
        &error(1,"�s���ȃG���[�ł��B") unless (open(OUT,">$tmpfile"));
        print OUT @log;
        close(OUT);
        rename($tmpfile,$logfile);
        if (-e $tmpfile) { unlink($tmpfile); }
    }
    &dubble_unlock_file;
    return @log;
}

# [ ���b�N�@�\ ]
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
        &error(1,"���b�N�@�\\���g���܂���B<BR>���b�N�@�\\���g��Ȃ��悤�ɂ��Ă��������B");
    }
    close(LOCK);
    return 1;
}
sub unlock_file {
    local($lockfile) = $_[0];
    unlink($lockfile);
}

# [ ���t���擾���� ]
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

# [ �t�H�[������f�[�^�擾 ]
#

sub read_form {
    # �W�����͂���f�[�^���炤
    if ($ENV{'REQUEST_METHOD'} eq "POST") {
        &error(1,"�������݂����̂��ߓ��e�ł��܂���I") if ($ENV{'CONTENT_LENGTH'} > 1024 * 99);
        read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
    } else { $buffer = $ENV{'QUERY_STRING'}; }
    # �f�R�[�h����
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

# [ �����R�[�h�֘A ]
#

sub check_code {
    unless (-r $jcode) { &error(1,"jcode.pl ���݂���܂���B"); }
    require $jcode;
    local($text) = ord(substr("���V�d�l�������(^-^;;",0,1));
    if ($text == 0xc3) { $mojicode = "euc"; $charset_code = "x-euc-jp"; }
    elsif ($text == 0x92) { $mojicode = "sjis";$charset_code = "x-sjis"; }
    else { &error(1,"�T�|�[�g����Ă��Ȃ������R�[�h�ł��B"); }
}
sub change_code {
    local($text)=$_[0];
    &jcode'convert(*text,$mojicode);
    if ($mojicode eq 'sjis') { &jcode'h2z_sjis(*text); }
    if ($mojicode eq 'euc')  { &jcode'h2z_euc(*text); }
    return $text;
}

# [ �G���[���� ]
#

sub error {
    print "Content-type: text/html\n\n<HTML><BODY>\n" if ($_[0]);
    print<<"_EOF_";
<HR NOSHADE>
<TABLE BGCOLOR=#FFEEEE CELLPADDING=5 WIDTH=100%><TD ALIGN=center><TT>
-�G���[�ɂȂ�܂���-<BR><BR>
<FONT COLOR=#FF0000>$_[1]</FONT><BR><BR>
<B>[ <A HREF="$cginame?">WeB DoRaMa</A> ]</B>
</TT></TD></TABLE>
<HR NOSHADE>
</BODY></HTML>
_EOF_
    exit;
}
