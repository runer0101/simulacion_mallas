/*
    main.js - Scripts interactivos para la simulación de mallas residenciales
    Autor: runer0101
    Este archivo contiene funciones para mejorar la experiencia del usuario.
    Incluye validación de formularios, animaciones y efectos visuales.
*/

// Variables globales
let isCalculating = false;

// Evento que se ejecuta al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('Simulación de mallas cargada correctamente.');
    
    // Inicializar funcionalidades
    initializeFormValidation();
    initializeAnimations();
    initializeTooltips();

    // Lógica para el botón 'Cargar ejemplo' dentro del formulario
    const btnEjemplo = Array.from(document.querySelectorAll('button')).find(btn => btn.textContent.trim() === 'Cargar ejemplo');
    if (btnEjemplo) {
        btnEjemplo.addEventListener('click', function(e) {
            e.preventDefault();
            fetch('/api/example')
                .then(response => response.json())
                .then(data => {
                    for (const key in data) {
                        const input = document.querySelector(`input[name="${key}"]`);
                        if (input) {
                            input.value = data[key];
                            // Disparar eventos para validación visual
                            input.dispatchEvent(new Event('input'));
                            input.dispatchEvent(new Event('blur'));
                        }
                    }
                })
                .catch(err => {
                    showError('No se pudo cargar el ejemplo.');
                });
        });
    }
});

// Validación en tiempo real del formulario
function initializeFormValidation() {
    const inputs = document.querySelectorAll('input[type="number"]');
    
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            validateInput(this);
        });
        
        input.addEventListener('blur', function() {
            validateInput(this);
        });
    });
    
    // Validación del formulario al enviar
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
                showError('Por favor, corrige los errores en el formulario antes de continuar.');
                return false;
            }
            
            showCalculating();
        });
    }
}

// Validar un campo individual
function validateInput(input) {
    const value = parseFloat(input.value);
    const fieldName = input.getAttribute('name');
    
    // Limpiar errores previos
    clearFieldError(input);
    
    // Validaciones
    if (input.value === '') {
        showFieldError(input, 'Este campo es obligatorio');
        return false;
    }
    
    if (isNaN(value)) {
        showFieldError(input, 'Debe ser un número válido');
        return false;
    }
    
    if (value <= 0) {
        showFieldError(input, 'El valor debe ser mayor que cero');
        return false;
    }
    
    // Validaciones específicas por tipo de campo
    if (fieldName.startsWith('R') && (value < 0.1 || value > 1000)) {
        showFieldError(input, 'La resistencia debe estar entre 0.1Ω y 1000Ω');
        return false;
    }
    
    if (fieldName.startsWith('V') && (value < 1 || value > 500)) {
        showFieldError(input, 'El voltaje debe estar entre 1V y 500V');
        return false;
    }
    
    // Si llegamos aquí, el campo es válido
    showFieldSuccess(input);
    return true;
}

// Validar todo el formulario
function validateForm() {
    const inputs = document.querySelectorAll('input[type="number"]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!validateInput(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

// Mostrar error en un campo específico
function showFieldError(input, message) {
    input.classList.add('error');
    input.classList.remove('success');
    
    // Crear o actualizar mensaje de error
    let errorMsg = input.parentNode.querySelector('.field-error');
    if (!errorMsg) {
        errorMsg = document.createElement('div');
        errorMsg.className = 'field-error';
        input.parentNode.appendChild(errorMsg);
    }
    errorMsg.textContent = message;
}

// Mostrar éxito en un campo
function showFieldSuccess(input) {
    input.classList.add('success');
    input.classList.remove('error');
    clearFieldError(input);
}

// Limpiar errores de un campo
function clearFieldError(input) {
    input.classList.remove('error', 'success');
    const errorMsg = input.parentNode.querySelector('.field-error');
    if (errorMsg) {
        errorMsg.remove();
    }
}

// Mostrar mensaje de error general
function showError(message) {
    // Crear o mostrar elemento de error
    let errorDiv = document.querySelector('.general-error');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'general-error error-msg';
        const form = document.querySelector('form');
        form.appendChild(errorDiv);
    }
    
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        if (errorDiv) {
            errorDiv.style.display = 'none';
        }
    }, 5000);
}

// Mostrar estado de cálculo
function showCalculating() {
    const button = document.querySelector('.btn-calcular');
    if (button) {
        isCalculating = true;
        button.disabled = true;
        button.innerHTML = '<span style="animation: spin 1s linear infinite;">⟳</span> Calculando...';
        button.style.opacity = '0.8';
        button.style.cursor = 'not-allowed';
        
        // Agregar indicador visual al formulario
        const form = document.querySelector('.formulario');
        if (form) {
            form.style.opacity = '0.6';
            form.style.pointerEvents = 'none';
        }
    }
}

// Inicializar animaciones
function initializeAnimations() {
    // Animación de electrones en el SVG
    animateElectrons();
    
    // Animación de aparición de resultados
    const resultCards = document.querySelectorAll('.result-card');
    resultCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.2}s`;
        card.classList.add('slide-in');
    });
}

// Animar electrones en el circuito
function animateElectrons() {
    const electrons = document.querySelectorAll('[id^="electron"]');
    
    electrons.forEach((electron, index) => {
        const delay = index * 200; // Diferentes delays para cada electrón
        
        setInterval(() => {
            // Cambiar opacidad para simular movimiento
            electron.style.opacity = '0.3';
            setTimeout(() => {
                electron.style.opacity = '0.8';
            }, 500);
        }, 2000 + delay);
    });
}

// Inicializar tooltips informativos
function initializeTooltips() {
    // Agregar tooltips a elementos con información técnica
    const resistanceInputs = document.querySelectorAll('input[name^="R"]');
    const voltageInputs = document.querySelectorAll('input[name^="V"]');
    
    resistanceInputs.forEach(input => {
        input.title = 'Resistencia en Ohmios (Ω). Representa la oposición al flujo de corriente.';
    });
    
    voltageInputs.forEach(input => {
        input.title = 'Voltaje en Voltios (V). Representa la diferencia de potencial eléctrico.';
    });
}

// Función para resaltar elementos del circuito según los resultados
function highlightCircuitElements() {
    const resultCards = document.querySelectorAll('.result-card');
    
    resultCards.forEach((card, index) => {
        card.addEventListener('mouseenter', function() {
            // Resaltar elementos correspondientes en el SVG
            const mallaClass = `malla${index + 1}`;
            const svgElements = document.querySelectorAll(`[class*="${mallaClass}"]`);
            
            svgElements.forEach(element => {
                element.style.filter = 'brightness(1.3)';
                element.style.transition = 'filter 0.3s ease';
            });
        });
        
        card.addEventListener('mouseleave', function() {
            // Restaurar elementos del SVG
            const mallaClass = `malla${index + 1}`;
            const svgElements = document.querySelectorAll(`[class*="${mallaClass}"]`);
            
            svgElements.forEach(element => {
                element.style.filter = 'brightness(1)';
            });
        });
    });
}

// Función para copiar resultados al portapapeles
function copyResults() {
    const results = document.querySelectorAll('.current-value');
    let resultText = 'Resultados de simulación de mallas:\n\n';
    
    results.forEach((result, index) => {
        resultText += `Malla ${index + 1}: ${result.textContent}\n`;
    });
    
    navigator.clipboard.writeText(resultText).then(() => {
        showNotification('Resultados copiados al portapapeles');
    }).catch(err => {
        console.error('Error al copiar:', err);
    });
}

// Mostrar notificaciones temporales
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #10b981;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 1000;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Mostrar
    setTimeout(() => {
        notification.style.opacity = '1';
    }, 100);
    
    // Ocultar y eliminar
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Función para exportar datos a CSV
function exportToCSV() {
    const vals = {};
    const inputs = document.querySelectorAll('input[type="number"]');
    
    inputs.forEach(input => {
        vals[input.name] = input.value;
    });
    
    const results = document.querySelectorAll('.current-value');
    let csvContent = "Parámetro,Valor\n";
    
    // Agregar resistencias y voltajes
    Object.entries(vals).forEach(([key, value]) => {
        const unit = key.startsWith('R') ? 'Ω' : 'V';
        csvContent += `${key},${value}${unit}\n`;
    });
    
    // Agregar resultados si existen
    if (results.length > 0) {
        csvContent += "\nResultados,Corriente\n";
        results.forEach((result, index) => {
            const current = result.textContent.match(/[\d.-]+/)[0];
            csvContent += `Malla ${index + 1},${current}A\n`;
        });
    }
    
    // Descargar archivo
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', 'simulacion_mallas.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Ejecutar funciones adicionales cuando los resultados estén disponibles
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si hay resultados y activar funciones adicionales
    setTimeout(() => {
        if (document.querySelector('.result-card')) {
            highlightCircuitElements();
        }
    }, 500);
});
