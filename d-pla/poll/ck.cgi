#!/usr/local/bin/perl

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃Petit Poll Conversion Kit(2002/09/02)
#┃Copyright(C) 2002 9TST4. All Rights Reserved.
#┃URL：http://paxs.hp.infoseek.co.jp/
#┃E-mail：axs@cocoa.freemail.ne.jp
#┃Web Master：高見将智(Masatomo Takami)
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#┌─────────────────────────────────────────────────────────┐
#│【注意事項】
#│１：このスクリプトは、Petit Poll ver3.2以前のバージョンからバージョンUPする際に、
#│　　ログを継続して使えるようにするためのものです。
#│２：SE ver1.0以降からPetit Pollを初めて使用する方は必要ありませんので、サーバーへ
#│　　アップする際にはこのファイルは削除してかまいません。
#│３：ログの更新後にPetit Pollへのログ持ち越しはできません。
#│４：使用後は誤作動を防ぐため、このファイルはサーバーから削除してください。
#│５：万が一の時のため、実行前にログのバックアップを取っておく事をお奨めいたします。
#│
#│【使い方】
#│１：設定の項目を個々の環境に合わせ修正してください。
#│２：サーバーにアップしたら、このファイルを「一度だけ」呼び出してください。
#│３：新設定はPetit Poll SE本体の管理モードで行えます。
#│
#│【免責】
#│このスクリプトを使用して起きた、いかなる損害に対して制作者は一切の責任を負いません。
#│
#└─────────────────────────────────────────────────────────┘



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃設定（必ず使用中のPetit Poll SE本体の設定と同じにしてください）
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#ログディレクトリ
$dir="./dir/";

#投票ログ（投票タイトルのみを抽出する大元のログ）
$pt_log="pt.log";

#ロックディレクトリ
$l_dir="lock";

#ファイルロックの使用未使用（1=使用、0=未使用）
$key=0;

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃更新処理
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
if($key){&lock_on;}				#ファイルロック開始
$pt_log2=$dir.$pt_log;				#投票ログを定義

#投票ログを開く
open(PT,"<$pt_log2") || &error("サーバーが混み合っています");
@PT=<PT>;					#配列に読み込み
$endid=@PT;					#作成済みの投票数を取得
close(PT);


@TLINE=();
@ILINE=();
#投票ログから各投票タイトルを取得
foreach $pt (@PT){
	chomp($pt);
	($id,$ptitle,$ing)=split(/<>/,$pt);
	push(@TLINE,"$ptitle");
	push(@ILINE,"$ing");
}

$ENV{'TZ'}="JST-9";				#日本時間に合わせる
$byousuu=time();				#秒数を取得
#各投票ログを更新
for($i=1; $i <= $endid; $i++){
	#各投票ログを定義
	$id_log2=$dir.$i.".log";

	#存在をチェック
	if(-e $id_log2){
		#各投票ログを開く
		open(ID,"+<$id_log2") || &error("サーバーが混み合っています");
		@ID=<ID>;

		#ヘッダー情報を取得
		$ct=shift(@ID);

		chomp($ct);

		#ヘッダー情報に新しい要素を追加
		#投票数/質問/閲覧制限/コメント取得/コメント限界/連禁/連禁期間/連禁単位/終了秒数/限界投票/開始時刻/終了時刻/ingフラグ
		$a=$i-1;
		#終了期限の分岐
		if($ILINE[$a] eq "2"){
			$kigen=$byousuu;
			($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=localtime($kigen);
			$mon++;
			$year+=1900;
			$year=substr("$year",2);
			$end=sprintf("$year/%02d/%02d",$mon,$mday);
		}else{
			$kigen="0";
			$end="無期限";
		}
		#整形
		$ctline="$ct<>$TLINE[$a]<>1<>0<>5<>0<>0<>1<>$kigen<>0<>不明<>$end<>$ILINE[$a]";

		#項目ラインの整形
		@NEWID=();
		foreach $_ (@ID){
			($pid,$psel,$pct)=split(/<>/,$_);
			$rline="$pid<><>$psel<><><>$pct";
			push(@NEWID,"$rline\n");
		}
		seek(ID,0,0);
		unshift(@NEWID,"$ctline\n");
		print ID @NEWID;
		truncate(ID,tell);
		close(ID);
	}
}


if($l_flag){&lock_off;}					#ファイルロック解除
&error("更新は正常に完了しました");



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃エラー処理
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub error{
print "Content-type:text/html\n\n";
print <<EOF;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<TITLE>Petit Poll Conversion Kit</TITLE>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
</HEAD>
<BODY>
<CENTER>
<BR><BR>
<SPAN style="color:#ff6666;font-size:10pt;font-weight:bold">$_[0]</SPAN>
<BR><BR><BR>
<A href="javascript:history.back()" style="font-size:10pt">戻る</A>
</CENTER>
</BODY>
</HTML>
EOF

exit;
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃ファイルロック開始
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub lock_on{
$retry=5;
if (-e $l_dir){
	$maked=(stat($l_dir))[9];
	if($maked < time - 60){&lock_off;}
}
while (!mkdir($l_dir, 0755)){
	if(--$retry <= 0){ &error("サーバーが混み合っています");}
	sleep(1);
}
$l_flag=1;
}



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃ファイルロック解除
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
sub lock_off{
rmdir($l_dir);
$l_flag=0;
}
