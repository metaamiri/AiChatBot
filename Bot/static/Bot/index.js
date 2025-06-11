document.addEventListener('DOMContentLoaded', () => {

    const homeLink = document.getElementById('homeLink');
    const newChatLink = document.getElementById('newChatLink');
    const defaultContent = document.querySelector('.default-content');
    const chatWrapper = document.querySelector('.chat-wrapper');

    defaultContent.style.display = 'block';
    chatWrapper.style.display = 'none';

    homeLink.addEventListener('click', () => {
        defaultContent.style.display = 'block';
        chatWrapper.style.display = 'none';
    })

    newChatLink.addEventListener('click', () => {
        defaultContent.style.display = 'none';
        chatWrapper.style.display = 'flex';
        newmsg();
    })

});

function newmsg(){
    const sendButton = document.querySelector('send-button');
     if (!sendButton.hasAttribute("listener-added")) {
        sendButton.addEventListener('click', () => {
            const inputField = document.querySelector('.prompt-input');
            const message = inputField.value.trim();
            if (message) {
                // Here you would typically send the message to the server
                console.log('Message sent:', message);
                fetch('/input_msg',{
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                }).then(response => response.json()).then(data => {
                    stream_chat(data);
                })

                inputField.value = ''; // Clear the input field after sending
            } else {
                alert('Input field is empty');
            }
        }
    );
    }
}

function stream_chat(data){
    
}
