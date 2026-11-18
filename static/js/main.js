// Система организации турниров — клиентские скрипты

document.addEventListener('DOMContentLoaded', function() {
    // Подсветка активной ссылки в навигации
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
            link.parentElement.classList.add('fw-bold');
        }
    });

    // Автоскрытие алертов через 5 секунд
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    console.log('Система организации турниров: скрипты загружены');
});