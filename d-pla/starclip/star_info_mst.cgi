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

# �K�v�ȃt�@�C���̃p�X�w�� ------------------------------------------------

require './jcode.pl';
require './boardini.cgi';
require './skinini.cgi';

# �ݒ�I�� ----------------------------------------------------------------

# -------------------------------------------------------------------------
# ��{����
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
# �t�H�[���f�[�^���f�R�[�h���邽�߂̃T�u���[�`��
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
		$value =~ s/\�@\r\�@\r//g;
		$value =~ s/ \r/\r/g;
		$value =~ s/\�@\r/\r/g;
		$value =~ s/\r\r\r\r//g;

		$value =~ s/&/&amp;/g;
		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
		$value =~ s/,/\0/g;
	
		if ($tagset eq 'off') {
			$value =~ s/"/&quot;/g;
		}

# jcode.pl �ɂ�镶���R�[�h�̕ϊ� -------------------------------
	
		&jcode'convert(*value,'sjis');
		&jcode'h2z_sjis(*value);


# �n�b�V���Ɋi�[ ------------------------------------------------

		if ($property eq 'target'){
			push(@RM,$value);
		} else {
		$FORMDATA{$property} = $value;
		}
	}
}

# -------------------------------------------------------------------------
# ���X�p�̃��b�Z�[�W���͉�ʂ̕\��
# -------------------------------------------------------------------------

sub read_mes_res {

# �f�[�^�t�@�C����ǂݍ��� --------------------------------------

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
		&print_error("�p�X���[�h���s�K�؁A�������͐������ݒ肳��Ă��܂���B");
	}

# �f�[�^�̐��𒲂ׂ� --------------------------------------------

	$volume = scalar(@txt);

# �\���͈͂̐ݒ� ------------------------------------------------

	$msgstart = $msgnum;

	if ($msgstart < 0) {
		$msgstart = 0;
	}

	$msgend = $msgnum + $data_out;

	if ($msgend > $volume) {
		$msgend = $volume;
	}

# ��ʂɕ\������O�̐ݒ� ----------------------------------------

	
	if ($command eq 'f_read') {
		undef %cookie;
		$cookie{'pwd'}  = $pwd;

		&print_cookie($mt_cookiename, 1);

	}
	
	print "Content-type: text/html; charset=Shift_JIS\n\n";
	
# �w�b�_�����̍쐬�ƕϊ� ----------------------------------------

	print "<html>\n";
	print "<head>\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
	print "<title>For Webmaster</title>\n";
	print "</head>\n";

	print "<body>\n";
	print "<center>\n";
	print "�@<br>\n";
	print "<b><font size=\"6\" face=\"Arial,Helvetica\">For Webmaster</font></b><br>\n";
	print "<form method=\"post\" action=\"$masterurl\">\n";
	print "�����͊Ǘ��җp�̃y�[�W�ł��B<br>�Ǘ��҈ȊO�̃A�N�Z�X���֎~���܂��B<br>\n";
	print "<br>\n";
	print "<br>\n";
	print "<a href=\"$bbsurl\">�Ǘ��p�y�[�W���I�����A�\\���p�y�[�W�ɖ߂�B</a><br><br>\n";
	
# ���e�̕\�� ----------------------------------------------------
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
		
# ���O�Ƀ��[���A�h���X�̃����N���͂� ----------------------------

		if($dispmail ne '') {
			$dispname = '<a href="mailto:' . $dispmail . '">' . $dispname . '</a>';
		}
		
# URL�Ƀ����N���͂� ---------------------------------------------

		if($dispurl ne '') {
			$dispurl = '- <a href="' . $dispurl . '" TARGET="_blank">' . Website . '</a>';
		}
		
# ���C�������̍쐬�i�e�����j ------------------------------------

		print "<table width=\"500\" border=\"0\" bgcolor=\"#FFFFFF\" cellpadding=\"5\" cellspacing=\"1\">\n";
		print "<tr>\n";
		print "<td bgcolor=\"#666666\" width=\"40\" align=\"center\" nowrap>\n";
		print "<input type=\"checkbox\" name=\"target\" value=\"$dispid\">\n";
		print "</td>\n";
		print "<td bgcolor=\"#CCCCCC\" width=\"458\">[$dispid] <b>$dispsubject�@</b></td>\n";
		print "</tr>\n";
		print "<tr>\n";
		print "<td valign=\"top\" align=\"center\" bgcolor=\"#666666\" width=\"40\" nowrap><font color=\"#FFFFFF\">���e</font></td>\n";
		print "<td bgcolor=\"#CCCCCC\" width=\"458\">\n";
		print "<font size=\"2\"><font color=\"#CCOOOO\">&lt;$dat_tmp&gt;</font>[$disphost]</font> <br>\n";
		print "<b>$dispsubject</b> by $dispname $dispurl<br>\n";
		print "<p>$dispmsg</p>\n";
		print "</blockquote>\n";
		
# ���C�������̍쐬�i�q�����j ------------------

		open(RES, $res_file) || &print_error('���X�t�@�C�����J���܂���B');
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
				
			# ���O�Ƀ��[���A�h���X�̃����N���͂� ----------------------------
				
			if($dresmail ne '') {
				$dresname = '<a href="mailto:' . $dresmail . '">' . $dresname . '</a>';
			};
			
			# URL�Ƀ����N���͂� ---------------------------------------------

			if($dresurl ne '') {
				$dresurl = '- <a href="' . $dresurl . '" TARGET="_blank">' . Website . '</a>';
			}
				
			print "<hr width=\"96%\">\n";
			print "�@<font size=\"2\"><font color=\"#CCOOOO\">&lt;$res_dat_tmp&gt;</font>[$dreshost]<input type=\"checkbox\" name=\"target\" value=\"$dresnum\">-�폜�p</font> <br>\n";
			print "�@<b>$dressubject</b> by $dresname $dresurl<br>\n";
			print "<blockquote>\n";
			print "<p>$dresmsg</p>\n";
			print "</blockquote>\n";
				
		}
			
		if ($reshtml =~ /ressubject<!--s-->/i){
			print "</td>\n";
			print "</tr>\n";
			print "<tr>\n";
			print "<td valign=\"top\" align=\"center\" bgcolor=\"#666666\" width=\"40\"><font color=\"#FFFFFF\">�薼</font></td>\n";
			print "<td bgcolor=\"#CCCCCC\" width=\"458\">\n";
			print "<input type=\"text\" name=\"subject$dispid\" size=\"30\">\n";
		}
		print "</td>\n";
		print "</tr>\n";
		print "<tr>\n";
		print "<td valign=\"top\" align=\"center\" bgcolor=\"#666666\" width=\"40\" nowrap><font color=\"#FFFFFF\">���X</font></td>\n";
		print "<td bgcolor=\"#CCCCCC\" width=\"458\">\n";
		print "<textarea name=\"resp$dispid\" cols=\"60\" rows=\"4\"></textarea>\n";
		print "</td>\n";
		print "</tr>\n";
		print "</table><br>\n";
	}

# �t�b�^�̍쐬�ƕ�����̕ϊ� ------------------------------------

	$nextmsg = $msgend ;
	print "<table width=\"500\" border=\"0\" bgcolor=\"#666666\" cellpadding=\"5\">\n";
	print "<tr align=\"center\">\n";
	print "<td>\n";
	print "<select name=\"command\">\n";
	print "<option value=\"res_mes\" selected>���X������</option>\n";
	print "<option value=\"remove\">�폜</option>\n";
	print "<option value=\"cg_mtpwd\">�Ǘ��җp�p�X���[�h�ύX</option>\n";
	print "</select>\n";
	print "<input type=\"submit\" name=\"submit\" value=\"�@�@���@��@�@\">\n";
	print "</td>\n";
	print "</tr>\n";
	print "</table>\n";
	print "</form>\n";
	print "<table width=\"500\" border=\"0\">";
	print "<tr>\n";
	print "<td><a href=\"$masterurl?command=read\"><font face=\"Arial,Helvetica\" size=\"4\"><B>&lt; TopLog</b></font></a></td>\n";
	if ($data_out + $msgnum + 1 > $volume) {
		print "<td align=\"right\"><font size=\"5\">�@</font><td>\n";
	} else {
		print "<td align=\"right\"><a href=\"$masterurl?command=read&msgnum=$nextmsg\"><font face=\"Arial,Helvetica\" size=\"4\"><b>OldLog &gt;</b></font></a><td>\n";
	}
	print "</tr>\n";
	print "</table>\n";
	print "</center>\n";
	print "<p>�@</p>\n";
	print "</body>\n";
	print "</html>\n";

	exit(0);
	
}

# -------------------------------------------------------------------------
# ���X���f�[�^�t�@�C���ɏ������ރT�u���[�`��
# -------------------------------------------------------------------------

sub res_message {

	if (!@RM) {
		&print_error('���b�Z�[�W���w�肳��Ă��܂���B<br>�`�F�b�N�{�b�N�X���m�F���ĉ������B');
	}
	

# �f�[�^�t�@�C����ǂݍ��� --------------------------------------

	&get_cookie($mt_cookiename);
	$ck_pwd  = $cookie{'pwd'};

	&lock_open(TXT, "+<$datafile");
	@txt = <TXT>;
	($encoded_pass) = splice(@txt, 0, 1);
	chop($encoded_pass);
	
	if (&mismatch_password($ck_pwd, $encoded_pass)) {
		&unlock_close(TXT);
		&print_error("�p�X���[�h�̗L�����Ԃ��߂��Ă��܂��B<br>�ēx���O�C�����ĉ������B");
	}

# ���X�̑ΏۂƂȂ铊�e������ ------------------------------------

	@tmp = @RM;
	foreach $tgtid(@tmp){
	
		if ($tgtid =~ /_/i){
		&print_error("���X��t����ۂ͐e�L���̂݃`�F�b�N���ĉ������B");
		}
			
		$index = &find_msg;

		if ($index < 0) {
			&unlock_close(TXT);
			&print_error("���̃��b�Z�[�W�͑��݂��܂���B");
		}

		($dispid,$dispname,$dispicon,$dispmail,$dispurl,$dispdate,$disppwd,$dispsubject,$dispmsg,$disphost,$dispres) = split(/,/, $txt[$index]);

		chomp($dispres);

# ���X�̃f�[�^�𐮂��� ------------------------------------------

		$respnum = 'resp' . "$dispid";
		$subjnum = 'subject' . "$dispid";
		$resp = $FORMDATA{"$respnum"};
		$r_subj=$FORMDATA{"$subjnum"};
		
		$resp =~ s/\r/<br>/g;
		
# �^�O�̎g�p�s�̏ꍇ�iURL �Ƀ����N���͂�j --------------------

		if ($tagset eq 'off') {
			if ($autolink ne '') {
				$resp =~ s/(s?https?:\/\/[-_.!~*'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)/<a href="$1" target="_blank">$autolink<\/a>/ig;
			} else {
				$resp =~ s/(s?https?:\/\/[-_.!~*'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)/<a href="$1" target="_blank">$1<\/a>/ig;
			}
		}

# �^�O�̎g�p�̏ꍇ�̊e���� ------------------------------------

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
		

# ��Ƃ̕��� ----------------------------------------------------

		@part_res = split(/:&:/, $dispres);

# ���t�̎擾 ----------------------------------------------------

		$datestr = &get_date_string;

# �L���ԍ��̐ݒ� ------------------------------------------------

		$id = 1;
		for ($i = 0; $i < @part_res; $i++) {
			($thisid) = split(/<>/, $part_res[$i]);
			($pnum,$cnum) = split(/_/,$thisid);
			if ($cnum >= $id) {
				$id = $cnum + 1;
			}
		}

		$id = "$dispid" . '_' . "$id";

# host ���̎擾 -----------------------------------------------

		$host = $ENV{'REMOTE_HOST'};
		$addr = $ENV{'REMOTE_ADDR'};
		if ($host eq $addr) { 
			$host = gethostbyaddr(pack('C4',split(/\./,$host)),2) || $addr;
		}
			
# �������ޏ��̐��� --------------------------------------------

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
# ���b�Z�[�W���폜����T�u���[�`��
# -------------------------------------------------------------------------

sub remove_message {

	if (!@RM) {
		&print_error('���b�Z�[�W���w�肳��Ă��܂���B<br>�`�F�b�N�{�b�N�X���m�F���ĉ������B');
	}
	
	&get_cookie($mt_cookiename);
	$ck_pwd  = $cookie{'pwd'};

	&lock_open(TXT, "+<$datafile");
	@txt = <TXT>;
	($encoded_pass) = splice(@txt, 0, 1);
	chop($encoded_pass);
	
	if (&mismatch_password($ck_pwd, $encoded_pass)) {
		&unlock_close(TXT);
		&print_error("�p�X���[�h�̗L�����Ԃ��߂��Ă��܂��B<br>�ēx���O�C�����ĉ������B");
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
			&print_error("���̃��b�Z�[�W�͑��݂��܂���B");
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
# �Ǘ��җp�p�X���[�h���͉�ʂ̕\��
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
	print "�Ǘ��җp�p�X���[�h����͂��ĉ������B<br><br>\n";
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
# �Ǘ��җp�p�X���[�h�ύX��ʂ̕\��
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
	print "�p�X���[�h�͔��p�p�� 4 �����ȏ�Ŏw��<br><br>\n";
	print "���݂̊Ǘ��җp�p�X���[�h�F\n";
	print "<input type=\"password\" name=\"old_pwd\" size=\"10\"><br><br>";
	print "�V�����Ǘ��җp�p�X���[�h�F\n";
	print "<input type=\"password\" name=\"new_pwd\" size=\"10\"><br><br>";
	print "�m�F�p�ɂ�����x<br><br>\n";
	print "�V�����Ǘ��җp�p�X���[�h�F\n";
	print "<input type=\"password\" name=\"cknew_pwd\" size=\"10\"><br><br>";
	print "<input type=\"submit\" name=\"submit\" value=\"�@�@�ρ@�X�@�@\">\n";
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
# �Ǘ��җp�p�X���[�h�̃`�F�b�N�ƕύX
# -------------------------------------------------------------------------

sub check_change {

	&lock_open(TXT, "+<$datafile");
	@txt = <TXT>;

	($encoded_pass) = splice(@txt, 0, 1);
	chop($encoded_pass);
	
	if ($encoded_pass eq '' || &mismatch_password($old_pwd, $encoded_pass)) {
		&unlock_close(TXT);
		&print_error("���݂̃p�X���[�h���s�K�؁A�������͐������ݒ肳��Ă��܂���B");
	}
	
	if ($new_pwd ne $cknew_pwd) {
		&unlock_close(TXT);
		&print_error('�V�����p�X���[�h���m�F�p�ɓ��͂��ꂽ���̂ƈ�v���܂���B');
	}
	
	if ($new_pwd eq '' || length($new_pwd) < 4) {
		&unlock_close(TXT);
		&print_error('�p�X���[�h�����͂���Ă��Ȃ����A�Z�����܂��B');
	}
	

	$encmaster = &encode_pwd($new_pwd);
	seek(TXT, 0, 0);
	print TXT "$encmaster\n";

	&unlock_close(TXT);
		
	print "Content-type: text/html; charset=Shift_JIS\n";
	print "\n";
	print "<html>\n";
	print "<head>\n";
	print "<title>- �ύX���� -</title>\n";
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
	print "�Ǘ��җp�p�X���[�h��ύX���܂����B<br>\n";
	print "�V�����p�X���[�h�ōă��O�C�����ĉ������B<br><br>\n";
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
# ���b�Z�[�W��T���T�u���[�`��
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
# �t�@�C�����b�N�̃T�u���[�`��
# -------------------------------------------------------------------------

sub lock_open {

	local(*FILE, $lk_name) = @_;
	if (!open(FILE, $lk_name)) {
		&print_error("$lk_name���I�[�v���ł��܂���B");
	}
	if ($lock) {
		eval("flock(FILE, 2)"); # 2=LOCK_EX
		if ($@) {
			&print_error("$@ - ���̊��ł� flock �͎g���܂���B\$uselock = 0 �ɂ��Ă��������B");
		}
	}
	seek(FILE, 0, 0);
	
}

# -------------------------------------------------------------------------
#�t�@�C���A�����b�N�̃T�u���[�`��
# -------------------------------------------------------------------------

sub unlock_close {

	local(*FILE) = @_;
	if ($lock) {
		eval("flock(FILE, 8)"); # 8=LOCK_UN
	}
	close(FILE);
	
}

# -------------------------------------------------------------------------
# �p�X���[�h�̈Í���
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
# �p�X���[�h�̏ƍ�
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
# �N�b�L�[�擾�̃T�u���[�`��
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
# �N�b�L�[�����T�u���[�`��
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
# �N�b�L�[�\���̃T�u���[�`��
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
# ���ݓ����𓾂�T�u���[�`��
# -------------------------------------------------------------------------

sub get_date_string {

	local(@week) = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat");
	local($sec, $min, $hour, $day, $mon, $year, $weekday) = localtime(time);
	$year += 1900;
	$mon++;
	
# �����񉻂��� --------------------------------------------------

	$weekstr = $week[$weekday];
#	return "$year/$mon/$day ($weekstr) $hour:$min";
	return "$year&$mon&$day&$weekstr&$hour&$min";
}

# -------------------------------------------------------------------------
# �G���[�\���̃T�u���[�`��
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
	print "�ēx�����Ă����������A";
	print "<a href=\"mailto:$admin\">$admin</a>";
	print "�܂ł��m�点���������B<br><br>\n";
	print "<font color=\"#CC0000\">�u���E�U��Back�ł��߂艺����</font><br><br>";
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
