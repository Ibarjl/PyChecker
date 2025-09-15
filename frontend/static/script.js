
// JavaScript mejorado para el dashboard
console.log('🚀 Health Monitor Dashboard cargado');

// Variables globales
let autoRefreshInterval;
let isAutoRefreshEnabled = true;

// Función para actualizar datos vía AJAX
async function refreshData() {
    console.log('🔄 Actualizando datos...');

    try {
        const response = await fetch('/api/status');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const statusData = await response.json();
        updateStatusTable(statusData);

        // Actualizar timestamp
        const now = new Date().toLocaleString('es-ES');
        document.querySelector('footer p').innerHTML =
            `🔧 Health Monitor v1.0 | 🕒 Última actualización: ${now}`;

        console.log('✅ Datos actualizados exitosamente');

    } catch (error) {
        console.error('❌ Error actualizando datos:', error);
        showNotification('Error actualizando datos: ' + error.message, 'error');
    }
}

// Función para actualizar la tabla de estado
function updateStatusTable(statusData) {
    const tbody = document.querySelector('.status-table tbody');
    if (!tbody) {
        console.warn('⚠️ No se encontró tabla de estado');
        return;
    }

    // Limpiar contenido actual
    tbody.innerHTML = '';

    // Agregar nuevas filas
    statusData.forEach(service => {
        const row = createStatusRow(service);
        tbody.appendChild(row);
    });
}

// Función para crear una fila de estado
function createStatusRow(service) {
    const row = document.createElement('tr');
    row.className = 'service-row';
    row.setAttribute('data-status', service.status);

    // Determinar emoji según estado
    let statusEmoji = '⏳';
    let statusClass = 'waiting';

    switch (service.status) {
        case 'OK':
            statusEmoji = '✅';
            statusClass = 'ok';
            break;
        case 'WARNING':
            statusEmoji = '⚠️';
            statusClass = 'warning';
            break;
        case 'ERROR':
            statusEmoji = '❌';
            statusClass = 'error';
            break;
        case 'CRITICAL':
            statusEmoji = '🚨';
            statusClass = 'critical';
            break;
    }

    row.innerHTML = `
        <td class="service-name">${service.name}</td>
        <td class="service-status">
            <span class="status-badge status-${statusClass}">
                ${statusEmoji} ${service.status}
            </span>
        </td>
        <td class="service-error">${service.last_error || '—'}</td>
        <td class="service-restarts">${service.restarts_last_hour}</td>
        <td class="service-checked">${service.last_checked}</td>
    `;

    return row;
}

// Función para mostrar información del sistema
async function viewSystemInfo() {
    try {
        const response = await fetch('/api/system');
        const systemInfo = await response.json();

        const info = `
            📊 Información del Sistema:
            
            🔧 Versión: ${systemInfo.monitor_version}
            📁 Archivo de estado: ${systemInfo.estado_file_exists ? '✅ Existe' : '❌ No existe'}
            🕒 Última actualización: ${systemInfo.last_update ? new Date(systemInfo.last_update * 1000).toLocaleString('es-ES') : 'Nunca'}
        `;

        alert(info);

    } catch (error) {
        console.error('❌ Error obteniendo info del sistema:', error);
        alert('Error obteniendo información del sistema');
    }
}

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    // Estilos básicos
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 10px 20px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
        z-index: 1000;
        background-color: ${type === 'error' ? '#f44336' : '#4CAF50'};
    `;

    // Agregar al DOM
    document.body.appendChild(notification);

    // Eliminar después de 3 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// Función para toggle del auto-refresh
function toggleAutoRefresh() {
    if (isAutoRefreshEnabled) {
        clearInterval(autoRefreshInterval);
        isAutoRefreshEnabled = false;
        console.log('⏸️ Auto-refresh deshabilitado');
        showNotification('Auto-refresh deshabilitado', 'info');
    } else {
        startAutoRefresh();
        console.log('▶️ Auto-refresh habilitado');
        showNotification('Auto-refresh habilitado', 'info');
    }
}

// Función para iniciar auto-refresh
function startAutoRefresh() {
    autoRefreshInterval = setInterval(refreshData, 30000); // 30 segundos
    isAutoRefreshEnabled = true;
}

// Event listeners cuando se carga la página
document.addEventListener('DOMContentLoaded', function () {
    console.log('📱 DOM cargado completamente');

    // Iniciar auto-refresh
    startAutoRefresh();

    // Agregar event listeners adicionales
    document.addEventListener('keydown', function (event) {
        // Ctrl + R para refresh manual
        if (event.ctrlKey && event.key === 'r') {
            event.preventDefault();
            refreshData();
        }

        // Ctrl + P para toggle auto-refresh
        if (event.ctrlKey && event.key === 'p') {
            event.preventDefault();
            toggleAutoRefresh();
        }
    });

    console.log('🎮 Atajos de teclado configurados:');
    console.log('   Ctrl + R: Actualizar datos manualmente');
    console.log('   Ctrl + P: Toggle auto-refresh');
});

// Limpiar interval cuando se cierra la página
window.addEventListener('beforeunload', function () {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
});
=======
// Opcional: refrescar la página cada 30 segundos
setInterval(() => {
    window.location.reload();
}, 30000);

