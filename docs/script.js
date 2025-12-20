/**
 * 掲示板形式にテキストをフォーマットする
 */
function formatBulletinBoard(text, startNumber, anonymousName, jumpMin, jumpMax) {
  const lines = text.trim().split('\n');
  const result = [];
  let commentNumber = startNumber;

  // タイトル行を探す
  let titleLine = null;
  let contentStart = 0;

  for (let i = 0; i < lines.length; i++) {
    if (lines[i].startsWith('## ')) {
      titleLine = lines[i];
      contentStart = i + 1;
      break;
    }
  }

  if (titleLine) {
    result.push(titleLine);
  }

  // コメントを処理
  let currentComment = [];
  let pendingJump = false;

  for (let i = contentStart; i < lines.length; i++) {
    const line = lines[i];
    const stripped = line.trim();

    // 「＊」マーカーをチェック
    if (stripped.includes('＊')) {
      // 現在のコメントを確定（もしあれば）
      if (currentComment.length > 0) {
        result.push(`${commentNumber}. ${anonymousName}`);
        result.push(...currentComment);
        result.push('');
        commentNumber += 1;
        currentComment = [];
      }
      // 「＊」行をそのまま出力
      result.push(line);
      result.push('');
      // 次のコメントの番号をジャンプさせるフラグを立てる
      pendingJump = true;
      continue;
    }

    if (stripped === '') {
      // 空行の場合、現在のコメントを確定
      if (currentComment.length > 0) {
        // ジャンプが必要な場合、番号を増加
        if (pendingJump) {
          const jump = Math.floor(Math.random() * (jumpMax - jumpMin + 1)) + jumpMin;
          commentNumber = (commentNumber - 1) + jump;
          pendingJump = false;
        }
        result.push(`${commentNumber}. ${anonymousName}`);
        result.push(...currentComment);
        result.push('');
        commentNumber += 1;
        currentComment = [];
      }
    } else {
      // コメント内容を追加
      currentComment.push(line);
    }
  }

  // 最後のコメントを処理
  if (currentComment.length > 0) {
    // ジャンプが必要な場合、番号を増加
    if (pendingJump) {
      const jump = Math.floor(Math.random() * (jumpMax - jumpMin + 1)) + jumpMin;
      commentNumber = (commentNumber - 1) + jump;
    }
    result.push(`${commentNumber}. ${anonymousName}`);
    result.push(...currentComment);
  }

  return result.join('\n');
}

/**
 * テキストを変換
 */
function formatText() {
  const inputText = document.getElementById('inputText').value;
  const startNumber = parseInt(document.getElementById('startNumber').value) || 1;
  const anonymousName = document.getElementById('anonymousName').value || '名無し';
  const jumpMin = parseInt(document.getElementById('jumpMin').value) || 50;
  const jumpMax = parseInt(document.getElementById('jumpMax').value) || 250;

  if (!inputText.trim()) {
    showToast('テキストを入力してください', 'error');
    return;
  }

  const result = formatBulletinBoard(inputText, startNumber, anonymousName, jumpMin, jumpMax);
  document.getElementById('outputText').value = result;
  showToast('変換完了！', 'success');
}

/**
 * 入力をクリア
 */
function clearInput() {
  document.getElementById('inputText').value = '';
  document.getElementById('outputText').value = '';
}

/**
 * 出力をクリップボードにコピー
 */
async function copyOutput() {
  const outputText = document.getElementById('outputText').value;

  if (!outputText.trim()) {
    showToast('コピーするテキストがありません', 'error');
    return;
  }

  try {
    await navigator.clipboard.writeText(outputText);
    showToast('コピーしました！', 'success');
  } catch (err) {
    // フォールバック
    const textarea = document.getElementById('outputText');
    textarea.select();
    document.execCommand('copy');
    showToast('コピーしました！', 'success');
  }
}

/**
 * 出力をダウンロード
 */
function downloadOutput() {
  const outputText = document.getElementById('outputText').value;

  if (!outputText.trim()) {
    showToast('ダウンロードするテキストがありません', 'error');
    return;
  }

  const blob = new Blob([outputText], { type: 'text/plain; charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'formatted_bulletin_board.txt';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast('ダウンロード開始！', 'success');
}

/**
 * トースト通知を表示
 */
function showToast(message, type = 'success') {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.style.background = type === 'success' ? 'var(--success)' : '#ef4444';
  toast.classList.add('show');

  setTimeout(() => {
    toast.classList.remove('show');
  }, 2000);
}

// キーボードショートカット
document.addEventListener('keydown', (e) => {
  // Ctrl/Cmd + Enter で変換
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault();
    formatText();
  }
});
