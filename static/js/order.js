function check(){

	var flag = 0;


	// 設定開始（必須にする項目を設定してください）

	if(document.form1.last_name.value == ""){ // 「お名前」の入力をチェック

		flag = 1;

	}
	else if(document.form1.first_name.value == ""){ // 「パスワード」の入力をチェック

		flag = 1;

	}
	else if(document.form1.postal_code.value == ""){ // 「コメント」の入力をチェック

		flag = 1;

	}

	// 設定終了


	if(flag){

		window.alert('必須項目に未入力がありました'); // 入力漏れがあれば警告ダイアログを表示
		return false; // 送信を中止

	}
	else{

		return true; // 送信を実行

	}

}