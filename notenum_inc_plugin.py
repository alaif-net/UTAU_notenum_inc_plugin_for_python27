#!/usr/bin/env python
# coding: shift_jis
# author: @alaif_net
# date  : 2015/12/30

import os.path
import re
import shutil
import sys

#�ꎞ�t�@�C����
WORKING_FILE='.working'
#���
STATE_WAIT_SECTION = 0      #�Z�N�V�����J�n�҂�
STATE_WAIT_NOTENO_ENTRY = 1 #NoteNum�G���g���[�҂�

#�u�Z�N�V�����J�n�҂��v��Ԃ̍s����
def state_wait_section_proc(line, file_output):
	file_output.write(line)
	if re.match('^\[#[0-9]{4}\]', line):
		#�����Z�N�V�������n�܂���
		return STATE_WAIT_NOTENO_ENTRY #�uNoteNum�G���g���[�҂��v�֑J��
	else:
		return STATE_WAIT_SECTION      #�u�Z�N�V�����J�n�҂��v�̂܂�

#�uNoteNum�G���g���[�҂��v��Ԃ̍s����
def state_wait_noteno_entry_proc(line, file_output):
	if re.match('^NoteNum=', line):
		# NoteNum�G���g���[����������
		fields = line.split('=')
		if fields[1].isdigit:
			#���l������
			noteno = int(fields[1])
			if noteno < 108:
				#NoteNum�̏���ɒB���Ă��Ȃ�����
				print 'NoteNum=%d' % noteno
				noteno = noteno + 1
				print 'NoteNum=%d' % noteno
				file_output.write('NoteNum=%d\n' % noteno)
			else:
				#NoteNum�̏���ɒB���Ă���
				print 'NoteNum out of range.'
				file_output.write(line)
		else:
			#���l����Ȃ�����
			print 'paramert invalid: %s' % fields[1]
			file_output.write(line)
		return STATE_WAIT_SECTION      #�u�Z�N�V�����J�n�҂��v�֑J��
	else:
		file_output.write(line)
		return STATE_WAIT_NOTENO_ENTRY #�uNoteNum�G���g���[�҂��v�̂܂�

#��Ԃ��Ƃ̍s�����֐��̃��X�g
STATE_PROC = {
	STATE_WAIT_SECTION     : state_wait_section_proc,
	STATE_WAIT_NOTENO_ENTRY: state_wait_noteno_entry_proc
}

state = STATE_WAIT_SECTION #�ŏ��̏�Ԃ��u�Z�N�V�����J�n�҂��v�ɐݒ�

if __name__ == "__main__":
	#�R�}���h���C���������m�F
	if len(sys.argv) < 2:
		print 'Usage: %s filename' % sys.argv[0]
		quit()
	
	#�t�@�C���̑��݊m�F
	path_pipe_file = sys.argv[1]
	if os.path.isfile(path_pipe_file) == False:
		print 'Error: Pipe file not found. %s' % path_pipe_file
		quit()
	
	#�t�@�C���I�[�v��
	file_input = open(path_pipe_file, "r")
	file_output = open(WORKING_FILE, "w")
	for line in file_input:
		#�ǂݍ��񂾍s������
		state = STATE_PROC[state](line, file_output)
	
	file_output.close()
	file_input.close()
	
	#�o�͂����t�@�C���œ��̓t�@�C�����㏑��
	shutil.move(WORKING_FILE, path_pipe_file)
