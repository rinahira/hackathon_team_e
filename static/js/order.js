function check(){

	var flag = 0;


	// �ݒ�J�n�i�K�{�ɂ��鍀�ڂ�ݒ肵�Ă��������j

	if(document.form1.last_name.value == ""){ // �u�����O�v�̓��͂��`�F�b�N

		flag = 1;

	}
	else if(document.form1.first_name.value == ""){ // �u�p�X���[�h�v�̓��͂��`�F�b�N

		flag = 1;

	}
	else if(document.form1.postal_code.value == ""){ // �u�R�����g�v�̓��͂��`�F�b�N

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