const API_BASE = "https://example-api-url.com"; // Reemplazar con URL real de despliegue

let map;
let provincesLayer;

async function fetchJSON(path) {
  const resp = await fetch(`${API_BASE}${path}`);
  if (!resp.ok) {
    throw new Error(`Error al llamar API: ${resp.status}`);
  }
  return await resp.json();
}

async function initSelectors() {
  const partySelect = document.getElementById("party-select");
  const yearSelect = document.getElementById("year-select");
  const provinceSelect = document.getElementById("province-select");

  const partiesResp = await fetchJSON("/parties");
  partiesResp.parties.forEach((p) => {
    const opt = document.createElement("option");
    opt.value = p;
    opt.textContent = p;
    partySelect.appendChild(opt);
  });

  [2021, 2023, 2025].forEach((y) => {
    const opt = document.createElement("option");
    opt.value = y;
    opt.textContent = y;
    yearSelect.appendChild(opt);
  });

  const provinces = ["Guayas", "Pichincha", "Manabí"]; // Placeholder, reemplazar con API/geometrías reales
  provinces.forEach((prov) => {
    const opt = document.createElement("option");
    opt.value = prov;
    opt.textContent = prov;
    provinceSelect.appendChild(opt);
  });
}

function initMap() {
  map = L.map("map").setView([-1.8312, -78.1834], 6);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  provincesLayer = L.layerGroup().addTo(map);
}

function updateMap(aggregates) {
  provincesLayer.clearLayers();

  aggregates.forEach((row) => {
    const lat = row.lat || -1.83;
    const lon = row.lon || -78.18;
    const value = row.profesionalizacion_media;

    const circle = L.circleMarker([lat, lon], {
      radius: 8,
      color: "#22c55e",
      fillColor: "#22c55e",
      fillOpacity: 0.7,
    }).bindPopup(
      `${row.province} – ${row.party_normalized}<br/>Índice: ${value.toFixed(1)}`
    );

    circle.addTo(provincesLayer);
  });
}

function updateAcademicBars(candidates) {
  const container = document.getElementById("academic-bars-chart");

  const levelsCount = d3.rollup(
    candidates,
    (v) => v.length,
    (d) => d.max_degree
  );

  const labels = Array.from(levelsCount.keys());
  const values = Array.from(levelsCount.values());

  const data = [
    {
      x: labels,
      y: values,
      type: "bar",
      marker: { color: "#6366f1" },
    },
  ];

  Plotly.newPlot(container, data, {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: "#e5e7eb" },
  });
}

function updateTurnoutSeries(turnout) {
  const container = document.getElementById("turnout-series-chart");

  const grouped = d3.group(turnout, (d) => d.canton);

  const traces = [];
  grouped.forEach((values, canton) => {
    const years = values.map((d) => d.year);
    const turnoutVals = values.map((d) => d.turnout);
    traces.push({
      x: years,
      y: turnoutVals,
      mode: "lines+markers",
      name: canton,
    });
  });

  Plotly.newPlot(container, traces, {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: "#e5e7eb" },
  });
}

function showCandidateModal(candidate) {
  const modal = document.getElementById("candidate-modal");
  const details = document.getElementById("candidate-details");

  details.innerHTML = `
    <h3>${candidate.name}</h3>
    <p><strong>Partido:</strong> ${candidate.party_normalized}</p>
    <p><strong>Provincia:</strong> ${candidate.province}</p>
    <p><strong>Índice de profesionalización:</strong> ${
      candidate.profesionalizacion.toFixed(1)
    }</p>
    <p><strong>Educación:</strong> ${candidate.max_degree}</p>
    <p><strong>Años de experiencia pública:</strong> ${
      candidate.years_public_service
    }</p>
  `;

  modal.classList.remove("hidden");
}

function initModal() {
  const modal = document.getElementById("candidate-modal");
  const closeBtn = document.getElementById("modal-close");

  closeBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.add("hidden");
    }
  });
}

async function refreshData() {
  const party = document.getElementById("party-select").value;
  const year = document.getElementById("year-select").value;
  const province = document.getElementById("province-select").value;

  const [aggResp, candidatesResp, turnoutResp] = await Promise.all([
    fetchJSON(`/aggregates?party=${party}&province=${province}`),
    fetchJSON(`/candidates?party=${party}&province=${province}`),
    fetchJSON(`/turnout?year=${year}&province=${province}`),
  ]);

  updateMap(aggResp.aggregates);
  updateAcademicBars(candidatesResp.candidates);
  updateTurnoutSeries(turnoutResp.turnout);
}

async function main() {
  await initSelectors();
  initMap();
  initModal();

  document
    .getElementById("party-select")
    .addEventListener("change", () => refreshData());
  document
    .getElementById("year-select")
    .addEventListener("change", () => refreshData());
  document
    .getElementById("province-select")
    .addEventListener("change", () => refreshData());

  await refreshData();
}

main().catch((err) => console.error(err));
