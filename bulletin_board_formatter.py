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

特殊機能:
    「＊」を含む行があると、その後の番号は直前の値から50〜250を
    ランダムに足した値にジャンプする
"""

import sys
import re
import random

# =============================================================================
# 設定パラメータ
# =============================================================================
DEFAULT_ANONYMOUS_NAME = "名無し"  # デフォルトの匿名名
DEFAULT_JUMP_MIN = 50              # 「＊」後のジャンプ最小値
DEFAULT_JUMP_MAX = 250             # 「＊」後のジャンプ最大値


def format_bulletin_board(
    text: str,
    start_number: int = 1,
    anonymous_name: str = None,
    jump_min: int = None,
    jump_max: int = None
) -> str:
    """
    掲示板形式にテキストをフォーマットする
    
    Args:
        text: 入力テキスト
        start_number: 開始番号（デフォルト: 1）
        anonymous_name: 匿名名（デフォルト: DEFAULT_ANONYMOUS_NAME）
        jump_min: 「＊」後のジャンプ最小値（デフォルト: DEFAULT_JUMP_MIN）
        jump_max: 「＊」後のジャンプ最大値（デフォルト: DEFAULT_JUMP_MAX）
    
    Returns:
        フォーマットされたテキスト
    """
    # デフォルト値を適用
    if anonymous_name is None:
        anonymous_name = DEFAULT_ANONYMOUS_NAME
    if jump_min is None:
        jump_min = DEFAULT_JUMP_MIN
    if jump_max is None:
        jump_max = DEFAULT_JUMP_MAX
    
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
    pending_jump = False  # 「＊」の後にジャンプするかどうか
    
    for line in lines[content_start:]:
        stripped = line.strip()
        
        # 「＊」マーカーをチェック
        if '＊' in stripped:
            # 現在のコメントを確定（もしあれば）
            if current_comment:
                result.append(f"{comment_number}. {anonymous_name}")
                result.extend(current_comment)
                result.append('')
                comment_number += 1
                current_comment = []
            # 「＊」行をそのまま出力
            result.append('')
            result.append(line)
            result.append('')
            # 次のコメントの番号をジャンプさせるフラグを立てる
            pending_jump = True
            continue
        
        if stripped == '':
            # 空行の場合、現在のコメントを確定
            if current_comment:
                # ジャンプが必要な場合、番号を増加
                if pending_jump:
                    jump = random.randint(jump_min, jump_max)
                    comment_number = (comment_number - 1) + jump
                    pending_jump = False
                result.append(f"{comment_number}. {anonymous_name}")
                result.extend(current_comment)
                result.append('')
                comment_number += 1
                current_comment = []
        else:
            # コメント内容を追加
            current_comment.append(line)
    
    # 最後のコメントを処理
    if current_comment:
        # ジャンプが必要な場合、番号を増加
        if pending_jump:
            jump = random.randint(jump_min, jump_max)
            comment_number = (comment_number - 1) + jump
            pending_jump = False
        result.append(f"{comment_number}. {anonymous_name}")
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
