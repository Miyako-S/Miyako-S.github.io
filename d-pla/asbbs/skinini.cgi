# ----------------------------------------------------- apeskinに関する設定

# ------------------------------------------------ 各種入力の省略可否の設定

# 名前の入力省略の可否（省略可は''、省略不可は'1'）                 ____.01
$must_name = '1';

# メールアドレス省略の可否（省略可は''、省略不可は'1'）             ____.02
$must_mail = '';

# 削除用パスワード省略の可否（省略可は''、省略不可は'1'）           ____.03
$must_pwd = '';

# ------------------------------------------------------ アイコン関連の設定

# アイコンの横のサイズを指定                                        ____.04
$icon_width = '44';

# アイコンの縦のサイズを指定                                        ____.05
$icon_height= '39';

# アイコンのフォーマットを指定                                      ____.06
$icon_format = 'gif';

# アイコンのパスを指定                                              ____.07
#（html ファイルからの相対パスでも、URL でも OK）
$icon_path = 'img/';

# ------------------------------------------------------ 日付表示関連の設定

# 日付の表示形式                                                    ____.08
# （year,month,day,hour,minute で指定）
$dateline = 'year.month.day.hour:minute';

# 月及び日が 1 桁の時は前に 0 をつけるかどうかを指定                ____.09
# つけるときは 'on' つけないときは 'off'
$addzero_md = 'on';

# 時間及び分が 1 桁の時は前に 0 をつけるかどうかを指定              ____.10
# つけるときは 'on' つけないときは 'off'
$addzero_hm = 'on';

# ------------------------------ メールアドレスのリンク方法の設定（親記事）

# メールアドレスにリンクをはる                                      ____.11
#（はる場合は'1'、はらない場合は''とする）
$mail_link = '';

# 名前にメールアドレスのリンクをはる                                ____.12
#（はる場合は'1'、はらない場合は''とする）
$name_link = '';

# ------------------ 画像にメールアドレスのリンクをはる場合の設定（親記事）

# 画像にメールアドレスのリンクをはる                                ____.13
#（はる場合は'1'、はらない場合は''とする）
$image_mail = '1';

# メールアドレス記入時に使用するリンク用画像（TEXTでもOK）のタグ    ____.14
#（メールアドレスが記入されているとき）
$mail_image01 = 'mail*';

# メールアドレス非記入時に使用する画像（TEXTでもOK）のタグ          ____.15
#（メールアドレスが記入されていないとき）
$mail_image02 = '<S>mail*</S>';

# ----------------------------------------- URLのリンク方法の設定（親記事）

#URLにリンクをはる（はる場合は'1'、はらない場合は''とする）         ____.16
$url_link  = '';

# ----------------------------- 画像にURLのリンクをはる場合の設定（親記事）

# 画像にURLのリンクをはる                                           ____.17
# （はる場合は'1'、はらない場合は''とする）
$image_url = '1';

# URL記入時に使用するリンク用画像（TEXTでもOK）のタグ               ____.18
# （URLが記入されているとき）
$url_image01 = 'home*';

# URL非記入時に使用するリンク用画像（TEXTでもOK）のタグ             ____.19
# （URLが記入されていないとき）
$url_image02 = '<S>home*</S>';

# ------------------------------ メールアドレスのリンク方法の設定（子記事）

# メールアドレスにリンクをはる                                      ____.20
#（はる場合は'1'、はらない場合は''とする）
$res_mail_link = '';

# 名前にメールアドレスのリンクをはる                                ____.21
#（はる場合は'1'、はらない場合は''とする）
$res_name_link = '';

# ------------------ 画像にメールアドレスのリンクをはる場合の設定（子記事）

# 画像にメールアドレスのリンクをはる                                ____.22
#（はる場合は'1'、はらない場合は''とする）
$res_image_mail = '1';

# メールアドレスのリンクに使用する画像（TEXTでもOK）のタグ          ____.23
#（メールアドレスが記入されているとき）
$res_mail_image01 = 'mail*';

# メールアドレスのリンクに使用する画像（TEXTでもOK）のタグ          ____.24
#（メールアドレスが記入されていないとき）
$res_mail_image02 = '<S>mail*</S>';

# ----------------------------------------- URLのリンク方法の設定（子記事）

#URLにリンクをはる（はる場合は'1'、はらない場合は''とする）         ____.25
$res_url_link  = '';

# ----------------------------- 画像にURLのリンクをはる場合の設定（子記事）

# 画像にURLのリンクをはる                                           ____.26
# （はる場合は'1'、はらない場合は''とする）
$res_image_url = '1';

# URLのリンクに使用する画像のタグ                                   ____.27
# （URLが記入されているとき）
$res_url_image01 = 'home*';

# URLのリンクに使用する画像のタグ                                   ____.28
# （URLが記入されていないとき）
$res_url_image02 = '<S>home*</S>';

# 以下の 1; は絶対に消さないこと！！！
1;
