# --------------------------------------------------- apeboard+に関する設定

# 時差の修正                                                        ____.00
# サーバが海外にある場合は「-9」の部分を変更すること

$ENV{'TZ'} = 'JST-9';

# -------------------------------------------------------- 管理者関係の設定

# 管理者のメールアドレス                                            ____.01
$admin = 'info@d-plantes.org';

# ホームページの URL                                                ____.02
$indexurl = 'http://www.d-planets.org/index.html';

# 管理者ページ用クッキーの名前                                      ____.03
$mt_cookiename = 'menyako';

# ホームページへの戻り URL                                          ____.04
$back_url = 'http://www.d-planets.org/index.html';

# ------------------------------------------------------ ファイル関連の設定

# 設置するBBSのファイル名                                           ____.05
$thisurl = 'g_book.cgi';

# 管理者ページのファイル名                                          ____.06
$masterurl='g_book_mst.cgi';

# 掲示板本体ページの場所の指定                                      ____.07
#（管理者ページからのパスとファイル名を指定）
$bbsurl = './g_book.cgi';

# データファイルの場所の指定                                        ____.08
$datafile = './sky.dat';

# 表示用ファイルの指定                                              ____.09
$apeskin_html = './apeskin.html';

# レスファイルの指定                                                ____.10
$res_file = 'res_file.html';

# ------------------------------------------------------ 掲示板の動作の設定

# クッキーの名前（必ず変更）                                        ____.11
$cookiename = 'menyako';

# クッキーの有効期限（日数）                                        ____.12
$cookieday = '10';

# 表示される記事件数                                                ____.13
# あまり多くすると重くなるので注意！
$data_out = '10';

# 保存される最大記事件数                                            ____.14
$max_data = '100';

# コメントの最大記入値（0なら無制限）                               ____.15
$maxlength = '0';

# URL の自動リンクの際に使用する文字列                              ____.16
# （無記入 '' の場合は URL をそのまま表示）
$autolink = 'Link';

# タグを使用可にするかどうか（使用可の時は'on'使用不可の時は'off'） ____.17
# この場合使用できるのは（img,font,a,b,i のタグ）
$tagset = 'off';

# imgタグを使用するかどうか（使用可の時は'on'使用不可の時は'off'）  ____.18
$tagimg = 'off';

# fontタグを使用可にするかどうか                                    ____.19
# （使用可の時は'on'使用不可の時は'off'）
$tagfnt = 'off';

# ロックを使用するかどうか（使用する場合は1を入れる）               ____.20
$lock = '1';

# ---------------------------------------------------- マルチレス関連の設定

# 管理者の名前（レス部分で使用可）                                  ____.21
$master_name = 'master';

# レスが書込まれた際にその記事を上に持ってくるかどうか              ____.22
$res_sort = 'on';

# -------------------------------------- 書き込みをメールで送信する際の設定

# 書き込みを管理者宛にメールで送る                                  ____.23
# 通常の書込み時のみ送る場合は  '1' 
# レス書込み時も送るときは '2'
# 使用しないときは '0'
$smail = '0';

# メールを送るときタイトルの前につける文字列（例えば、apeboard）    ____.24
$mail_head = 'hogetest';

# sendmailのパス                                                    ____.25
$sendmail = '/usr/lib/sendmail';

# -------------------------------------------------- 各種セキュリティの設定

# --------------------------------- 他のサイトからの書き込み禁止の設定

# 他のサイトからの書き込みを禁止する                                ____.26
#（禁止するときは'1'、しないときは''）
#（通常の書き込みに支障が出る場合もあるのでその時は''にする）
$fromsite = '';

# 書込むサイトのURL                                                 ____.27
#（フルURLで指定。他のサイトからの書き込みチェックに使用）
#（複数指定する場合はカンマで区切る）
$site = 'http://www.d-planets.org/sky/g_book.cgi';

# ----------------------------------- プロキシからのアクセス規制の設定

# proxyからのアクセスを規制する                                     ____.28
#（規制するときは'1'、しないときは''）
$pcheck = '';

# proxy制限レベル                                                   ____.29
# '1' - 匿名proxy経由の閲覧禁止
# '2' - 全てのproxy経由の閲覧禁止
$plevel = '1';

# ------------------------------- 特定のホストからのアクセス規制の設定

# ホスト名を指定してアクセスを規制する。                            ____.30
#（規制するときは'1'、しないときは''）
$deny_host = '';

# アクセスを規制するホスト名（複数指定する場合はカンマで区切る）    ____.31
$deniedhost = 'xxx.xxx.xxx,xxx.xxx.xxx';

# --------------------------- 特定のIPアドレスからのアクセス規制の設定

# IPアドレスを指定して投稿を規制する。                              ____.32
#（規制するときは'1'、しないときは''）
$deny_IP = '';

# 投稿を規制するIPアドレス（複数指定する場合はカンマで区切る）      ____.33
$deniedip = 'xxx.xxx.xxx.xxx,xxx.xxx.xxx.xxx';

# =========================================================================
# 以下の 1; は絶対に消さないこと！！！
# =========================================================================
1;
# =========================================================================

