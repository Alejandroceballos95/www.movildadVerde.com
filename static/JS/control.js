document.getElementById("compararFormulario").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevenir que el formulario se envíe

    // Recoger datos del formulario
    const nombre = document.getElementById("nombre").value;
    const vehiculo1 = document.getElementById("vehiculo1").value;
    const vehiculo2 = document.getElementById("vehiculo2").value;
    const kilometraje = parseFloat(document.getElementById("kilometraje").value);
    const gastoCombustible = parseFloat(document.getElementById("gastoCombustible").value);

    // Costos promedio por km (en pesos colombianos)
    const costos = {
        "Electrico": 126, // COP/km
        "Hibrido": 270,   // COP/km
        "Combustion": 450, // COP/km
        "E-fuel": 500    // COP/km
    };

    // Cálculo de los costos mensuales
    const costo1 = kilometraje * costos[vehiculo1] * 30; // Costo mensual del vehículo 1
    const costo2 = kilometraje * costos[vehiculo2] * 30; // Costo mensual del vehículo 2

    // Diferencia de costos
    const diferencia = costo2 - costo1;

    // Mostrar resultados
    resultado=alert(
        `Resultado Comparativo
        ${nombre} estos son tus resultados
        Si pasas de ${vehiculo1} a ${vehiculo2} Gastaras mensualmente  $${Math.abs(diferencia + gastoCombustible)}`);
});
