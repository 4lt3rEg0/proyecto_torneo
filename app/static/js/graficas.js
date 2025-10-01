// Sistema de Gráficas para el Torneo
class GestorGraficas {
    constructor() {
        this.graficas = new Map();
    }

    // Inicializar todas las gráficas de la página
    inicializar() {
        this.inicializarProgresoUsuario();
        this.inicializarEstadisticasGlobales();
        this.inicializarRankingTiempoReal();
    }

    // Gráfica de progreso del usuario
    inicializarProgresoUsuario() {
        const ctx = document.getElementById('progresoChart');
        if (!ctx) return;

        // Simular datos de progreso (en producción, obtener de la API)
        const datosProgreso = {
            labels: ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4', 'Semana 5'],
            datasets: [{
                label: 'Mi Puntuación',
                data: [450, 620, 580, 750, 820],
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Promedio General',
                data: [400, 550, 600, 650, 700],
                borderColor: '#6c757d',
                borderDash: [5, 5],
                tension: 0.4,
                fill: false
            }]
        };

        this.crearGrafica(ctx, 'line', datosProgreso, {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1000,
                    title: {
                        display: true,
                        text: 'Puntuación'
                    }
                }
            }
        });
    }

    // Gráfica de estadísticas globales
    inicializarEstadisticasGlobales() {
        const ctx = document.getElementById('estadisticasChart');
        if (!ctx) return;

        const datos = {
            labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
            datasets: [{
                label: 'Nuevos Usuarios',
                data: [5, 8, 12, 6, 15, 10, 7],
                backgroundColor: 'rgba(40, 167, 69, 0.8)'
            }, {
                label: 'Partidas Jugadas',
                data: [20, 25, 30, 22, 35, 40, 28],
                backgroundColor: 'rgba(0, 123, 255, 0.8)'
            }, {
                label: 'Inscripciones',
                data: [15, 18, 22, 16, 25, 30, 20],
                backgroundColor: 'rgba(255, 193, 7, 0.8)'
            }]
        };

        this.crearGrafica(ctx, 'bar', datos, {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        });
    }

    // Gráfica de ranking en tiempo real
    inicializarRankingTiempoReal() {
        const ctx = document.getElementById('rankingChart');
        if (!ctx) return;

        // Simular datos de ranking
        const jugadores = ['Jugador A', 'Jugador B', 'Jugador C', 'Jugador D', 'Jugador E'];
        const puntuaciones = [950, 870, 790, 720, 680];

        const datos = {
            labels: jugadores,
            datasets: [{
                label: 'Puntuación',
                data: puntuaciones,
                backgroundColor: [
                    'rgba(255, 215, 0, 0.8)',
                    'rgba(192, 192, 192, 0.8)',
                    'rgba(205, 127, 50, 0.8)',
                    'rgba(0, 123, 255, 0.8)',
                    'rgba(108, 117, 125, 0.8)'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        };

        this.crearGrafica(ctx, 'bar', datos, {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            }
        });
    }

    // Función genérica para crear gráficas
    crearGrafica(ctx, tipo, datos, opciones) {
        const config = {
            type: tipo,
            data: datos,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                ...opciones
            }
        };

        const grafica = new Chart(ctx, config);
        this.graficas.set(ctx.id, grafica);
        return grafica;
    }

    // Actualizar gráfica con nuevos datos
    actualizarGrafica(idGrafica, nuevosDatos) {
        const grafica = this.graficas.get(idGrafica);
        if (grafica) {
            grafica.data = nuevosDatos;
            grafica.update();
        }
    }

    // Cargar datos reales desde la API
    async cargarDatosReales(juegoId) {
        try {
            const response = await fetch(`/api/ranking/${juegoId}`);
            const datos = await response.json();
            return datos;
        } catch (error) {
            console.error('Error cargando datos:', error);
            return null;
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    const gestor = new GestorGraficas();
    gestor.inicializar();

    // Exponer el gestor globalmente para debugging
    window.gestorGraficas = gestor;
});