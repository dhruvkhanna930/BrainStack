
  const messagesList = document.querySelector('.chat-bg');
  const messageForm = document.querySelector('.message-form');
  const messageInput = document.querySelector('.message-input');
  const waitingDots = document.querySelector('.messages__item--typing');

  waitingDots.style.display = 'none';

  messageForm.addEventListener('submit', (event) => {
    event.preventDefault();
    

    const message = messageInput.value.trim();
    if (message.length === 0) {
      return;
    }

    var dotItem = document.createElement('div');
    dotItem.classList.add('messages__item', 'messages__item--typing')
    dotItem.innerHTML = `
        <span class="messages__dot"></span>
        <span class="messages__dot"></span>
        <span class="messages__dot"></span>`;
        
        

    const messageItem = document.createElement('li');
    messageItem.classList.add('messages__item', 'messages__item--operator');
    messageItem.innerHTML = `
        <div class="message-text">
            <div class="message-sender">
                <b>You</b>
            </div>
            <div class="message-content">
                ${message}
            </div>
        </div>`;
    messagesList.appendChild(messageItem);

    messageInput.value = '';

    messagesList.appendChild(dotItem);

    fetch('', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'message': message
      })
    })

      .then(response => response.json())
      .then(data => {
        const response = data.response;
        const messageItem = document.createElement('li');
        messageItem.classList.add('messages__item', 'messages__item--visitor');
        messageItem.innerHTML = `
        <div class="message-text">
            <div class="message-sender">
              <b>AI Chatbot</b>
            </div>
            <div class="message-content">
                ${response}
            </div>
        </div>
          `;
        dotItem.remove();
        messagesList.appendChild(messageItem);
      });
  });
