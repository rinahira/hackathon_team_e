function check(){

	var flag = 0;


	// �ݒ�J�n�i�K�{�ɂ��鍀�ڂ�ݒ肵�Ă��������j

	if(document.form1.field1.value == ""){ // �u�����O�v�̓��͂��`�F�b�N

		flag = 1;

	}
	else if(document.form1.field2.value == ""){ // �u�p�X���[�h�v�̓��͂��`�F�b�N

		flag = 1;

	}
	else if(document.form1.field3.value == ""){ // �u�R�����g�v�̓��͂��`�F�b�N

		flag = 1;

	}

	// �ݒ�I��


	if(flag){

		window.alert('�K�{���ڂɖ����͂�����܂���'); // ���͘R�ꂪ����Όx���_�C�A���O��\��
		return false; // ���M�𒆎~

	}
	else{

		return true; // ���M�����s

	}

}