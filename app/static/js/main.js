// app/static/js/main.js

// Função para formatar datas
function formatDate(dateString, withYear = true) {
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    
    return withYear
        ? `${day}/${month}/${year} ${hours}:${minutes}`
        : `${hours}:${minutes}`;
}

// Verificar se o usuário está autenticado (tem token)
function isAuthenticated() {
    return localStorage.getItem('auth_token') !== null;
}

// Adicionar token de autenticação às requisições
document.addEventListener('DOMContentLoaded', function() {
    // Configurar interceptor para Axios (se estiver usando)
    if (typeof axios !== 'undefined') {
        axios.interceptors.request.use(
            config => {
                const token = localStorage.getItem('auth_token');
                if (token) {
                    config.headers['Authorization'] = `Bearer ${token}`;
                }
                return config;
            },
            error => {
                return Promise.reject(error);
            }
        );
        
        // Interceptor para tratar erros de autenticação
        axios.interceptors.response.use(
            response => {
                return response;
            },
            error => {
                if (error.response && error.response.status === 401) {
                    // Redirecionar para login se token expirou
                    localStorage.removeItem('auth_token');
                    window.location.href = '/auth/login';
                }
                return Promise.reject(error);
            }
        );
    }
    
    // Verificar notificações não lidas (se usuário estiver autenticado)
    if (isAuthenticated()) {
        checkNotifications();
    }
});

// Verificar notificações
function checkNotifications() {
    // Use fetch em vez de axios para garantir compatibilidade
    fetch('/api/notifications/unread-count')
        .then(response => response.json())
        .then(data => {
            if (data.count > 0) {
                // Atualizar badge
                const badge = document.querySelector('.notification-badge');
                badge.textContent = data.count;
                badge.classList.remove('d-none');
            }
        })
        .catch(error => {
            console.error('Erro ao verificar notificações:', error);
        });
}