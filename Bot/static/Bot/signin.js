document.addEventListener('DOMContentLoaded', ()=>{
    const loginContainer = document.querySelector('.login-container');
    const registerContainer = document.querySelector('.register-container');
    const loginAnchor = document.getElementById('login-anchor');
    const signUpAnchor = document.getElementById('sign-up-anchor');
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');

    loginContainer.style.display = 'block';
    registerContainer.style.display = 'none';

    signUpAnchor.addEventListener('click', ()=>{
        loginContainer.style.display = 'none';
        registerContainer.style.display = 'block';
    });

    loginAnchor.addEventListener('click', ()=>{
        loginContainer.style.display = 'block';
        registerContainer.style.display = 'none';
    });

    registerForm.addEventListener('submit', (event)=>{
        event.preventDefault(); // prevent default form submit

        const username = document.getElementById('register-username').value.trim();
        const email = document.getElementById('register-email').value.trim();
        const password = document.getElementById('register-password').value;
        const confPassword = document.getElementById('register-confirm-password').value;

        if(password != confPassword){
            alert("passwords don't match.");
            return;
        }

        // Optional: simple validation
        if (!username || !email || !password || !confPassword ) {
            alert('All fields are required.');
            return;
        }

        try {
            fetch('/register/', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),  // include CSRF token if needed
                },
                body: JSON.stringify({ username, email, password })
            }).then(response => response.json() )
            .then(data=>{
                if (data.status === "success"){
                     window.location.href = '/';  // or whatever page you want
                }
                else{
                    alert(data.message);
                }
            })

        } catch (error) {
            console.error('Error:', error);
            alert('Something went wrong!');
        }
    });

    loginForm.addEventListener('submit', (event)=>{
        event.preventDefault(); // prevent default form submit
        const username = document.getElementById('login-username').value.trim();
        const password = document.getElementById('login-password').value;
        
        if (!username || !password) {
            alert('All fields are required.');
            return;
        }

        try {
            fetch('/login/', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),  // include CSRF token if needed
                },
                body: JSON.stringify({ username, password })
                
            }).then(response => response.json() )
            .then(data=>{
                if (data.status === "success"){
                     window.location.href = '/';  // or whatever page you want
                }
                else{
                    alert(data.message);
                }
            })

        } catch (error) {
            console.error('Error:', error);
            alert('Something went wrong!');
        }

    });

})
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
    return '';
  }