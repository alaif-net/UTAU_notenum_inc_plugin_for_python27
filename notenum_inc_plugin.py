#!/usr/bin/env python
# coding: shift_jis
# author: @alaif_net
# date  : 2015/12/30

import os.path
import re
import shutil
import sys

#一時ファイル名
WORKING_FILE='.working'
#状態
STATE_WAIT_SECTION = 0      #セクション開始待ち
STATE_WAIT_NOTENO_ENTRY = 1 #NoteNumエントリー待ち

#「セクション開始待ち」状態の行処理
def state_wait_section_proc(line, file_output):
	file_output.write(line)
	if re.match('^\[#[0-9]{4}\]', line):
		#音符セクションが始まった
		return STATE_WAIT_NOTENO_ENTRY #「NoteNumエントリー待ち」へ遷移
	else:
		return STATE_WAIT_SECTION      #「セクション開始待ち」のまま

#「NoteNumエントリー待ち」状態の行処理
def state_wait_noteno_entry_proc(line, file_output):
	if re.match('^NoteNum=', line):
		# NoteNumエントリーが見つかった
		fields = line.split('=')
		if fields[1].isdigit:
			#数値だった
			noteno = int(fields[1])
			if noteno < 108:
				#NoteNumの上限に達していなかった
				print 'NoteNum=%d' % noteno
				noteno = noteno + 1
				print 'NoteNum=%d' % noteno
				file_output.write('NoteNum=%d\n' % noteno)
			else:
				#NoteNumの上限に達していた
				print 'NoteNum out of range.'
				file_output.write(line)
		else:
			#数値じゃなかった
			print 'paramert invalid: %s' % fields[1]
			file_output.write(line)
		return STATE_WAIT_SECTION      #「セクション開始待ち」へ遷移
	else:
		file_output.write(line)
		return STATE_WAIT_NOTENO_ENTRY #「NoteNumエントリー待ち」のまま

#状態ごとの行処理関数のリスト
STATE_PROC = {
	STATE_WAIT_SECTION     : state_wait_section_proc,
	STATE_WAIT_NOTENO_ENTRY: state_wait_noteno_entry_proc
}

state = STATE_WAIT_SECTION #最初の状態を「セクション開始待ち」に設定

if __name__ == "__main__":
	#コマンドライン引数を確認
	if len(sys.argv) < 2:
		print 'Usage: %s filename' % sys.argv[0]
		quit()
	
	#ファイルの存在確認
	path_pipe_file = sys.argv[1]
	if os.path.isfile(path_pipe_file) == False:
		print 'Error: Pipe file not found. %s' % path_pipe_file
		quit()
	
	#ファイルオープン
	file_input = open(path_pipe_file, "r")
	file_output = open(WORKING_FILE, "w")
	for line in file_input:
		#読み込んだ行を処理
		state = STATE_PROC[state](line, file_output)
	
	file_output.close()
	file_input.close()
	
	#出力したファイルで入力ファイルを上書き
	shutil.move(WORKING_FILE, path_pipe_file)
