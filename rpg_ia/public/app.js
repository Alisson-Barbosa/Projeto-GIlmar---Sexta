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
    return String(s).replace(/[&<>"']/g, c => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    }[c]));
  }

  startBtn.addEventListener('click', async () => {
    startBtn.disabled = true;
    try {
      const res = await fetch('start.php', { method: 'POST' });
      const data = await res.json();
      renderMessages(data.messages);
    } catch (err) {
      alert('Erro ao iniciar: ' + err.message);
    } finally {
      startBtn.disabled = false;
    }
  });

  sendBtn.addEventListener('click', async () => {
    const text = input.value.trim();
    if (!text) return;
    sendBtn.disabled = true;

    // Mostra a mensagem do usuário
    const userDiv = document.createElement('div');
    userDiv.className = 'msg user';
    userDiv.innerHTML = '<div class="text">' + escapeHtml(text) + '</div>';
    chat.appendChild(userDiv);
    input.value = '';
    chat.scrollTop = chat.scrollHeight;

    try {
      const res = await fetch('send.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });

      const raw = await res.text();

      if (!raw.trim()) {
        throw new Error("O PHP não retornou nada. Verifique se há erro em send.php no servidor.");
      }

      let data;
      try {
        data = JSON.parse(raw);
      } catch (e) {
        throw new Error("Resposta inválida do PHP: " + raw);
      }

      if (!data.success) {
        alert("Erro: " + (data.error || "Falha desconhecida"));
        return;
      }

      renderMessages(data.messages);
    } catch (err) {
      alert("Erro ao enviar mensagem: " + err.message);
    } finally {
      sendBtn.disabled = false;
    }
  });

  clearBtn.addEventListener('click', () => {
    if (confirm('Tem certeza que deseja limpar a conversa?')) {
      window.location.href = 'clear.php';
    }
  });
});
