document.addEventListener('DOMContentLoaded', () => {
  const startBtn = document.getElementById('startBtn');
  const sendBtn = document.getElementById('sendBtn');
  const clearBtn = document.getElementById('clearBtn');
  const input = document.getElementById('input');
  const chat = document.getElementById('chat');

  function renderMessages(messages) {
    chat.innerHTML = '';
    if (!messages || messages.length === 0) {
      chat.innerHTML = '<div class="notice">Nenhuma mensagem. Clique em "Iniciar Campanha" para começar.</div>';
      return;
    }
    messages.forEach(m => {
      const d = document.createElement('div');
      d.className = 'msg ' + (m.role === 'user' ? 'user' : 'assistant');
      d.innerHTML = '<div class="text">' + escapeHtml(m.text).replace(/\n/g, '<br>') + '</div>';
      chat.appendChild(d);
    });
    chat.scrollTop = chat.scrollHeight;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }

  startBtn.addEventListener('click', async () => {
    startBtn.disabled = true;
    const res = await fetch('start.php', { method: 'POST' });
    const data = await res.json();
    renderMessages(data.messages);
    startBtn.disabled = false;
  });

  sendBtn.addEventListener('click', async () => {
    const text = input.value.trim();
    if (!text) return;
    // UI otimista
    const userDiv = document.createElement('div');
    userDiv.className = 'msg user';
    userDiv.textContent = text;
    chat.appendChild(userDiv);
    input.value = '';
    chat.scrollTop = chat.scrollHeight;

    const res = await fetch('send.php', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    renderMessages(data.messages);
  });

  clearBtn.addEventListener('click', () => {
    window.location.href = 'clear.php';
  });
});