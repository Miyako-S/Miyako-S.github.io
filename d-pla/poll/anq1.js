<!-- Petit Poll JavaScript ID1-->
<SCRIPT type="text/javascript">
<!--
function OpenWin1() {
var id = document.pollform1.id.value;
var com = document.pollform1.com.value;

if (com == "") {
document.pollform1.com.value = 'none';
com = document.pollform1.com.value;
} else {
com = document.pollform1.com.value;
}

var poll = 0;

for (var i=0; i < document.pollform1.poll.length; i++) {
if (document.pollform1.poll[i].checked) {
poll = document.pollform1.poll[i].value;
}
}

if (poll == 0) {
alert ("項目がチェックされていません！");
} else {
window.open ('http://www.d-planets.org/poll/poll.cgi?mode=on&id='+id+'&poll='+poll+'&com='+com, 'newwin', 'menubar=no, scrollbars=yes, width=330, height=302');
}
}

function ResultWin (Id) {
window.open('http://www.d-planets.org/poll/poll.cgi?mode=result&id='+Id,'newwin','menubar=no, scrollbars=yes, width=330, height=302');
}
//-->
</SCRIPT>
<!-- Petit Poll JavaScript ID1 END -->
