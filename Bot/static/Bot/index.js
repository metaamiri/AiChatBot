
document.addEventListener('DOMContentLoaded', () => {

    const homeLink = document.getElementById('homeLink');
    const newChatLink = document.getElementById('newChatLink');
    const defaultContent = document.querySelector('.default-content');
    const chatWrapper = document.querySelector('.chat-wrapper');
    const streamWrapper = document.querySelector(".stream-wrapper");

    defaultContent.style.display = 'block';
    chatWrapper.style.display = 'none';
    streamWrapper.style.display = 'none';

    

    homeLink.addEventListener('click', () => {
        defaultContent.style.display = 'block';
        chatWrapper.style.display = 'none';
        streamWrapper.style.display = 'none';
        // history.pushState(null, '', '/');
    })

    newChatLink.addEventListener('click', () => {
        defaultContent.style.display = 'none';
        streamWrapper.style.display = 'none';
        chatWrapper.style.display = 'flex';
        // history.pushState(null, '', '/chat/1');
        newmsg();
    })
});

function newmsg() {
  const sendButton = document.querySelector('.send-button');
  const textarea = document.querySelector('.prompt-input');

  textarea.addEventListener('keydown', function(event){
    if (event.key === 'Enter') {
      if (event.shiftKey) {
        // Let Shift+Enter insert a newline (default behavior)
        return;
      }

      // Prevent newline on normal Enter
      event.preventDefault();

      // Only send if input is not empty
      if (textarea.value.trim() !== '') {
        sendButton.click();
      }
    }
  });

  sendButton.disabled = true;
  textarea.addEventListener('input', () => {
    sendButton.disabled = textarea.value.trim() === '';

    // Prevent adding multiple listeners if already added
    if (!sendButton.hasAttribute('listener-added')) {
      sendButton.setAttribute('listener-added', 'true');

      sendButton.addEventListener("click", () => {
        const message = document.querySelector('.prompt-input').value;
        document.querySelector('.prompt-input').value = '';
        stream_chat(message);
        addmsg();
      });
    }
  });


}


function stream_chat(data){
    
    const streamWrapper = document.querySelector(".stream-wrapper");
    const streamChat = document.querySelector(".stream-chat");
    const chatWrapper = document.querySelector('.chat-wrapper');

    chatWrapper.style.display = 'none';
    streamWrapper.style.display = 'flex';


    const userInput = document.createElement('div');
    userInput.className = 'user-message message';
    userInput.style.border = '1px solid rgb(230, 230, 230)';
    userInput.style.borderRadius = '15px';  
    userInput.style.backgroundColor = 'rgb(230, 230, 230)';
    userInput.style.padding = '12px';
    userInput.style.margin = '20px';
    userInput.style.width = '300px';
    userInput.style.display = 'inline-block';
    userInput.style.alignSelf = 'flex-end';

    const userParag = document.createElement('p');
    userParag.textContent = data;

    userInput.appendChild(userParag);
    streamChat.appendChild(userInput);
    streamChat.scrollTop = streamChat.scrollHeight; // scroll to bottom

    const botDiv = document.createElement('div');
    botDiv.textContent = 'Thinking...';
    botDiv.className = 'bot-message message';
    botDiv.style.border = '1px solid rgb(230, 230, 230)';
    botDiv.style.borderRadius = '15px';  
    botDiv.style.backgroundColor = 'rgb(230, 230, 230)';
    botDiv.style.padding = '12px';
    botDiv.style.margin = '20px';
    botDiv.style.width = '90%';
    botDiv.style.display = 'inline-block';
    botDiv.style.alignSelf = 'flex-start';
    streamChat.appendChild(botDiv);

    var converter = new showdown.Converter()

    fetch(`/input_msg/?message=${encodeURIComponent(data)}`)
    .then(response => {return response.json()})
    .then(data =>{
      html = converter.makeHtml(data.message);
      botDiv.innerHTML = html;
      botDiv.style.direction = data.dir;
      console.log(data.dir);
      console.log(data.message)
      if (data.status === "success"){
        streamChat.scrollTo({
          top: streamChat.scrollHeight,
          behavior: 'smooth'
        });
      }
      hljs.highlightAll();
    });
  
}
    


function addmsg() {
  const sendButton = document.querySelector('.send-button-addmsg');
  const textarea = document.querySelector('.prompt-input-addmsg');
  const streamChat = document.querySelector(".stream-chat");

  textarea.addEventListener('keydown', function(event){
    if (event.key === 'Enter') {
      if (event.shiftKey) {
        // Let Shift+Enter insert a newline (default behavior)
        return;
      }

      // Prevent newline on normal Enter
      event.preventDefault();

      // Only send if input is not empty
      if (textarea.value.trim() !== '') {
        sendButton.click();
      }
    }
  });


  textarea.addEventListener('input', () => {
    sendButton.disabled = textarea.value.trim() === '';
  });
 

  // Prevent adding multiple listeners if already added
  if (!sendButton.hasAttribute('listener-added')) {
    sendButton.setAttribute('listener-added', 'true');

    sendButton.addEventListener("click", () => {
      const message = document.querySelector('.prompt-input-addmsg').value;
      document.querySelector('.prompt-input-addmsg').value = '';
      sendButton.disabled = true;
      stream_chat(message);
      streamChat.scrollTo({
          top: streamChat.scrollHeight,
          behavior: 'smooth'
      });
    });
  }
}
