// app/static/js/auth.js
document.addEventListener('DOMContentLoaded', function() {
    // Event listener para formulário de login
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const remember = document.getElementById('remember').checked;
            
            login(email, password, remember);
        });
    }
    
    // Event listener para formulário de registro
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            
            if (password !== confirmPassword) {
                alert('As senhas não coincidem. Por favor, verifique.');
                return;
            }
            
            register(username, email, password);
        });
    }
    
    // Event listener para logout
    const logoutLink = document.querySelector('a[href="/auth/logout"]');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
});

// Função de login
function login(email, password, remember = false) {
    // Usando fetch API em vez de axios
    fetch('/api/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, remember })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Armazenar token
            localStorage.setItem('auth_token', data.access_token);
            
            // Redirecionar para o dashboard
            window.location.href = '/dashboard';
        } else {
            alert('Credenciais inválidas. Por favor, tente novamente.');
        }
    })
    .catch(error => {
        console.error('Erro ao fazer login:', error);
        alert('Erro ao fazer login. Por favor, tente novamente.');
    });
}

// Função de registro
function register(username, email, password) {
    // Usando fetch API em vez de axios
    fetch('/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Armazenar token
            localStorage.setItem('auth_token', data.access_token);
            
            // Redirecionar para o dashboard
            window.location.href = '/dashboard';
        } else {
            alert('Erro ao registrar. Por favor, tente novamente.');
        }
    })
    .catch(error => {
        console.error('Erro ao registrar:', error);
        alert('Erro ao registrar. Por favor, tente novamente.');
    });
}

// Função de logout
function logout() {
    // Remover token
    localStorage.removeItem('auth_token');
    
    // Redirecionar para a página de login
    window.location.href = '/auth/login';
}