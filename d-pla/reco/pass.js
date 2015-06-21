function pass() {
 var p = document.fm.word.value;
 if(p == "MENYAKO") {   //この"miyako-deen"がパスワード。この場合は必ずパスワードは大文字で書いてください。
   location.href = "write.html"; //このリンクに飛びます
 }
 else {
  alert("PASSWORDが違います！");
 }
}
