#!/usr/local/bin/perl

#����������������������������������������������������������������������������������������������������������������������
#��Petit Poll Stylish Edition ver 4.3 (2003/10/07)
#��Copyright(C) 2002-2003 9TST4. All Rights Reserved.
#��URL�Fhttp://paxs.hp.infoseek.co.jp/
#��E-mail�Faxs@cocoa.freemail.ne.jp
#��Web Master�F�������q(Masatomo Takami)
#����������������������������������������������������������������������������������������������������������������������
#����������������������������������������������������������������������������������������������������������������������
#���ySE ver4.0�ȍ~�̃o�[�W���������芷������z
#��
#���@�@�P�Fpoll.cgi�������ւ��邾���ł����p���������܂��B
#��
#��
#���ySE ver4.0�ȑO�̃o�[�W���������芷������z
#��
#���@�@�P�F�V�o�[�W�����̃��O�f�B���N�g�����Ɂu�g�p���̃��O�v���ڂ��܂��B
#���@�@�Q�F�Ǘ����[�h�փA�N�Z�X���āAWEB�ォ��ݒ�ύX���s���Ă��������B
#��
#��
#���yPetit Poll�����芷������z
#��
#���@�@�P�F�V�o�[�W�����̃��O�f�B���N�g�����Ɂu�g�p���̃��O�v���ڂ��܂��B
#���@�@�Q�F������ck.cgi�i�ݒ�ύX�ς݁j����x�����Ăяo���܂��B
#���@�@�R�F�Ǘ����[�h�փA�N�Z�X���āAWEB�ォ��ݒ�ύX���s���Ă��������B
#��
#����������������������������������������������������������������������������������������������������������������������

require './jcode.pl';
my ($fpath, $ldir, $idir, @GAZOU, $qs_img, $rs_img, $od_img, $dw_img, $wn_img, $ad_img, $nw_img, $ptname, $lock, $web);

#����������������������������������������������������������������������������������������������������������������������
#���t�@�C�����̐ݒ�
#����������������������������������������������������������������������������������������������������������������������
#���̃t�@�C���ւ̃p�X�ihttp����j
$fpath = "http://www.d-planets.org/poll/poll.cgi";


#���O�f�B���N�g���ւ̃p�X�i�K���C�ӂ̖��O�ɕύX�B�Ō���u/�v�ŕ���j
$ldir  = "./log_d/";


#�摜�f�B���N�g���ւ̃p�X�ihttp����j
$idir  = "http://www.d-planets.org/poll/image/";


#�o�[�摜�i�w�蕪���������摜���g�p�j
@GAZOU = ("bar2.gif");


#����A�C�R��
$qs_img = "q.gif";


#���ʃA�C�R��
$rs_img = "res.gif";


#�ߋ��A�C�R��
$od_img = "old.gif";


#�z�z���A�C�R��
$dw_img = "down.gif";


#�Ǘ��A�C�R��
$ad_img = "ad.gif";


#�g�k�A�C�R��
$wn_img = "win.gif";


#�V���A�C�R��
$nw_img = "new.gif";


#�ȉ��͓��ɕύX�̕K�v�͂���܂���\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\
$ptname = "pt.log";
$lock   = "lock";
$web    = "http://paxs.hp.infoseek.co.jp/";



#����������������������������������������������������������������������������������������������������������������������
#���f�R�[�h����
#����������������������������������������������������������������������������������������������������������������������
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
	&error ("�f�[�^�𐳂����󂯎��܂���ł���");
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

	#�I�����̂݉��s����
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

	#�폜�R�����g��z���
	if ($key eq "delarray") { push (@DEL, $val); }

	$FORMS{$key} = $val;

	if ($key eq "pass") {
		if (!$val) {
			&error ("�p�X���[�h�����͂���Ă��܂���");
		}
	} elsif ($key =~ /whi|cleng|nmark/) {
		if (!$val) {
			&error ("���M���e�ɋL���R�ꂪ����܂�");
		} elsif ($val =~ /\D/) {
			&error ("���M���e�ɑS�p�������܂܂�Ă��܂�");
		}
	}

	push (@EDIT, "$key=$val\n");
}

undef (@DATE);



#����������������������������������������������������������������������������������������������������������������������
#���ݒ�t�@�C���ǂݍ���
#����������������������������������������������������������������������������������������������������������������������
my $set = $ldir . "set.dat";
my %SET = ();
my $now_lock = 0;

if (!open (SET, "< $set")) { &error ("�ݒ�t�@�C�����J���܂���ł���"); }
	while (chomp ($_ = <SET>)) {
		my ($key, $val) = split (/=/);

		$SET{$key} = $val;
	}
close (SET);

#�ݒ�ύX��ɐF�w��𔽉f���邽�߂̑[�u
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



#������������������������������������������������������������������������������������������������������������������
#�����[�h����
#������������������������������������������������������������������������������������������������������������������
if (!$FORMS{'mode'}) {
	&head (1, "�Ǘ��p�X���[�h�F�؉��");
	&adcheck;
	&foot (1);
} elsif ($FORMS{'mode'} eq "adcheck") {
	&head (1, "�Ǘ��p�X���[�h�F�؉��");
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

#�ȉ����[�h�̓N�G���r��
if (!$pflag) { &error ("�s���ȃA�N�Z�X�ł�"); }

if ($FORMS{'mode'} eq "admin") {
	if (!$FORMS{'pass'} or $FORMS{'pass'} ne $SET{'pass'}) {
		&error ("�Ǘ��p�X���[�h���F�؂���܂���ł���");
	} else {
		&admin;
		&foot (1);
	}
} elsif ($FORMS{'mode'} eq "set") {
	&head (1, "�ݒ�ύX�t�H�[��");
	&set_form;
	&foot (1);
} elsif ($FORMS{'mode'} eq "s_edt") {
	&set_edit;
} elsif ($FORMS{'mode'} eq "new") {
	&head (1, "�V�K���[�쐬�t�H�[��");
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
	if ($FORMS{'ing'} != 1) { &error ("�ݒ�ύX�͐i�s���̓��[�����s���܂���"); }
	&head (1, "�ݒ�ύX�t�H�[��");
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
	&error ("�s���ȃA�N�Z�X�ł�");
}



#����������������������������������������������������������������������������������������������������������������������
#���Ǘ����[�h �F�؉��
#����������������������������������������������������������������������������������������������������������������������
sub adcheck {
my ($p_edt);

$p_edt = qq|
<DIV style="width:400px;border:solid 1px #ccc;padding:6px;">
<BR>
<SPAN class="em_font" style="font-weight:bold;">�I�I�I</SPAN>
<BR>
<BR>
�Ǘ��p�X���[�h�́w0123�x�ł��B���}�ɐݒ�ύX���s���ĉ������B
<BR>
<BR>
</DIV>
<BR>
|;

#�p�X0123�͌x��
if ($SET{'pass'} ne "0123") { $p_edt = "�Ǘ��p�X���[�h����͂��Ă�������<BR>"; }

print <<EOF;
$p_edt
<BR>

<FORM method="POST" action="$fpath">
<INPUT type="password" name="pass" size="8">
<INPUT type="hidden" name="mode" value="admin">
<INPUT type="hidden" name="act" value="1">
<INPUT type="submit" value="�F��">
</FORM>

EOF
}



#������������������������������������������������������������������������������������������������������������������
#�����[�Ǘ����
#������������������������������������������������������������������������������������������������������������������
sub admin {
#�ē����L�[���擾
if (!$FORMS{'act'}) { $FORMS{'pass'} = $_[0]; }

#�f�B���N�g�����`�F�b�N
unless (-e $ldir) { &error ("���O�f�B���N�g�����쐬���Ă�������"); }

#���[�^�C�g�����O
my $ptlog = $ldir . $ptname;

#���[�^�C�g�����O���`�F�b�N
unless (-e $ptlog) {
	if (!open (PT, ">$ptlog")) { &error ("���[�^�C�g�����O�̍쐬�Ɏ��s���܂���"); }
	close (PT);
	chmod (0666, "$ptlog");
}


my $p_edt = qq|
<BR>
*���߂ẴA�N�Z�X���ɂ́u�ݒ�ύX�v����Ǘ��p�X���[�h��ύX���ĉ������B
|;

if ($FORMS{'pass'} ne "0123") { undef ($p_edt); }


#���[�^�C�g�����擾
if (!open (PT, "<$ptlog")) { &error ("���[�^�C�g�����O���J���܂���ł���"); }

&head (1, "���[�Ǘ����");

print <<EOF;
<DIV style="text-align:left;width:440px;">
*�����e�i���X��ʂ֐i�ނɂ́A�^�C�g���̑O�̃{�^���Ƀ`�F�b�N�����ĉ������B
<BR>
*�u���[��S�폜�v����ƁA�쐬�������[�����ׂč폜����܂��B
$p_edt
</DIV>
<BR>
<BR>

<FORM method="POST" action="$fpath">
<DIV class="pframe">
<TABLE cellpadding="3" cellspacing="1" border="0" summary="���X�g">
<TR>
<TD class="pline1" style="width:40px;">ID</TD>
<TD class="pline1" style="width:40px;">�����e</TD>
<TD class="pline1" style="width:400px;">���[�^�C�g��</TD>
</TR>

EOF

my $idno = 1;	#�V�K�쐬����ID�i���o�[
my $exflag = 0;	#���[���݃t���O

#���[�^�C�g�����擾
while (chomp ($_ = <PT>)) {
	my ($id, $ptitle, $ing) = split (/<>/);

	print qq|<TR><TD class="pline2">$id</TD>|;

		if ($ing == 1) {
			print qq|<TD class="pline2"><INPUT type="radio" name="id" value="$id"></TD>|;
			print qq|<TD class="pline2">$ptitle</TD>|;
		} elsif ($ing == 2) {
			print qq|<TD class="pline2"><INPUT type="radio" name="id" value="$id"></TD>|;
			print qq|<TD class="pline2">$ptitle<SPAN style="color:$SET{'efont'};">�i�I���j</SPAN></TD>|;
		} elsif (!$ing) {
			print qq|<TD class="pline2">-</TD>|;
			print qq|<TD class="pline2">$ptitle<SPAN style="color:$SET{'efont'};">�i�폜�j</SPAN></TD>|;
		}

	print qq|</TR>|;

	$idno ++;
	$exflag = 1;
}

close (PT);

#���X�g����
if (!$exflag) {
	print qq|
	<TR>
	<TD class="pline2">-</TD>
	<TD class="pline2">-</TD>
	<TD class="pline2">���ݍs���Ă��铊�[�͂���܂���</TD>
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
<TABLE cellpadding="1" cellspacing="2" border="0" summary="���j���[">
<TR>
<TD>
<INPUT type="hidden" name="mode" value="maint">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="hidden" name="act" value="1">
<INPUT type="submit" value="�`�F�b�N���ڂ�ҏW">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="id" value="$idno">
<INPUT type="hidden" name="mode" value="new">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="���[���쐬">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="u_end">
<INPUT type="submit" value="���[��S�폜">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="set">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="�ݒ�ύX">
</FORM>
</TD>
</TR>
</TABLE>

EOF

}



#����������������������������������������������������������������������������������������������������������������������
#���ݒ�t�@�C�� �t�H�[��
#����������������������������������������������������������������������������������������������������������������������
sub set_form {
my (%CHECK);
#�\���`��
if (!$SET{'rtype'}) {
	$CHECK{'rtp_0'} = " checked";
} else {
	$CHECK{'rtp_1'} = " checked";
}

#�R�����g�{��
if (!$SET{'ctype'}) {
	$CHECK{'ctp_0'} = " checked";
} else {
	$CHECK{'ctp_1'} = " checked";
}

#�\�[�g����
if (!$SET{'stype'}) {
	$CHECK{'stp_0'} = " checked";
} elsif ($SET{'stype'} == 1) {
	$CHECK{'stp_1'} = " checked";
} elsif ($SET{'stype'} == 2) {
	$CHECK{'stp_2'} = " checked";
}

#�t�@�C�����b�N
if (!$SET{'lkey'}) {
	$CHECK{'lky_0'} = " checked";
} else {
	$CHECK{'lky_1'} = " checked";
}

print <<EOF;
<DIV style="text-align:left;width:460px;line-height:16px;">
*�S���[���ʂ̐ݒ�ł��B
<BR>
*�F�w��ɘR��E��肪����ƁA�F������ɔ��f����܂���̂ł����ӂ��������B
<BR>
*���ʕ\\���E�����T�C�Y�E�F�w���ύX�����ꍇ�A�\\�[�X���������ĉ������B
<BR>
*�z�X�g�����͍Ō�̕������Ȃ��ĉ������B�i127.0.0.1  -&gt;  127.0.0�j
</DIV>

<FORM method="POST" action="$fpath">
<DIV class="fframe">
<TABLE cellpadding="5" cellspacing="1" border="0">
<TR>
<TD class="fleft">���[�S�̂̃^�C�g��</TD>
<TD class="fright">
<INPUT type="text" name="title" size="50" value="$SET{'title'}">
</TD>
</TR>

<TR>
<TD class="fleft">�z�[���y�[�W</TD>
<TD class="fright">
<INPUT type="text" name="home" size="50" value="$SET{'home'}">
</TD>
</TR>

<TR>
<TD class="fleft">�Ǘ��p�X���[�h</TD>
<TD class="fright">
<INPUT type="text" name="pass" size="8" value="$SET{'pass'}">
<SPAN class="em_font">�����p�p�����̂�</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft">���ʕ\\��</TD>
<TD class="fright">
<INPUT type="radio" name="rtype" value="0"$CHECK{'rtp_0'}>�����ŊJ��
<INPUT type="radio" name="rtype" value="1"$CHECK{'rtp_1'}>�����̃E�B���h�E�ŊJ��
</TD>
</TR>

<TR>
<TD class="fleft">�R�����g�{������</TD>
<TD class="fright">
<INPUT type="radio" name="ctype" value="0"$CHECK{'ctp_0'}>�N�ł���
<INPUT type="radio" name="ctype" value="1"$CHECK{'ctp_1'}>�Ǘ��҂̂�
</TD>
</TR>

<TR>
<TD class="fleft">���[���ʂ̃\\�[�g</TD>
<TD class="fright">
<INPUT type="radio" name="stype" value="0"$CHECK{'stp_0'}>�s��Ȃ�
<INPUT type="radio" name="stype" value="1"$CHECK{'stp_1'}>����
<INPUT type="radio" name="stype" value="2"$CHECK{'stp_2'}>�~��
</TD>
</TR>

<TR>
<TD class="fleft">�����̍���</TD>
<TD class="fright">
<INPUT type="text" name="whi" size="4" value="$SET{'whi'}">
<SPAN class="em_font">�����p�����̂�/�W���F302�i�I����4�j</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft">�R�����g�̒���</TD>
<TD class="fright">
<INPUT type="text" name="cleng" size="4" value="$SET{'cleng'}">
<SPAN class="em_font">�����p�����̂�/�@\�\\���p���Ɏ擾�ł��镶�����i�S�p���Z�j</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft">�R�����g�̐V���}�[�N</TD>
<TD class="fright">
<INPUT type="text" name="nmark" size="4" value="$SET{'nmark'}">���Ԉȓ�
<SPAN class="em_font">�����p�����̂�</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft">�t�@�C�����b�N</TD>
<TD class="fright">
<INPUT type="radio" name="lkey" value="0"$CHECK{'lky_0'}>���b�N���Ȃ�
<INPUT type="radio" name="lkey" value="1"$CHECK{'lky_1'}>���b�N����
</TD>
</TR>

<TR>
<TD class="fleft">�z�X�g����</TD>
<TD class="fright">
<TEXTAREA cols="20" rows="3" name="hkick">
EOF

foreach (split (/;/, $SET{'hkick'})) {
	print "$_\n";
}

print <<EOF;
</TEXTAREA>
<SPAN class="em_font">����s�Ɉꌏ����</SPAN>
</TD>
</TR>
</TABLE>
</DIV>
<BR>

<DIV class="fframe">
<TABLE cellpadding="5" cellspacing="1" border="0">
<TR>
<TD class="fleft2">�S�̂̔w�i�F�ƃt�H���g�F</TD>
<TD class="fright2">
<INPUT type="text" name="bback" size="8" value="$SET{'bback'}">/
<INPUT type="text" name="bfont" size="8" value="$SET{'bfont'}">
<SPAN class="em_font">�i�w�i/�t�H���g�j</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft2">�w�b�_�[�̉��n�ƃt�H���g�F</TD>
<TD class="fright2">
<INPUT type="text" name="hback" size="8" value="$SET{'hback'}">/
<INPUT type="text" name="hfont" size="8" value="$SET{'hfont'}">
<SPAN class="em_font">�i���n/�t�H���g�j</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft2">�����N</TD>
<TD class="fright2">
<INPUT type="text" name="alink" size="8" value="$SET{'alink'}">/
<INPUT type="text" name="vlink" size="8" value="$SET{'vlink'}">/
<INPUT type="text" name="hlink" size="8" value="$SET{'hlink'}">
<SPAN class="em_font">�i�ʏ�/�K��ς�/�}�E�X�I�[�o�[�j</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft2">���[�t���[���F�ƃt�H���g�F</TD>
<TD class="fright2">
<INPUT type="text" name="rback1" size="8" value="$SET{'rback1'}">/
<INPUT type="text" name="rfont1" size="8" value="$SET{'rfont1'}">
<SPAN class="em_font">�i�t���[��/�t�H���g�j</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft2">���[�f�[�^���̉��n�ƃt�H���g�F</TD>
<TD class="fright2">
<INPUT type="text" name="rback2" size="8" value="$SET{'rback2'}">/
<INPUT type="text" name="rfont2" size="8" value="$SET{'rfont2'}">
<SPAN class="em_font">�i���n/�t�H���g�j</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft2">���[�t���[���̉e</TD>
<TD class="fright2">
<INPUT type="text" name="rshadow" size="8" value="$SET{'rshadow'}">
<SPAN class="em_font">�i���[�f�[�^���̉��n�Ɠ����F�ł��ǁj</SPAN>
</TD>
</TR>

<TR>
<TD class="fleft2">�����t�H���g�F</TD>
<TD class="fright2">
<INPUT type="text" name="efont" size="8" value="$SET{'efont'}">
<SPAN class="em_font">�i���߂ق��A���[���ԂȂǂ̐F�j</SPAN>
</TD>
</TR>
</TABLE>
</DIV>
<BR>
<BR>
<BR>

<INPUT type="hidden" name="mode" value="s_edt">
<INPUT type="hidden" name="temp" value="1">
<INPUT type="button" value="�߂�" onClick="JavaScript:history.back()">
<INPUT type="submit" value="�ύX�𔽉f����">
</FORM>

EOF
}



#����������������������������������������������������������������������������������������������������������������������
#���ݒ�t�@�C�� �쐬
#����������������������������������������������������������������������������������������������������������������������
sub set_edit {
#mode��temp���폜
pop (@EDIT);
pop (@EDIT);

#�ύX�s�\�Ȏ�����ǉ�
push (@EDIT, "bhi=$SET{'bhi'}\n");

if ($SET{'lkey'}) { if (!&lock_on) { &error ("�T�[�o�[�����ݍ����Ă��܂�"); } }
$now_lock = 1;

if (!open (SET, "+< $set")) { &error ("�ݒ�t�@�C�����J���܂���ł���"); }
seek (SET, 0, 0);
print SET @EDIT;
truncate (SET, tell);
close (SET);

if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

#�폜��΍�̂��߁A�ē����L�[���폜
undef ($FORMS{'act'});

&admin ($FORMS{'pass'});
&foot (1);
}



#������������������������������������������������������������������������������������������������������������������
#�����[�쐬�t�H�[��
#������������������������������������������������������������������������������������������������������������������
sub form {
my ($setline);

if ($FORMS{'mode'} eq "new") {
	print qq|
		<DIV style="width:400px;text-align:left;line-height:18px;">
		*�ݒ�͊e���[���Ƃɋ�ʂ���܂��B<BR>
		*�R�����g�͌��E���𒴂���Ɓu�Â������珇�v�ɍ폜����܂��B<BR>
		*���[�̎����I���́u�����Ɉ�v�������v���D�悳��܂��B
		</DIV>
		<BR>\n
		|;
} else {
	my $idlog = $ldir . $FORMS{'id'} . ".log";

	if (!open (ID, "<$idlog")) { &error ("���[���O���J���܂���ł���"); }

	$setline = <ID>;

	close (ID);
}

#���[��/����/�{������/�R�����g�擾/�R�����g���E/�A��/�A�֊���/�A�֒P��/�I���b��/���E���[/�J�n����/�I������/ing�t���O
my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split (/<>/, $setline) if ($setline);

#�t�H�[�����e�̒�`�i�ݒ�ύX���p�j
my (%CHECK);
if ($FORMS{'mode'} ne "new") {
	#�{������
	if ($reye) {
		$CHECK{'rch_1'} = " checked";
	} else {
		$CHECK{'rch_0'} = " checked";
	}

	#�R�����g�擾
	if (!$cget) {
		$CHECK{'cgt_0'} = " checked";
	} elsif ($cget == 1) {
		$CHECK{'cgt_1'} = " checked";
	} elsif ($cget == 2) {
		$CHECK{'cgt_2'} = " checked";
	}

	#�A�����[�֎~
	if (!$pkick) {
		$CHECK{'pkc_0'} = " checked";
	} elsif ($pkick == 1) {
		$CHECK{'pkc_1'} = " checked";
	}

	#�A�����[�֎~
	if (!$kunit) {
		$CHECK{'kut_0'} = " checked";
	} elsif ($kunit == 1) {
		$CHECK{'kut_1'} = " checked";
	} elsif ($kunit == 2) {
		$CHECK{'kut_2'} = " checked";
	}

	#�c�����
	my $p_bef = sprintf ("%.1f", ($period - $time) / 86400);
	$period = (int ($p_bef) == $p_bef) ? sprintf ("%d", $p_bef) : int ($p_bef) + 1;

	if (!$cget)   { undef ($climit); }
	if (!$kval)   { undef ($kval); }
	if (!$plimit) { undef ($plimit); }
	if ($end eq "������") { undef ($period); }
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
	<TD class="fleft">������e</TD>
	<TD class="fright"><INPUT type="text" name="qst" size="50"></TD>
	</TR>
	
	<TR>
	<TD class="fleft">�I����</TD>
	<TD class="fright">
	<TEXTAREA cols="40" rows="5" name="sel"></TEXTAREA><BR>
	<DIV class="em_font">�E�I������1�s�ɂ�����L�����Ă��������i�_��p�����͗v��܂���j</DIV>
	<DIV class="em_font">�E�I�����͍Œ�2�ȏ�p�ӂ��Ă�������</DIV>
	</TD>
	</TR>
	|;
}

#�V�K�쐬�A�ݒ�ύX���p�t�H�[��
print <<EOF;
<TR>
<TD class="fleft">���ʉ{��</TD>
<TD class="fright">
<INPUT type="radio" name="reye" value="0"$CHECK{'rch_0'}>�����[���͕s��
<INPUT type="radio" name="reye" value="1"$CHECK{'rch_1'}>���ł���
</TD>
</TR>

<TR>
<TD class="fleft">�R�����g�擾</TD>
<TD class="fright">
<INPUT type="radio" name="cget" value="0"$CHECK{'cgt_0'}>���g�p
<INPUT type="radio" name="cget" value="1"$CHECK{'cgt_1'}>�C��
<INPUT type="radio" name="cget" value="2"$CHECK{'cgt_2'}>�K�{
</TD>
</TR>

<TR>
<TD class="fleft">�R�����g���E��</TD>
<TD class="fright">
�I������ɂ�<INPUT type="text" name="climit" size="4" value="$climit">�܂�
<DIV class="em_font">�i���p�����A0�����L���Ȃ�5�܂ŁA�@\�\\�g�p���̂ݔ��f�j</DIV>
</TD>
</TR>

<TR>
<TD class="fleft">�A�����[�֎~�@\�\\</TD>
<TD class="fright">
<INPUT type="radio" name="pkick" value="0"$CHECK{'pkc_0'}>���g�p
<INPUT type="radio" name="pkick" value="1"$CHECK{'pkc_1'}>�g�p
</TD>
</TR>

<TR>
<TD class="fleft">�A�����[�֎~����</TD>
<TD class="fright">
<INPUT type="text" name="kval" size="4" value="$kval">
<INPUT type="radio" name="kunit" value="0"$CHECK{'kut_0'}>��
<INPUT type="radio" name="kunit" value="1"$CHECK{'kut_1'}>����
<INPUT type="radio" name="kunit" value="2"$CHECK{'kut_2'}>��
<DIV class="em_font">�i��/���p�����A�E/�P�ʁA0�����L���Ȃ��l���A�@\�\\�g�p���̂ݔ��f�j</DIV>
</TD>
</TR>

<TR>
<TD class="fleft">���[����</TD>
<TD class="fright">
<INPUT type="text" name="period" size="4" value="$period">����
<DIV class="em_font">�i���p�����A0�����L���Ȃ疳�����A�w����ԂŎ����I���j</DIV>
</TD>
</TR>

<TR>
<TD class="fleft">���E���[��</TD>
<TD class="fright">
<INPUT type="text" name="plimit" size="4" value="$plimit">�[
<DIV class="em_font">�i���p�����A0�����L���Ȃ疳�����A�w��[�Ŏ����I���j</DIV>
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
		<INPUT type="button" value="�߂�" onClick="JavaScript:history.back()">
		<INPUT type="submit" value="���̓��e�Ŋm�F����">
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
		<INPUT type="button" value="�߂�" onClick="JavaScript:history.back()">
		<INPUT type="submit" value="�ύX�𔽉f����">
		</FORM>
		|;
}
}



#����������������������������������������������������������������������������������������������������������������������
#�����[�쐬 �m�F
#����������������������������������������������������������������������������������������������������������������������
sub pre {
my ($sel_d, @SEL, $ing_ms);

if ($FORMS{'mode'} eq "pre") {
	#�I�����̓��e�͑��M�p�Ɗm�F�p��p��
	$sel_d = $FORMS{'sel'};

	#�m�F�p�̑I������z��ɑ��
	@SEL = split (/<BR>/, $FORMS{'sel'});

	#���M���e�m�F
	if (!$FORMS{'qst'}) {
		&error ("������e���L������Ă��܂���");
	} elsif (!$SEL[1]) {
		&error ("�I�����͍Œ�2�ȏ�p�ӂ��Ă�������");
	}
	#���[��
	$ing_ms = "�i�s��";
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
	
	if ($ing == 1) { $ing_ms ="�i�s��"; } else { $ing_ms ="�I��"; }
}

#���ʉ{���t���O�i�Y������$FORMS{'reye'}�j
my @REYE = qw (�����[���͕s�� ���ł���);

#���ʕ\���^�C�v / �R�����g�{������
my @RTYPE = qw (�������J�� �������J���Ȃ�);
my @CTYPE = qw (�N�ł��� �Ǘ��҂̂�);

#���[����
if ($FORMS{'period'} =~ /\D/) { &error ("���[���Ԃɖ����Ȑ��l���܂܂�Ă��܂�"); }

#�J�n���ƏI����
if ($FORMS{'mode'} eq "pre") { &opening; &finale; }

#�R�����g�擾�i$FORMS{'cget'} = �g�p���g�p / $FORMS{'climit'} = �擾���j
my ($c_ms, $c_lt);
if ($FORMS{'climit'} =~ /\D/) {
	&error ("���E�R�����g���ɖ����Ȑ��l���܂܂�Ă��܂�");
} elsif (!$FORMS{'climit'}) {
	$FORMS{'climit'} = 5;
}

if (!$FORMS{'cget'}) { 
	$c_ms = "���g�p";
	$c_lt = "���ݒ�";
} elsif ($FORMS{'cget'} == 1) {
	$c_ms = "�C��";
	$c_lt = "�e$FORMS{'climit'}�܂�";
} elsif ($FORMS{'cget'} == 2) {
	$c_ms = "�K�{";
	$c_lt = "�e$FORMS{'climit'}�܂�";
}

#�A�֊��ԁi�Y������$FORMS{'kunit'}�j
my ($k_ms);
my @KUNIT = qw (�� ���� ��);
if(!$FORMS{'pkick'}) {
	$k_ms = "���ݒ�";
	$FORMS{'kval'} = 0;
} else {
	if (!$FORMS{'kval'}) {
		$k_ms = "��l���";
		$FORMS{'kval'} = 0;
	} else {
		$k_ms = "$FORMS{'pkick'}$KUNIT[$FORMS{'kunit'}]�Ɉ��";
	}
}

#���E���[
my $pl_ms;
if ($FORMS{'plimit'} =~ /\D/) {
	&error ("���E���[���ɖ����Ȑ��l���܂܂�Ă��܂�");
} elsif (!$FORMS{'plimit'}) {
	$pl_ms = "���ݒ�";
} else  {
	$pl_ms = "$FORMS{'plimit'}�[�܂�";
}

if ($FORMS{'mode'} eq "pre") {
	&head (1, "�V�K���[�쐬�m�F���");

	print qq|
	<DIV style="width:400px;text-align:left;line-height:18px;">
	*���L�̓��e�ł�낵����΁A�u���̓��e�ō쐬����v�{�^���������Ă��������B<BR>
	*���e�ɒ���������΁u�߂�v�{�^���������Ă��������B<BR>
	*�쐬��Ɏ���A�I�����̓��e��ς��邱�Ƃ͂ł��܂���B<BR>
	*�ݒ�A�t�H�[���f�U�C���͐ݒu��ł����R�ɕύX���邱�Ƃ��ł��܂��B
	</DIV>
	<BR>
	<BR>\n
	|;
}

#�ݒ�e�[�u��
print <<EOF;
<DIV class="fframe">
<TABLE cellpadding="5" cellspacing="1" border="0">
<TR>
<TD class="sleft">���[��</TD>
<TD class="sright">$ing_ms</TD>
<TD class="sleft">�J�n��</TD>
<TD class="sright">$FORMS{'start'}</TD>
<TD class="sleft">�I����</TD>
<TD class="sright">$FORMS{'end'}</TD>
</TR>

<TR>
<TD class="sleft">���E���[��</TD>
<TD class="sright">$pl_ms</TD>
<TD class="sleft">�R�����g�擾</TD>
<TD class="sright">$c_ms</TD>
<TD class="sleft">�R�����g���E��</TD>
<TD class="sright">$c_lt</TD>
</TR>

<TR>
<TD class="sleft">�A���֎~����</TD>
<TD class="sright">$k_ms</TD>
<TD class="sleft">���ʉ{��</TD>
<TD class="sright">$REYE[$FORMS{'reye'}]</TD>
<TD class="sleft">�R�����g�{��</TD>
<TD class="sright">$CTYPE[$SET{'$ctype'}]</TD>
</TR>

<TR>
<TD class="sleft">���ʕ\\��</TD>
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
	#���[�t�H�[���T���v��
	print qq|
	<FORM>
	<DIV style="font-size:13px;width:180px;background-color:$SET{'rback1'};border:solid 1px $SET{'rback2'};padding:3px;">
	<DIV style="width:100%;color:$SET{'rfont1'};text-align:left;padding-bottom:3px;">
	<IMG src="$idir$qs_img"> $FORMS{'qst'}
	</DIV>
	<DIV style="width:100%;text-align:left;background-color:$SET{'rback2'};color:$SET{'rfont2'};border-top:solid 2px $SET{'rshadow'};border-left:solid 2px $SET{'rshadow'};padding:3px;">
	\n
	|;

	#�I��������W�J
	my $no = 1;
	foreach (0 .. $#SEL) {
		my $check = " checked" if ($no == 1);
		print qq|<DIV style="padding:3px;"><INPUT type="radio" name="poll" value="$no"$check>$SEL[$_]</DIV>\n|;
		$no ++;
		undef ($check);
	}

	print qq|<DIV align="center"><BR>|;
	
	#�R�����g�t�H�[����W�J
	if ($FORMS{'cget'}) {
		print qq|
		�R�����g<BR>
		<INPUT type="text" size="25" name="com"><BR><BR>
		|;
	}

	print qq|
	<INPUT type="button" value="���["><BR><BR>
	</DIV>
	</DIV>
	<SPAN style="width:100%;text-align:right;padding-top:3px;">
	<IMG src="$idir$rs_img" border="0" alt="����" title="����">
	<IMG src="$idir$od_img" border="0" alt="�ߋ��̓��[" title="�ߋ��̓��[">
	<IMG src="$idir$dw_img" border="0" alt="Petit Poll SE �_�E�����[�h">
	<IMG src="$idir$ad_img" border="0" alt="�Ǘ�" title="�Ǘ�">
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
	<INPUT type="button" value="�߂�" onClick="JavaScript:history.back()">
	<INPUT type="submit" value="���̓��e�ō쐬����">
	</FORM>\n
	|;
}
}



#������������������������������������������������������������������������������������������������������������������
#�����[�쐬 �X�V
#������������������������������������������������������������������������������������������������������������������
sub new_make {
#���O���`
my $ptlog = $ldir . $ptname;
my $idlog = $ldir . $FORMS{'id'} . ".log";

if ($SET{'lkey'}) { if (!&lock_on) { &error ("�T�[�o�[�����ݍ����Ă��܂�"); } }
$now_lock = 1;

#���[�^�C�g�����O���J��
if (!open (PT, "+<$ptlog")) { &error ("���[�^�C�g�����O���J���܂���ł���"); }

my @PNEW = ();
while (chomp ($_ = <PT>)) {
	my ($id, $qst, $ing) = split (/<>/, $_);

	#��d�쐬�`�F�b�N
	if ($id eq $FORMS{'id'}) {
		&error ("���ɓ��[�쐬���������Ă��܂�");
	} elsif ($qst eq $FORMS{'qst'}) {
		&error ("��������̓��[���쐬�ς݂ł�");
	}

	push (@PNEW, "$_\n");
}

#�V�K�z��ǉ�
push (@PNEW, "$FORMS{'id'}<>$FORMS{'qst'}<>1\n");
seek (PT, 0, 0);
print PT @PNEW;
truncate (PT, tell);
close(PT);

#ID���O���쐬
if (!open (ID, ">$idlog")) { &error ("���[���O�̍쐬�Ɏ��s���܂���"); }
	seek (ID, 0, 0);

	#���[��/����/�{������/�R�����g�擾/�R�����g���E/�A��/�A�֊���/�A�֒P��/�I���b��/���E���[/�J�n����/�I������/ing�t���O
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

&head (1, "���[�t�H�[�� �\\�[�X");

print <<EOF;
<DIV style="width:400px;text-align:left;line-height:18px;">
*���̃\\�[�X���R�s�[���āA�ݒu������HTML�t�@�C����\�\\��t���Ă��������B<BR>
*������̃\\�[�X�́A�����e�i���X���[�h�ł��ł��m�F���ł��܂��B
</DIV>
<BR>
<BR>
EOF

&sourse (0, 0, @SEL);
&foot (1);

}



#������������������������������������������������������������������������������������������������������������������
#���\�[�X
#������������������������������������������������������������������������������������������������������������������
sub sourse {
my ($qst, $cget, @SEL) = @_;
$FORMS{'qst'} ||= $qst;

my ($front, $button, $rslink);
#�����g�p���g�p�̕���i�OFORM / ���[�{�^�� / ���ʃ����N�j
if ($SET{'rtype'}) {
	$front  = "&lt;FORM method=&quot;POST&quot; action=&quot;$fpath&quot;&gt;";
	$button = "&lt;INPUT type=&quot;submit&quot; value=&quot;���[&quot;&gt;";
	$rslink = "&lt;A href=&quot;$fpath?mode=result&amp;id=$FORMS{'id'}&quot;&gt;<BR>&lt;IMG src=&quot;$idir$rs_img&quot; alt=&quot;����&quot; border=&quot;0&quot;&gt;&lt;/A&gt;";
} else {
	$front  = "&lt;FORM name=&quot;pollform$FORMS{'id'}&quot;&gt;";
	$button = "&lt;INPUT type=&quot;button&quot; value=&quot;���[&quot;onClick=&quot;OpenWin$FORMS{'id'}()&quot;&gt;";
	$rslink = "&lt;A href=&quot;JavaScript:ResultWin('$FORMS{'id'}')&quot;&gt;<BR>&lt;IMG src=&quot;$idir$rs_img&quot; alt=&quot;����&quot; border=&quot;0&quot;&gt;&lt;/A&gt;";
}

print qq|<DIV class="sourse">\n|;

#�����g�p���g�p���R�����g�L���̕���
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
		alert (&quot;���ڂ��`�F�b�N����Ă��܂���I&quot;);<BR>
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

#���[�t�H�[���T���v��
print <<EOF;
&lt;!-- ���[�t�H�[�� ID$FORMS{'id'}--&gt;<BR>
$front<BR>
&lt;DIV style=&quot;font-size:13px;width:180px;background-color:$SET{'rback1'};border:solid 1px $SET{'rback2'};padding:3px;&quot;&gt;<BR>
&lt;DIV style=&quot;width:100%;color:$SET{'rfont1'};text-align:left;padding-bottom:3px;&quot;&gt;<BR>
&lt;IMG src=&quot;$idir$qs_img&quot; alt=&quot;����&quot;&gt; $FORMS{'qst'}<BR>
&lt;/DIV&gt;<BR>
&lt;DIV style=&quot;width:100%;text-align:left;background-color:$SET{'rback2'};color:$SET{'rfont2'};border-top:solid 2px $SET{'rshadow'};border-left:solid 2px $SET{'rshadow'};padding:3px;&quot;&gt;<BR>
EOF

#�I��������W�J
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

#�R�����g�t�H�[����W�J
if ($FORMS{'cget'} or $cget) {
	print qq|
	�R�����g&lt;BR&gt;<BR>
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
&lt;IMG src=&quot;$idir$od_img&quot; border=&quot;0&quot; alt=&quot;�ߋ��̓��[&quot; title=&quot;�ߋ��̓��[&quot;&gt;&lt;/A&gt<BR>
&lt;A href=&quot;$web&quot; target=&quot;_blank&quot;&gt;<BR>
&lt;IMG src=&quot;$idir$dw_img&quot; border=&quot;0&quot; alt=&quot;Petit Poll SE �_�E�����[�h&quot;&gt;&lt;/A&gt<BR>
&lt;A href=&quot;$fpath&quot;&gt;<BR>
&lt;IMG src=&quot;$idir$ad_img&quot; border=&quot;0&quot; alt=&quot;�Ǘ�&quot; title=&quot;�Ǘ�&quot;&gt;&lt;/A&gt<BR>
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
	<INPUT type="submit" value="�߂�">
	</FORM>
	|;
}
}



#������������������������������������������������������������������������������������������������������������������
#�����[����
#������������������������������������������������������������������������������������������������������������������
sub on_poll {
#���O���`
my $ptlog = $ldir . $ptname;
my $idlog = $ldir . $FORMS{'id'} . ".log";

unless (-e $idlog) { &error ("�Ăяo���ꂽ���[�͍폜����Ă��܂�"); }

if ($SET{'lkey'}) { if (!&lock_on) { &error ("�T�[�o�[�����ݍ����Ă��܂�"); } }
$now_lock = 1;

if (!open (ID, "<$idlog")) { &error ("���[���O���J���܂���ł���"); }

my @OLDID = <ID>;

close (ID);

#�ݒ胉�C���𔲂�
chomp (my $setline = shift (@OLDID));

#���[��/����/�{������/�R�����g�擾/�R�����g���E/�A��/�A�֊���/�A�֒P��/�I���b��/���E���[/�J�n����/�I������/ing�t���O
my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split(/<>/, $setline);

#���[���ԃ`�F�b�N
if ($period and ($ing == 1) and ($time >= $period)) {
	#���[�^�C�g�����O�X�V
	my @NEWPT=();
	if (!open (PT, "+<$ptlog")) { &error("���[�^�C�g�����O���J���܂���ł���"); }
		while (chomp ($_ = <PT>)){
			my ($id, $ptitle, $ing) = split(/<>/);
			if ($FORMS{'id'} eq $id) {
				push (@NEWPT, "$id<>$ptitle<>2\n");
			} else {
				push (@NEWPT, "$_\n");
			}
		}

	#ID���O�X�V
	if (!open (ID, "+<$idlog")) { &error ("���[���O���J���܂���ł���"); }
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

	&error ("���̓��[�͏I�����܂���");
}

#�i�s�󋵃`�F�b�N
if ($ing == 2) { &error ("���̓��[�͏I�����܂���"); }

#���[���ڃ`�F�b�N
if (!$FORMS{'poll'}) { &error ("���[���ڂ��`�F�b�N����Ă��܂���"); }

#�A�N�Z�X����
my $ip  = $ENV{'REMOTE_ADDR'};
my $ip2 = $ip;
$ip2 =~ s/(\d+\.\d+\.\d+)\.\w+/$1/;

if ($SET{'hkick'} =~ /$ip2/) { &error ("���[��������Ă��܂���"); }

#�R�����g�`�F�b�N
if ($FORMS{'com'} eq "undefined" or !$FORMS{'com'}) {
	$FORMS{'com'} = "none";
}
if (($cget == 2) and ($FORMS{'com'} eq "none")) {
	&error ("�I�����ڂւ̃R�����g�͕K�{�ł�");
}
if (length ($FORMS{'com'}) > ($SET{'cleng'} * 2)) {
	&error ("�R�����g�͑S�p��$SET{'cleng'}���ȓ��܂łł�");
}
if ($FORMS{'com'} eq "none") {
	undef ($FORMS{'com'});
}

#�{���������A�����[�`�F�b�N
my ($getcook) = &get_cook (1, $pkick, $kval, $kunit) if (!$reye or $pkick);

#���[��
$count ++;

my $com_ct = 0;		#�R�����g��
my @ID = ();

#�I�����ڂ��C���N�����R�����g�ǉ�
while (chomp ($_ = shift (@OLDID))) {
	#ID�e/ID�q/�I����or�R�����g/���[����/�z�X�g/���[��or�R�����g��
	my ($idno, $idsel, $idq, $idj, $idh, $idct) = split(/<>/);

	#���[���{��
	if (($idno eq $FORMS{'poll'}) or ($idsel eq $FORMS{'poll'})) {
		#�I�������C���X�V�i�e�j
		if ($idno eq $FORMS{'poll'}) {
			$idct ++;
			push (@ID, "$idno<><>$idq<><><>$idct\n");
	
			#�R�����g�ǉ�
			if ($FORMS{'com'}) {
				push (@ID, "<>$idno<>$FORMS{'com'}<>$time<>$ip<>$count\n");
				$com_ct = 1;		#�R�����g�J�E���g
			}
		}else{
			#�R�����g���C���ǉ��i�q�j���R�����g���E�`�F�b�N
			if ($climit > $com_ct) {
				push (@ID, "$_\n");
				$com_ct ++;
			}
		}
	} else {
		#�����[�z��
		push (@ID, "$_\n");
	}
}

#���E���[�`�F�b�N
if ($plimit and ($count >= $plimit)){
	my @NEWPT=();
	if (!open (PT, "+<$ptlog")) { &error("���[�^�C�g�����O���J���܂���ł���"); }
		while (chomp ($_ = <PT>)){
			my ($id, $ptitle, $ing) = split(/<>/, $_);

			if ($id eq $FORMS{'id'}) {
				push (@NEWPT, "$id<>$ptitle<>2\n");
			} else {
				push (@NEWPT, "$_\n");
			}
		}

	#�I�������`
	&opening;

	#���ʕ\���p�̓��t
	$end = $FORMS{'start'};

	if (!open (ID, "+<$idlog")) { &error ("���[���O���J���܂���ł���"); }
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
	#�ʏ�X�V
	if (!open (ID, "+<$idlog")) { &error ("���[���O���J���܂���ł���"); }
	seek (ID, 0, 0);
	print ID "$count<>$qst<>$reye<>$cget<>$climit<>$pkick<>$kval<>$kunit<>$period<>$plimit<>$start<>$end<>$ing\n";
	print ID @ID;
	truncate(ID,tell);
	close(ID);
}

if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

#�N�b�L�[�ݒ�
if (!$reye or $pkick) { &set_cook ($getcook); }

if ($SET{'stype'} == 1) {
	my @TMP = map {(split /<>/)[5]} @ID;
	@ID = @ID[sort{$TMP[$b] <=> $TMP[$a]} 0 .. $#TMP];
} elsif ($SET{'stype'} == 2) {
	my @TMP = map {(split /<>/)[5]} @ID;
	@ID = @ID[sort{$TMP[$a] <=> $TMP[$b]} 0 .. $#TMP];
}

#�����g�p���g�p�̕���
my $cpflag = 0;
if ($SET{'rtype'}) {
	&head (1, "���[����");
	$cpflag = 1;
} else {
	&head (0);
}

&rs_table_top ($count, $qst, $start, $end);

print qq|<OL type="A">\n|;

my ($num);
while (chomp ($_ = shift (@ID))) {
	#�I�������i�e�j / �I�������i�q�j / �I���� / ���[�b�� / �z�X�g / ���[�� or ���[�ԍ�
	my ($idno, $idsel, $idq, $idj, $idh, $idct) = split(/<>/);

	my $rate = 1.7;
	if ($SET{'rtype'}) { $rate = 3; }
	my $per = sprintf ("%.1f", ($idct * 100) / $count);		#�p�[�Z���e�[�W
	my $wid = sprintf ("%d", $per * $rate);				#�摜��
	if (!$GAZOU[$num]) { $num = 0; }				#�o�[�摜��

	#�e�̂ݓW�J
	if ($idno) {
		print "<LI>$idq<BR>\n";
		if ($wid >= 0) {
			if ($wid <= 0) { $wid = 1; }
			print qq|
				<IMG src="$idir$GAZOU[$num]" width="$wid" height="$SET{'bhi'}" alt="$per\%">
				<SPAN style="font-size:12px;">($idct�[/$per%)</SPAN><BR><BR></LI>\n
				|;
		} else {
			print qq|
				<IMG src="$idir$GAZOU[$num]" width="1" height="$SET{'bhi'}" alt="0\%">
				<SPAN style="font-size:12px;">(0�[/0%)</SPAN><BR><BR></LI>\n
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



#����������������������������������������������������������������������������������������������������������������������
#�����[����
#����������������������������������������������������������������������������������������������������������������������
sub result {
#���O���`
my $ptlog = $ldir . $ptname;
my $idlog = $ldir . $FORMS{'id'} . ".log";

unless (-e $idlog) { &error ("�Ăяo���ꂽ���[�͍폜����Ă��܂�"); }

if (!open (ID, "+<$idlog")) { &error("���[���O���J���܂���ł���"); }

my @ID = <ID>;

#�ݒ胉�C���𒊏o
chomp (my $setline = shift (@ID));

#���[��/����/�{������/�R�����g�擾/�R�����g���E/�A��/�A�֊���/�A�֒P��/�I���b��/���E���[/�J�n����/�I������/ing�t���O
my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split (/<>/, $setline);

#�{�������`�F�b�N
my ($getcook, $ckflag) = &get_cook if (!$reye and $ing == 1);

if (!$reye and !$ckflag and !$FORMS{'r'} and $ing ==1) { &error ("���[�O�̌��ʂ̉{������������Ă��܂�"); }

#���[���ԃ`�F�b�N
if ($ing == 1 and $period and $time >= $period and !$FORMS{'r'}){
	if ($SET{'lkey'}) { if (!&lock_on) { &error ("�T�[�o�[�����ݍ����Ă��܂�"); } }
	$now_lock = 1;

	my @NEWPT = ();
	if (!open (PT, "+<$ptlog")) { &error("���[�^�C�g�����O���J���܂���ł���"); }
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

	#ID���O�X�V
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

#�����g�p���g�p�̕���
my $cpflag = 0;
if ($SET{'rtype'} or $FORMS{'r'}) {
	&head (1, "���[����");
	$cpflag = 1;
} else {
	&head (0);
}

&rs_table_top ($count, $qst, $start, $end);

print qq|<OL type="A">\n|;

$count ||= 1;

my ($num);
while (chomp ($_ = shift (@ID))) {
	#�I�������i�e�j / �I�������i�q�j / �I���� / ���[�b�� / �z�X�g / ���[�� or ���[�ԍ�
	my ($idno, $idsel, $idq, $idj, $idh, $idct) = split(/<>/);

	my $rate = 1.7;
	if ($SET{'rtype'} or $FORMS{'wide'} or $FORMS{'r'}) { $rate = 3; }

	my $per = sprintf ("%.1f", ($idct * 100) / $count);		#�p�[�Z���e�[�W
	my $wid = sprintf ("%d", $per * $rate);				#�摜��
	if (!$GAZOU[$num]) { $num = 0; }				#�o�[�摜��

	#�e�̂ݓW�J
	if ($idno) {
		print "<LI>$idq<BR>\n";
		if ($wid >= 0) {
			if ($wid <= 0) { $wid = 1; }
			print qq|
				<IMG src="$idir$GAZOU[$num]" width="$wid" height="$SET{'bhi'}" alt="$per\%">
				<SPAN style="font-size:12px;">($idct�[/$per%)</SPAN><BR><BR></LI>\n
				|;
		} else {
			print qq|
				<IMG src="$idir$GAZOU[$num]" width="1" height="$SET{'bhi'}" alt="0\%">
				<SPAN style="font-size:12px;">(0�[/0%)</SPAN><BR><BR></LI>\n
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



#����������������������������������������������������������������������������������������������������������������������
#�����[���ʃe�[�u��
#����������������������������������������������������������������������������������������������������������������������
sub rs_table_top {
my ($count, $qst, $start, $end, $mikey) = @_;

#�g��k���A�C�R��
my $wd_icon = <<WIDE;
<SPAN style="text-align:right;width:100%">
<A href="javascript:WideWin('$FORMS{'id'}');"><IMG src="$idir$wn_img" border="0" alt="�g��k��"></A>
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
<IMG src="$idir$qs_img" alt="����">
$qst
</SPAN>
$wd_icon
</DIV>
<DIV style="clear:left;width:100%;text-align:left;background-color:$SET{'rback2'};color:$SET{'rfont2'};border-top:solid 2px $SET{'rshadow'};border-left:solid 2px $SET{'rshadow'};padding:3px;">
<DIV class="period">[���[����] $start �` $end [���[��] $count�[</DIV>

EOF
}

sub rs_table_bottom {
my ($id, $cget, $cvflag) = @_;

print <<EOF;
<FORM action="$fpath" method="POST">
<DIV align="center">
EOF

#�ߋ����O�{���L�[/�ʏ펞CLOSE/�߂�{�^��
my ($root, $back, $p, $close);
if ($FORMS{'r'}) {
	$root = qq|<INPUT type="hidden" name="r" value="1">|;
	$back = qq|<INPUT type="button" value="�߂�" onClick="javascript:history.back()">|;
} else {
	if (!$SET{'rtype'}) {
		$close = qq|<INPUT type="button" value="����" onClick="javascript:window.close();">|;
	} else {
		$back = qq|<INPUT type="button" value="�߂�" onClick="javascript:history.back()">|;
	}
}

#�R�����g�{�^��
if (!$SET{'ctype'} and $cget and $cvflag) {
	print qq|
		<INPUT type="hidden" name="mode" value="cview">
		<INPUT type="hidden" name="id" value="$id">
		<INPUT type="hidden" name="wide" value="$FORMS{'wide'}">
		$root
		<INPUT type="submit" value="�R�����g������">
		$back
		|;
} elsif ($FORMS{'mode'} eq "cview" and !$FORMS{'r'} and !$SET{'rtype'}) {
	print qq|
		<INPUT type="hidden" name="mode" value="result">
		<INPUT type="hidden" name="id" value="$id">
		<INPUT type="hidden" name="wide" value="$FORMS{'wide'}">
		$root
		<INPUT type="submit" value="�߂�">
		|;
} elsif ($back) {
	print "$back\n";
}

#���쌠���폜�E���Ҍ��ցI�I
print <<EOF;
$close
</FORM>
</DIV>
<SPAN style="text-align:right;width:100%;">
<A href="$web" target="_blank"><IMG src="$idir$dw_img" alt="Petit Poll SE �_�E�����[�h" border="0"></A>
</SPAN>

EOF
}



#����������������������������������������������������������������������������������������������������������������������
#���R�����g�{��
#����������������������������������������������������������������������������������������������������������������������
sub com_view {
if (!$FORMS{'id'}) { ($FORMS{'id'}, $FORMS{'pass'}, $FORMS{'cdkey'}) = @_; }

if ($SET{'ctype'} and !$FORMS{'cdkey'}) { &error ("�R�����g�͊Ǘ��҂������邱�Ƃ��ł��܂���"); }

#���O���`
my $idlog = $ldir . $FORMS{'id'} . ".log";

if (!open (ID, "+<$idlog")) { &error("���[���O���J���܂���ł���"); }

#�ݒ胉�C���𒊏o
chomp (my $setline = <ID>);

#���[��/����/�{������/�R�����g�擾/�R�����g���E/�A��/�A�֊���/�A�֒P��/�I���b��/���E���[/�J�n����/�I������/ing�t���O
my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split (/<>/, $setline);

if (!$cget) { &error ("�R�����g�擾�@\�\\�͎g�p���Ă��܂���"); }

#�����g�p���g�p�̕���
my $cpflag = 0;
if ($FORMS{'cdkey'}) {
	&head (1, "�R�����g�폜���");
	$cpflag = 1;
} elsif ($SET{'rtype'} or $FORMS{'r'}) {
	&head (1, "�R�����g�{��");
	$cpflag = 1;
} else {
	&head (0);
}

#�폜���[�h �O�^�O�}��
if ($FORMS{'cdkey'}) {
	print qq|
		<DIV style="width:400px;text-align:left;line-height:18px;">
		*�폜�������R�����g���`�F�b�N���č폜�{�^���������ƍ폜���邱�Ƃ��o���܂��B<BR>
		*�z�X�g�������s�������ꍇ�A�폜�O�ɃJ�b�R���̐������������Ă����ĉ������B<BR>
		*���M��̂�蒼���͂ł��܂���̂Œ��ӂ��Ă��������B�i�m�F��ʂ͏o�܂���j
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
	#�I�������i�e�j / �I�������i�q�j / �I���� / ���[�b�� / �z�X�g / ���[�� or ���[�ԍ�
	my ($idno, $idsel, $idq, $idj, $idh, $idct) = split(/<>/);

	if (!$r and $idno) {
		#�擪
		print qq|
			<BR><BR>
			<DIV class="com1">��$idq</DIV>
			<OL type="disc">
			|;
		$r = $idno;
	} elsif ($idno) {
		if ($chflag) {
			#���e�i�O�e�ɃR�����g�L��j
			print qq|
				</OL>
				|;
		} else {
			#���e�i�O�e�ɃR�����g�����j
			print qq|
				<LI class="com2">�R�����g�͂܂�����܂���</LI>
				</OL>
				|;
		}

		print qq|
			<BR><BR>
			<DIV class="com1">��$idq</DIV>
			<OL type="disc">
			|;

		#���[�g�X�V�A�t���O�[��
		$r = $idno;
		$chflag = 0;
		next;
	} elsif ($r eq $idsel) {
		#�R�����g
		if ($time < ($idj + ($SET{'nmark'} * 60 * 60))) {
			$new_com = qq |<IMG src="$idir$nw_img" alt="�V��">|;
		}

		#�폜���[�h��p�{�^�����z�X�g�\��
		if ($FORMS{'cdkey'}) {
			$del_box = qq|<INPUT type="checkbox" name="delarray" value="$idct">|;
			$host = qq|<SPAN class="em_font">�i$idh�j</SPAN>|;
		}

		print qq|<LI class="com2">$del_box $idq $host $new_com</LI>\n|;
		$chflag = 1;
		undef ($new_com);
	}

}

close (ID);

if (!$chflag) {
	print qq|
		<LI class="com2">�R�����g�͂܂�����܂���</LI>
		</OL><BR><BR>
		|;
} else {
	print "</OL><BR><BR>\n";
}

if (!$FORMS{'cdkey'}) {
	&rs_table_bottom ($FORMS{'id'}, $cget, 0);
} else {
	#�폜���[�h ��^�O�}��
	print qq|
		<DIV align="center">
		<TABLE cellpadding="0" cellspacing="3" border="0" summary="�{�^��">
		<TR><TD>
		<INPUT type="hidden" name="mode" value="comdel">
		<INPUT type="hidden" name="id" value="$FORMS{'id'}">
		<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
		<INPUT type="hidden" name="cdkey" value="$FORMS{'cdkey'}">
		<INPUT type="submit" value="�R�����g�폜">
		</FORM>
		</TD><TD>
		<FORM method="POST" action="$fpath">
		<INPUT type="hidden" name="mode" value="maint">
		<INPUT type="hidden" name="id" value="$FORMS{'id'}">
		<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
		<INPUT type="submit" value="�����e�i���X���">
		</FORM>
		</TABLE>
		</DIV>\n
		|;
}

print "</DIV></DIV>\n";

&foot ($cpflag);
}



#����������������������������������������������������������������������������������������������������������������������
#�������e�i���X
#����������������������������������������������������������������������������������������������������������������������
sub maint {
#�ē����L�[���擾
my ($id, $pass) = @_ if (!$FORMS{'act'});

#�ē����΍�Ń��[�h���Œ�
$FORMS{'mode'} = "maint";

if ($FORMS{'pass'} ne $SET{'pass'}) {
	&error("�s���ȃA�N�Z�X�ł�");
} elsif (!$FORMS{'id'}) {
	&error ("�ҏW�{�^���Ƀ`�F�b�N�������Ă��܂���");
}

#���O���`
my $idlog = $ldir . $FORMS{'id'} . ".log";

unless (-e $idlog) { &error ("�Ăяo���ꂽ���[�͍폜����Ă��܂�"); }

if (!open (ID, "+<$idlog")) { &error("���[���O���J���܂���ł���"); }

chomp (my $setline = <ID>);

#���[��/����/�{������/�R�����g�擾/�R�����g���E/�A��/�A�֊���/�A�֒P��/�I���b��/���E���[/�J�n����/�I������/ing�t���O
my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split (/<>/, $setline);

&head (1, "�����e�i���X���");

print <<EOF;
<SPAN style="width:500px;text-align:left;line-height:18px;">
*�u�ݒ�ύX�v����A�e��ݒ��ύX���邽�߂̃t�H�[���֍s�����Ƃ��o���܂��B<BR>
*�u�R�����g�폜��ʁv�ł́A�R�����g�̉{���A�폜���s�����Ƃ��o���܂��B<BR>
*�R�����g�̗L����ύX�����ꍇ�A�����̎g�p���g�p��ύX�����ꍇ��\�\\�[�X���������Ă��������B<BR>
*�u���[���Z�b�g�v����ƁA���[�쐬���̏�Ԃɖ߂��܂��B�i���[���[���Őݒ�̓f�t�H���g�j<BR>
*�u���[�I���v����ƁA���̏�ŉߋ����O�����邱�Ƃ��ł��܂��B<BR>
*�u���[�폜�v����ƁA���̓��[�����S�ɍ폜����܂��B<BR>
*���M��̂�蒼���͂ł��܂���̂ł����ӂ��������B�i�m�F��ʂ͏o�܂���j<BR>
</SPAN>
<BR>
<BR>
<BR>

<TABLE cellpadding="0" cellspacing="3" botder="0" summary="�ݒ胁�j���[">
<TR>
<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="admin">
<INPUT type="hidden" name="act" value="1">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="�Ǘ��z�[��">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="edit">
<INPUT type="hidden" name="ing" value="$ing">
<INPUT type="hidden" name="id" value="$FORMS{'id'}">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="�ݒ�ύX">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="cview">
<INPUT type="hidden" name="cdkey" value="1">
<INPUT type="hidden" name="id" value="$FORMS{'id'}">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="�R�����g�폜���">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="re_set">
<INPUT type="hidden" name="id" value="$FORMS{'id'}">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="���[���Z�b�g">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="p_end">
<INPUT type="hidden" name="id" value="$FORMS{'id'}">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="���[�I��">
</FORM>
</TD>

<TD>
<FORM method="POST" action="$fpath">
<INPUT type="hidden" name="mode" value="p_del">
<INPUT type="hidden" name="id" value="$FORMS{'id'}">
<INPUT type="hidden" name="pass" value="$FORMS{'pass'}">
<INPUT type="submit" value="���[�폜">
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
	#�I�������i�e�j / �I�������i�q�j / �I���� / ���[�b�� / �z�X�g / ���[�� or ���[�ԍ�
	my ($idno, $idsel, $idq, $idj, $idh, $idct) = split(/<>/);

	my $per = sprintf ("%.1f", ($idct * 100) / $count);		#�p�[�Z���e�[�W
	my $wid = sprintf ("%d", $per * 1.7);				#�摜��
	if (!$GAZOU[$num]) { $num = 0; }				#�o�[�摜��

	#�e�̂ݓW�J
	if ($idno) {
		print "<LI>$idq<BR>\n";
		if ($wid >= 0) {
			if ($wid <= 0) { $wid = 1; }
			print qq|
				<IMG src="$idir$GAZOU[$num]" width="$wid" height="$SET{'bhi'}" alt="$per\%">
				<SPAN style="font-size:12px;">($idct�[/$per%)</SPAN><BR><BR></LI>\n
				|;
		} else {
			print qq|
				<IMG src="$idir$GAZOU[$num]" width="1" height="$SET{'bhi'}" alt="0\%">
				<SPAN style="font-size:12px;">(0�[/0%)</SPAN><BR><BR></LI>\n
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
&lt;�\\�[�X��\\������&gt;
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



#����������������������������������������������������������������������������������������������������������������������
#���ݒ�ύX
#����������������������������������������������������������������������������������������������������������������������
sub relog {
if ($FORMS{'climit'} =~ /\D/) { &error ("���E�R�����g���ɖ����Ȑ��l���܂܂�Ă��܂�"); }
if ($FORMS{'plimit'} =~ /\D/) { &error ("���E���[���ɖ����Ȑ��l���܂܂�Ă��܂�"); }
if ($FORMS{'kval'}   =~ /\D/) { &error ("�A�����[�֎~���Ԃɖ����Ȑ��l���܂܂�Ă��܂�");}

my $idlog = $ldir . $FORMS{'id'} . ".log";

if ($SET{'lkey'}) { if (!&lock_on) { &error ("�T�[�o�[�����ݍ����Ă��܂�"); } }
$now_lock = 1;

if (!open (ID, "+<$idlog")) { &error("���[���O���J���܂���ł���"); }

my @ID = <ID>;

chomp (my $setline = shift (@ID));

#���[��/����/�{������/�R�����g�擾/�R�����g���E/�A��/�A�֊���/�A�֒P��/�I���b��/���E���[/�J�n����/�I������/ing�t���O
my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split (/<>/, $setline);

#�I����
&finale;

#���E�R�����g
if (!$FORMS{'climit'}) { $FORMS{'climit'} = 5;}

#���E���[���̃`�F�b�N
if ($FORMS{'plimit'} and $FORMS{'plimit'} < $count) { &error ("�w�肳�ꂽ���E���[���͊��ɒ����Ă��܂�"); }

#�R�����g���C���̃`�F�b�N�ƍ폜
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



#����������������������������������������������������������������������������������������������������������������������
#���R�����g�폜����
#����������������������������������������������������������������������������������������������������������������������
sub com_delete {
my $idlog = $ldir . $FORMS{'id'} . ".log";

if ($SET{'lkey'}) { if (!&lock_on) { &error ("�T�[�o�[�����ݍ����Ă��܂�"); } }
$now_lock = 1;

if (!open (ID, "+<$idlog")) { &error ("���[���O���J���܂���ł���"); }

chomp (my $setline = <ID>);

my (@NEWID, $dlflag, $val);
while (chomp ($_ = <ID>)) {
	my ($idno, $selid, $idq, $idj, $idh, $idct) = split(/<>/);

	#�R�����g�̂ݍ폜
	if (!$idno) {
		foreach $val (@DEL) {
			if ($idct eq $val){
				$dlflag = 1;
				last;
			}
		}

		#�ΏۊO
		if (!$dlflag) { push (@NEWID, "$_\n"); }
	} else {
		#�I����
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



#����������������������������������������������������������������������������������������������������������������������
#�����[���Z�b�g
#����������������������������������������������������������������������������������������������������������������������
sub re_set {
my $ptlog = $ldir . $ptname;
my $idlog = $ldir . $FORMS{'id'} . ".log";

if ($SET{'lkey'}) { if (!&lock_on) { &error ("�T�[�o�[�����ݍ����Ă��܂�"); } }
$now_lock = 1;

if (!open (ID, "+<$idlog")) { &error ("���[���O���J���܂���ł���"); }

chomp (my $setline = <ID>);

#���[��/����/�{������/�R�����g�擾/�R�����g���E/�A��/�A�֊���/�A�֒P��/�I���b��/���E���[/�J�n����/�I������/ing�t���O
my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split (/<>/, $setline);

#�J�n��
&opening;

#�I�����擾
my @ID = ();
while (chomp ($_ = <ID>)) {
	my ($idno, $selid, $idq, $idj, $idh,  $idc) = split (/<>/);

	if ($idno) { push (@ID, "$idno<><>$idq<><><>0\n"); }
}

#���[�^�C�g�����O�X�V
if ($ing != 0) {
	my @PT = ();
	if (!open (PT, "+<$ptlog")) { &error ("���[�^�C�g�����O���J���܂���ł���"); }
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
print ID "0<>$qst<>1<>0<>5<>0<>0<>0<>0<>0<>$FORMS{'start'}<>������<>1\n";
print ID @ID;
truncate (ID, tell);

close (ID);

if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

&maint ($FORMS{'id'}, $FORMS{'pass'});
}



#����������������������������������������������������������������������������������������������������������������������
#�����[�I��
#����������������������������������������������������������������������������������������������������������������������
sub poll_end {
my $ptlog = $ldir . $ptname;
my $idlog = $ldir . $FORMS{'id'} . ".log";

if ($SET{'lkey'}) { if (!&lock_on) { &error ("�T�[�o�[�����ݍ����Ă��܂�"); } }
$now_lock = 1;

#PT���O�X�V
my @PT = ();
if (!open (PT, "+<$ptlog")) { &error("���[�^�C�g�����O���J���܂���ł���"); }
	while (chomp ($_ = <PT>)) {
		my ($id, $ptitle, $ing) = split(/<>/);

		if ($id eq $FORMS{'id'}) {
			push (@PT, "$id<>$ptitle<>2\n");
		} else {
			push (@PT, "$_\n");
		}
	}

	#ID���O�X�V
	if (!open (ID, "+<$idlog")) { &error("���[���O���J���܂���ł���"); }

	my @ID = <ID>;
	
	chomp (my $setline = shift (@ID));
	
	#���[��/����/�{������/�R�����g�擾/�R�����g���E/�A��/�A�֊���/�A�֒P��/�I���b��/���E���[/�J�n����/�I������/ing�t���O
	my ($count, $qst, $reye, $cget, $climit, $pkick, $kval, $kunit, $period, $plimit, $start, $end, $ing) = split (/<>/, $setline);

	#�I�������`
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



#����������������������������������������������������������������������������������������������������������������������
#�����[�폜
#����������������������������������������������������������������������������������������������������������������������
sub poll_del {
my $ptlog = $ldir . $ptname;
my $idlog = $ldir . $FORMS{'id'} . ".log";

if ($SET{'lkey'}) { if (!&lock_on) { &error ("�T�[�o�[�����ݍ����Ă��܂�"); } }
$now_lock = 1;

my @PT = ();
if (!open (PT, "+<$ptlog")) { &error ("���[�^�C�g�����O���J���܂���ł���"); }
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

#�폜��΍�̂��߁A�ē����L�[���폜
undef ($FORMS{'act'});

&admin ($FORMS{'pass'});
&foot (1);
}



#����������������������������������������������������������������������������������������������������������������������
#���ߋ����O
#����������������������������������������������������������������������������������������������������������������������
sub old {
my $ptlog = $ldir . $ptname;

unless (-e $ptlog) { &error ("���̓��[�̗��p�͋x�~����Ă��܂�"); }

#���ݍs���Ă��铊�[�^�C�g�����擾
if (!open(PT, "<$ptlog")) { &error ("�ߋ����O���J���܂���ł���"); }

&head (1, "�ߋ����[");

print <<EOF;
*���[�^�C�g�����N���b�N����ƍŏI���ʂ������ɂȂ�܂��B
<BR>
<BR>

<DIV class="oframe">
<TABLE cellpadding="3" cellspacing="1" border="0" summary="���X�g">
<TR>
<TD class="pline1" style="width:40px;">ID</TD>
<TD class="pline1" style="width:400px;">���[�^�C�g��</TD>
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
		<TD class="pline2">�I���������[�͂���܂���</TD></TR>
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
<INPUT type="button" value="�߂�" onClick="javascript:history.back()">
</DIV>
</FORM>

EOF

&foot (1);
}



#����������������������������������������������������������������������������������������������������������������������
#�����[�S�폜
#����������������������������������������������������������������������������������������������������������������������
sub use_end {
my $ptlog = $ldir . $ptname;

if ($SET{'lkey'}) { if (!&lock_on) { &error ("�T�[�o�[�����ݍ����Ă��܂�"); } }
$now_lock = 1;

#���[�^�C�g�����O��������
if (!open (PT, "+<$ptlog")) { &error ("���[�^�C�g�����O���J���܂���ł���"); }

my @PT = <PT>;
my $on = @PT;

seek (PT, 0, 0);
truncate (PT, tell);
close (PT);

#�e���[���O��S�폜
my ($i);
for ($i = 1; $i <= $on; $i ++) {
	my $idlog = $ldir . $i . ".log";
	if (-e $idlog) { unlink ("$idlog"); }
	undef ($idlog);
}

if ($SET{'lkey'} and $now_lock) { rmdir ($lock); }

#�폜��΍�̂��߁A�ē����L�[���폜
undef ($FORMS{'act'});

&admin ($FORMS{'pass'});
&foot (1);
}



#����������������������������������������������������������������������������������������������������������������������
#���J�n��
#����������������������������������������������������������������������������������������������������������������������
sub opening {
my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime ($time);

$mon++;
$year += 1900;
$year = substr ("$year", 2);

$FORMS{'start'} = sprintf ("%s/%02d/%02d", $year, $mon, $mday);
}



#����������������������������������������������������������������������������������������������������������������������
#���I����
#����������������������������������������������������������������������������������������������������������������������
sub finale {
if (!$FORMS{'period'}) {
	$FORMS{'end'} = "������";
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



#����������������������������������������������������������������������������������������������������������������������
#���N�b�L�[�擾
#����������������������������������������������������������������������������������������������������������������������
sub get_cook {
my ($pcflag, $pkick, $kval, $kunit) = @_;
my ($tani, $kakeru, %COOKIE, $ckflag, $getcook);

if ($pcflag) {
	if (!$kunit) {
		$tani = "��"; $kakeru = 60;
	} elsif ($kunit == 1) {
		$tani = "����"; $kakeru = 3600;
	} elsif ($kunit == 2) {
		$tani = "��"; $kakeru = 86800;
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
				&error ("���[�͈�l��񂵂��ł��܂���");
			} elsif ($val + ($kval * $kakeru) < $time) {
				$val = $time;
			} else {
				&error ("���[��$kval$tani�Ɉ�񂵂��ł��܂���");
			}
		}

		$ckflag = 1;
	}

	$getcook .= "$key<>$val,";
}

if (!$ckflag and $pcflag) { $getcook .= "$FORMS{'id'}<>$time,"; }

return ($getcook, $ckflag);
}



#����������������������������������������������������������������������������������������������������������������������
#���N�b�L�[�ݒ�
#����������������������������������������������������������������������������������������������������������������������
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



#����������������������������������������������������������������������������������������������������������������������
#���t�@�C�����b�N ON
#����������������������������������������������������������������������������������������������������������������������
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



#������������������������������������������������������������������������������������������������������������������
#���G���[
#������������������������������������������������������������������������������������������������������������������
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
ERROR�I
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



#������������������������������������������������������������������������������������������������������������������
#���w�b�_�[
#������������������������������������������������������������������������������������������������������������������
sub head {
#$hdflag=�w�b�_�[ / $room=���[���l�[��
my ($hdflag, $room)= @_;

#�y�[�W�w�b�_�[
my $hdline =<<HEAD;
<BR>
<SPAN style="text-align:left;width:85%;"><A href="$SET{'home'}">���z�[���y�[�W��</A></SPAN>

<DIV class="head">$room</DIV>
<BR>
<BR>

HEAD

#���[���l�[���ƃ}�[�W��
my ($margin);
if (!$hdflag) {
	undef ($hdline);
	$margin = 0;
} else {
	$margin = 13;
}

#���C�h�E�B���h�E
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



#������������������������������������������������������������������������������������������������������������������
#���t�b�^�[�i�폜�E���Ҍ��ցj
#������������������������������������������������������������������������������������������������������������������
sub foot {
my ($cpflag) = @_;

#������ȉ��̕����͍폜���ό���
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