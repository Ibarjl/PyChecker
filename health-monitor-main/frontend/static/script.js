async function fetchHealth() {
    try {
        const res = await axios.get("/api/health");
        const services = res.data;
        const container = document.getElementById("services-container");
        container.innerHTML = "";

        if (!services || Object.keys(services).length === 0) {
            container.innerHTML = `<div class="col-12"><p>No hay datos disponibles</p></div>`;
            return;
        }

        for (const [name, info] of Object.entries(services)) {
            const card = document.createElement("div");
            card.className = "col-md-6 col-lg-4";

            const statusClass = info.status === "healthy" ? "status-healthy" : "status-error";

            card.innerHTML = `
                <div class="card p-3">
                    <div class="card-header">${name}</div>
                    <div class="card-body">
                        <p>Estado: <span class="${statusClass}">${info.status}</span></p>
                        <p>Último check: ${info.last_checked || "N/A"}</p>
                        <p>Reiniciado: ${info.restarted ? "Sí" : "No"}</p>
                        <p>Error: ${info.error || "Ninguno"}</p>
                        <div class="log-box">${info.logs || "Sin logs"}</div>
                    </div>
                </div>
            `;

            container.appendChild(card);
        }
    } catch (err) {
        console.error("Error cargando datos:", err);
    }
}

// Refrescar cada 5 segundos
fetchHealth();
setInterval(fetchHealth, 5000);
