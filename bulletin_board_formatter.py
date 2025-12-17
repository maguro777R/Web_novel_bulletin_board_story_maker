#!/usr/bin/env python3
"""
Web小説の掲示板回用フォーマッタースクリプト

入力形式:
    ## タイトル
    コメント

    コメント

    コメント

出力形式:
    ## タイトル
    n. 名無し
    コメント

    n+1. 名無し
    コメント

    n+2. 名無し
    コメント
"""

import sys
import re


def format_bulletin_board(text: str, start_number: int = 1) -> str:
    """
    掲示板形式にテキストをフォーマットする
    
    Args:
        text: 入力テキスト
        start_number: 開始番号（デフォルト: 1）
    
    Returns:
        フォーマットされたテキスト
    """
    lines = text.strip().split('\n')
    result = []
    comment_number = start_number
    
    # タイトル行を探す
    title_line = None
    content_start = 0
    
    for i, line in enumerate(lines):
        if line.startswith('## '):
            title_line = line
            content_start = i + 1
            break
    
    if title_line:
        result.append(title_line)
    
    # コメントを処理
    current_comment = []
    
    for line in lines[content_start:]:
        stripped = line.strip()
        
        if stripped == '':
            # 空行の場合、現在のコメントを確定
            if current_comment:
                result.append(f"{comment_number}. 名無し")
                result.extend(current_comment)
                result.append('')
                comment_number += 1
                current_comment = []
        else:
            # コメント内容を追加
            current_comment.append(line)
    
    # 最後のコメントを処理
    if current_comment:
        result.append(f"{comment_number}. 名無し")
        result.extend(current_comment)
    
    return '\n'.join(result)


def main():
    """メイン関数"""
    print("テキストを入力してください（Ctrl+D または Ctrl+Z で終了）:")
    print("開始番号を指定する場合は、最初の行に数字を入力してください。")
    print("-" * 50)
    
    try:
        input_text = sys.stdin.read()
    except KeyboardInterrupt:
        print("\n中断されました。")
        return
    
    if not input_text.strip():
        print("入力がありません。")
        return
    
    # 開始番号をチェック
    lines = input_text.strip().split('\n')
    start_number = 1
    
    # 最初の行が数字のみの場合、開始番号として扱う
    first_line = lines[0].strip()
    if first_line.isdigit():
        start_number = int(first_line)
        input_text = '\n'.join(lines[1:])
    
    result = format_bulletin_board(input_text, start_number)
    
    print("\n" + "=" * 50)
    print("出力結果:")
    print("=" * 50)
    print(result)


if __name__ == "__main__":
    main()
