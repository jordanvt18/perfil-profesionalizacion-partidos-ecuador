/* ============================================================
   CONGRUENCIA — Mapa de Congruencia Programa–Votantes
   Frontend logic: map, radar, table, themes graph, export
   ============================================================ */

import { TEMAS, PARTIDOS, CANDIDATOS, CO_MENTION_MATRIX, THEME_GAPS, YEARS } from "./congruencia-demo-data.js";

const EC_CENTER = [-1.8312, -78.1834];
const $ = (id) => document.getElementById(id);

const state = {
  map: null,
  cantonLayer: null,
  circleLayer: null,
  selectedCanton: null,
  selectedCandidate: null,
  filtered: []
};

// ═══════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════
function uni(arr, k) {
  return [...new Set(arr.map(x => x[k]))].filter(Boolean).sort();
}

function fillSelect(id, allLabel, opts) {
  const sel = $(id);
  sel.innerHTML = "";
  const o0 = document.createElement("option");
  o0.value = "";
  o0.textContent = allLabel;
  sel.appendChild(o0);
  opts.forEach(v => {
    const o = document.createElement("option");
    o.value = v;
    o.textContent = String(v);
    sel.appendChild(o);
  });
}

// Color scale: red → orange → yellow → green
function congruenciaColor(v) {
  if (v >= 80) return "#22c55e";
  if (v >= 70) return "#84cc16";
  if (v >= 60) return "#f59e0b";
  if (v >= 50) return "#f97316";
  return "#ef4444";
}

// Get top 3 priority themes for a candidate
function top3Themes(cand) {
  const pv = cand.priority_vector;
  const indices = pv.map((v, i) => ({ v, i, tema: TEMAS[i] }))
    .sort((a, b) => b.v - a.v)
    .slice(0, 3);
  return indices;
}

// Get top 3 themes with biggest gap (demand > offer)
function topGapThemes(cand) {
  const gaps = cand.priority_vector.map((pv, i) => ({
    tema: TEMAS[i],
    gap: pv - (cand.program_vector[i] || 0),
    demanda: pv,
    oferta: cand.program_vector[i] || 0
  })).sort((a, b) => b.gap - a.gap);
  return gaps.slice(0, 3);
}

// ═══════════════════════════════════════════════════
// MAP
// ═══════════════════════════════════════════════════
function initMap() {
  state.map = L.map("map").setView(EC_CENTER, 6);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap | Mapa de Congruencia"
  }).addTo(state.map);
  state.cantonLayer = L.layerGroup().addTo(state.map);
  state.circleLayer = L.layerGroup().addTo(state.map);

  // Legend
  const legend = L.control({ position: "bottomright" });
  legend.onAdd = function () {
    const div = L.DomUtil.create("div", "info-legend");
    div.innerHTML = `
      <div style="font-size:0.72rem;font-weight:700;margin-bottom:4px">Congruencia</div>
      <div><i style="background:#22c55e;width:14px;height:14px;display:inline-block;border-radius:3px;vertical-align:middle;margin-right:4px"></i> 80–100</div>
      <div><i style="background:#84cc16;width:14px;height:14px;display:inline-block;border-radius:3px;vertical-align:middle;margin-right:4px"></i> 70–80</div>
      <div><i style="background:#f59e0b;width:14px;height:14px;display:inline-block;border-radius:3px;vertical-align:middle;margin-right:4px"></i> 60–70</div>
      <div><i style="background:#f97316;width:14px;height:14px;display:inline-block;border-radius:3px;vertical-align:middle;margin-right:4px"></i> 50–60</div>
      <div><i style="background:#ef4444;width:14px;height:14px;display:inline-block;border-radius:3px;vertical-align:middle;margin-right:4px"></i> 0–50</div>
    `;
    div.style.cssText = "background:#020617cc;padding:8px 10px;border-radius:6px;color:#e5e7eb;font-size:0.65rem;line-height:1.7;border:1px solid #374151;backdrop-filter:blur(8px);";
    return div;
  };
  legend.addTo(state.map);
}

function updateMap(cands) {
  state.cantonLayer.clearLayers();
  state.circleLayer.clearLayers();
  if (!cands.length) { state.map.setView(EC_CENTER, 6); return; }

  // Group by cantón
  const byCanton = {};
  cands.forEach(c => {
    const key = c.canton;
    if (!byCanton[key]) byCanton[key] = { vals: [], lat: c.lat, lon: c.lon, prov: c.provincia };
    byCanton[key].vals.push(c);
  });

  // Draw cantón circles
  Object.entries(byCanton).forEach(([canton, info]) => {
    const avg = info.vals.reduce((s, c) => s + c.congruence, 0) / info.vals.length;
    const clr = congruenciaColor(avg);
    const best = info.vals.reduce((a, b) => a.congruence > b.congruence ? a : b);
    const t3 = top3Themes(best);

    const c = L.circleMarker([info.lat, info.lon], {
      radius: 16 + (avg / 100) * 18,
      color: clr,
      fillColor: clr,
      fillOpacity: 0.3,
      weight: 2
    });
    c.bindPopup(
      `<b>${canton}</b> (${info.prov})<br>` +
      `Congruencia promedio: <b style="color:${clr}">${avg.toFixed(1)}/100</b><br>` +
      `Candidatos/as: ${info.vals.length}<br>` +
      `<hr style="border-color:#374151;margin:4px 0">` +
      `<b>Top 3 prioridades (mejor candidato):</b><br>` +
      `1. ${t3[0].tema} (${(t3[0].v * 100).toFixed(0)}%)<br>` +
      `2. ${t3[1].tema} (${(t3[1].v * 100).toFixed(0)}%)<br>` +
      `3. ${t3[2].tema} (${(t3[2].v * 100).toFixed(0)}%)`
    );
    c.on("click", () => {
      state.selectedCanton = canton;
      $("canton-select").value = canton;
      refresh();
    });
    c.addTo(state.cantonLayer);
  });

  // Overlay: per-candidate circles
  cands.forEach(r => {
    const t3 = top3Themes(r);
    const c2 = L.circleMarker([r.lat, r.lon], {
      radius: 7 + (r.congruence / 100) * 10,
      color: congruenciaColor(r.congruence),
      fillColor: congruenciaColor(r.congruence),
      fillOpacity: 0.75,
      weight: 1.5
    });
    c2.bindPopup(
      `<b>${r.canton}</b> (${r.provincia})<br>` +
      `${r.nombre}<br>${r.partido}<br>` +
      `Congruencia: <b style="color:${congruenciaColor(r.congruence)}">${r.congruence.toFixed(1)}/100</b><br>` +
      `<hr style="border-color:#374151;margin:4px 0">` +
      `<b>Top 3 prioridades:</b><br>` +
      `1. ${t3[0].tema} (${(t3[0].v * 100).toFixed(0)}%)<br>` +
      `2. ${t3[1].tema} (${(t3[1].v * 100).toFixed(0)}%)<br>` +
      `3. ${t3[2].tema} (${(t3[2].v * 100).toFixed(0)}%)`
    );
    c2.on("mouseover", function () { this.setStyle({ fillOpacity: 1, weight: 3 }); });
    c2.on("mouseout", function () { this.setStyle({ fillOpacity: 0.75, weight: 1.5 }); });
    c2.on("click", () => {
      state.selectedCandidate = r.id;
      $("candidate-select").value = String(r.id);
      updateRadar(r);
      showModal(r);
    });
    c2.addTo(state.circleLayer);
  });

  // Zoom to fit
  const selProv = $("province-select").value;
  if (selProv && cands.length > 0) {
    const lats = cands.map(r => r.lat), lons = cands.map(r => r.lon);
    const bounds = [[Math.min(...lats), Math.min(...lons)], [Math.max(...lats), Math.max(...lons)]];
    state.map.fitBounds(bounds, { padding: [20, 20], maxZoom: 11 });
  } else if (cands.length === 1) {
    state.map.setView([cands[0].lat, cands[0].lon], 11);
  } else {
    state.map.setView(EC_CENTER, 6);
  }
}

// ═══════════════════════════════════════════════════
// RADAR CHART (Plotly)
// ═══════════════════════════════════════════════════
function updateRadar(cand) {
  if (!cand) return;
  const target = $("radar-chart-container");
  if (!target) return;

  const data = [
    {
      type: "scatterpolar",
      r: cand.priority_vector.map(v => +(v * 100).toFixed(1)),
      theta: TEMAS,
      fill: "toself",
      name: "Prioridades ciudadanas",
      line: { color: "#3b82f6", width: 2 },
      fillcolor: "rgba(59,130,246,0.15)",
      hovertemplate: "<b>%{theta}</b><br>Prioridad: %{r:.1f}%<extra></extra>"
    },
    {
      type: "scatterpolar",
      r: cand.program_vector.map(v => +(v * 100).toFixed(1)),
      theta: TEMAS,
      fill: "toself",
      name: "Programa de gobierno",
      line: { color: "#22c55e", width: 2, dash: "dash" },
      fillcolor: "rgba(34,197,94,0.10)",
      hovertemplate: "<b>%{theta}</b><br>Programa: %{r:.1f}%<extra></extra>"
    }
  ];

  const layout = {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: "#e5e7eb", size: 9 },
    margin: { l: 40, r: 40, t: 30, b: 20 },
    polar: {
      bgcolor: "rgba(15,23,42,0.5)",
      radialaxis: {
        visible: true,
        range: [0, 100],
        tickfont: { size: 7, color: "#6b7280" },
        gridcolor: "rgba(255,255,255,0.08)",
        linecolor: "rgba(255,255,255,0.1)"
      },
      angularaxis: {
        tickfont: { size: 8, color: "#9ca3af" },
        gridcolor: "rgba(255,255,255,0.08)",
        linecolor: "rgba(255,255,255,0.1)"
      }
    },
    legend: {
      orientation: "h",
      y: -0.1,
      font: { size: 8, color: "#9ca3af" }
    },
    title: {
      text: `${cand.nombre} — ${cantonNombre(cand)}`,
      font: { size: 10, color: "#60a5fa" }
    }
  };

  Plotly.newPlot(target, data, layout, { displayModeBar: false, responsive: true });
}

function cantonNombre(c) {
  return `${c.canton}, ${c.provincia}`;
}

// ═══════════════════════════════════════════════════
// MODAL RADAR
// ═══════════════════════════════════════════════════
function updateModalRadar(cand) {
  const target = $("modal-radar");
  if (!target || !cand) return;

  const gaps = cand.priority_vector.map((pv, i) => ({
    tema: TEMAS[i],
    demanda: pv * 100,
    oferta: (cand.program_vector[i] || 0) * 100,
    gap: (pv - (cand.program_vector[i] || 0)) * 100
  })).sort((a, b) => Math.abs(b.gap) - Math.abs(a.gap));

  const data = [
    {
      type: "scatterpolar",
      r: cand.priority_vector.map(v => +(v * 100).toFixed(1)),
      theta: TEMAS,
      fill: "toself",
      name: "Prioridades ciudadanas",
      line: { color: "#3b82f6", width: 2 },
      fillcolor: "rgba(59,130,246,0.15)",
      hovertemplate: "<b>%{theta}</b><br>Prioridad: %{r:.1f}%<extra></extra>"
    },
    {
      type: "scatterpolar",
      r: cand.program_vector.map(v => +(v * 100).toFixed(1)),
      theta: TEMAS,
      fill: "toself",
      name: "Programa de gobierno",
      line: { color: "#22c55e", width: 2, dash: "dash" },
      fillcolor: "rgba(34,197,94,0.10)",
      hovertemplate: "<b>%{theta}</b><br>Programa: %{r:.1f}%<extra></extra>"
    }
  ];

  const layout = {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: "#e5e7eb", size: 9 },
    margin: { l: 40, r: 40, t: 20, b: 30 },
    polar: {
      bgcolor: "rgba(15,23,42,0.5)",
      radialaxis: {
        visible: true, range: [0, 100],
        tickfont: { size: 7, color: "#6b7280" },
        gridcolor: "rgba(255,255,255,0.08)"
      },
      angularaxis: {
        tickfont: { size: 8, color: "#9ca3af" },
        gridcolor: "rgba(255,255,255,0.08)"
      }
    },
    legend: { orientation: "h", y: -0.15, font: { size: 8 } }
  };

  Plotly.newPlot(target, data, layout, { displayModeBar: false, responsive: true });

  // Also update the details
  const t3 = top3Themes(cand);
  const g3 = topGapThemes(cand);
  $("candidate-details").innerHTML = `
    <h3 style="font-size:1.1rem;margin-bottom:0.15rem">${cand.nombre}</h3>
    <p style="color:#3b82f6;font-size:0.82rem;font-weight:600;margin-bottom:0.4rem">${cand.partido} — ${cand.dignidad}</p>
    <p style="font-size:0.78rem;color:#9ca3af;margin-bottom:0.3rem"><b>Provincia:</b> ${cand.provincia} · <b>Cantón:</b> ${cand.canton}</p>
    <p style="font-size:0.78rem;margin-bottom:0.3rem">Congruencia: <span class="cong-badge" style="background:${congruenciaColor(cand.congruence)}">${cand.congruence.toFixed(1)}/100</span></p>
    <div style="font-size:0.75rem;margin-top:0.5rem">
      <b style="color:#3b82f6">Top 3 prioridades ciudadanas:</b><br>
      1. ${t3[0].tema} (${(t3[0].v * 100).toFixed(0)}%)<br>
      2. ${t3[1].tema} (${(t3[1].v * 100).toFixed(0)}%)<br>
      3. ${t3[2].tema} (${(t3[2].v * 100).toFixed(0)}%)
    </div>
    <div style="font-size:0.75rem;margin-top:0.4rem">
      <b style="color:#ef4444">Mayores brechas (demanda sin cubrir):</b><br>
      1. ${g3[0].tema} (brecha: +${(g3[0].gap * 100).toFixed(0)}%)<br>
      2. ${g3[1].tema} (brecha: +${(g3[1].gap * 100).toFixed(0)}%)<br>
      3. ${g3[2].tema} (brecha: +${(g3[2].gap * 100).toFixed(0)}%)
    </div>
  `;
}

// ═══════════════════════════════════════════════════
// TABLE
// ═══════════════════════════════════════════════════
function updateTable(cands) {
  const tbody = $("candidates-table-body");
  const sorted = [...cands].sort((a, b) => b.congruence - a.congruence);

  tbody.innerHTML = sorted.map((c, i) => {
    const t3 = top3Themes(c);
    return `
      <tr class="candidate-row" data-id="${c.id}">
        <td>${i + 1}</td>
        <td class="cand-name" title="${c.nombre}">${c.nombre}</td>
        <td class="cand-party" title="${c.partido}">${c.partido}</td>
        <td>${c.provincia}</td>
        <td>${c.canton}</td>
        <td><span class="cong-badge" style="background:${congruenciaColor(c.congruence)}">${c.congruence.toFixed(1)}</span></td>
        <td style="font-size:0.72rem;color:#9ca3af">${t3.map(t => t.tema).join(" · ")}</td>
      </tr>`;
  }).join("");

  tbody.querySelectorAll(".candidate-row").forEach(row => {
    row.addEventListener("click", () => {
      const c = cands.find(x => x.id === Number(row.dataset.id));
      if (c) {
        updateRadar(c);
        showModal(c);
      }
    });
  });

  $("candidates-count").textContent = `${sorted.length} candidatos/as`;
}

// ═══════════════════════════════════════════════════
// STATS
// ═══════════════════════════════════════════════════
function updateStats(cands) {
  const avg = cands.length ? (cands.reduce((s, c) => s + c.congruence, 0) / cands.length).toFixed(1) : null;
  const best = cands.length ? cands.reduce((a, b) => a.congruence > b.congruence ? a : b) : null;
  $("stat-avg-cong").textContent = avg ? `${avg}/100` : "-";
  $("stat-cands").textContent = cands.length;
  $("stat-parties").textContent = new Set(cands.map(c => c.partido)).size;
  $("stat-best-cand").innerHTML = best
    ? `${best.congruence.toFixed(1)}<br><small>${best.nombre.split(" ").slice(0, 2).join(" ")}<br>${best.canton}</small>`
    : "-";
}

// ═══════════════════════════════════════════════════
// THEMES GRAPH (D3 force-directed)
// ═══════════════════════════════════════════════════
function renderThemesGraph() {
  const svg = d3.select("#themes-svg");
  svg.selectAll("*").remove();

  const container = document.getElementById("themes-graph-container");
  const width = container.clientWidth - 32;
  const height = 380;

  svg.attr("viewBox", `0 0 ${width} ${height}`);

  // Build nodes from TEMAS
  const nodes = TEMAS.map((tema, i) => ({
    id: i,
    name: tema,
    gap: THEME_GAPS[i].gap,
    oferta: THEME_GAPS[i].oferta,
    demanda: THEME_GAPS[i].demanda
  }));

  // Build edges from CO_MENTION_MATRIX
  const links = [];
  for (let i = 0; i < CO_MENTION_MATRIX.length; i++) {
    for (let j = i + 1; j < CO_MENTION_MATRIX[i].length; j++) {
      if (CO_MENTION_MATRIX[i][j] > 0) {
        links.push({
          source: i,
          target: j,
          weight: CO_MENTION_MATRIX[i][j]
        });
      }
    }
  }

  // Color scale for gap
  const maxGap = d3.max(nodes, d => Math.abs(d.gap));
  const colorScale = d3.scaleLinear()
    .domain([0, maxGap])
    .range(["#22c55e", "#ef4444"])
    .interpolate(d3.interpolateHcl);

  // Node radius based on demanda
  const rScale = d3.scaleLinear()
    .domain([0, d3.max(nodes, d => d.demanda)])
    .range([12, 28]);

  // Link width based on weight
  const wScale = d3.scaleLinear()
    .domain([0, d3.max(links, d => d.weight)])
    .range([0.5, 4]);

  // Force simulation
  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(d => 80 + (100 / d.weight) * 20))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(d => rScale(d.demanda) + 5));

  // Links
  const link = svg.append("g")
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke", "rgba(255,255,255,0.10)")
    .attr("stroke-width", d => wScale(d.weight))
    .attr("stroke-opacity", 0.6);

  // Node groups
  const node = svg.append("g")
    .selectAll("g")
    .data(nodes)
    .join("g")
    .style("cursor", "pointer")
    .call(drag(simulation));

  // Node circles
  node.append("circle")
    .attr("r", d => rScale(d.demanda))
    .attr("fill", d => colorScale(Math.abs(d.gap)))
    .attr("fill-opacity", 0.3)
    .attr("stroke", d => colorScale(Math.abs(d.gap)))
    .attr("stroke-width", 2);

  // Node labels
  node.append("text")
    .text(d => d.name.length > 20 ? d.name.substring(0, 18) + "…" : d.name)
    .attr("text-anchor", "middle")
    .attr("dy", d => rScale(d.demanda) + 12)
    .attr("font-size", "8px")
    .attr("fill", "#e5e7eb")
    .attr("font-family", "system-ui, sans-serif");

  // Tooltip
  const tooltip = d3.select("body").append("div")
    .style("position", "absolute")
    .style("background", "#020617")
    .style("border", "1px solid #374151")
    .style("border-radius", "6px")
    .style("padding", "8px 10px")
    .style("font-size", "0.72rem")
    .style("color", "#e5e7eb")
    .style("pointer-events", "none")
    .style("opacity", 0)
    .style("z-index", 10000)
    .style("max-width", "220px");

  node.on("mouseover", (event, d) => {
    tooltip.style("opacity", 1).html(
      `<b>${d.name}</b><br>` +
      `Demanda ciudadana: <b style="color:#3b82f6">${(d.demanda * 100).toFixed(0)}%</b><br>` +
      `Oferta en programas: <b style="color:#22c55e">${(d.oferta * 100).toFixed(0)}%</b><br>` +
      `Brecha: <b style="color:${d.gap > 0.05 ? "#ef4444" : "#22c55e"}">${d.gap > 0 ? "+" : ""}${(d.gap * 100).toFixed(0)}%</b>`
    );
  })
    .on("mousemove", (event) => {
      tooltip
        .style("left", (event.pageX + 12) + "px")
        .style("top", (event.pageY - 10) + "px");
    })
    .on("mouseout", () => tooltip.style("opacity", 0));

  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);
    node.attr("transform", d => {
      d.x = Math.max(rScale(d.demanda) + 2, Math.min(width - rScale(d.demanda) - 2, d.x));
      d.y = Math.max(rScale(d.demanda) + 2, Math.min(height - rScale(d.demanda) - 14, d.y));
      return `translate(${d.x},${d.y})`;
    });
  });

  // Drag functions
  function drag(simulation) {
    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }
    function dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }
    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }
    return d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended);
  }
}

// ═══════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════
function exportCSV() {
  const cands = state.filtered;
  if (!cands.length) return;

  const headers = ["#", "Nombre", "Partido", "Provincia", "Cantón", "Congruencia", "Tema 1", "Tema 2", "Tema 3"];
  const rows = cands
    .sort((a, b) => b.congruence - a.congruence)
    .map((c, i) => {
      const t3 = top3Themes(c);
      return [
        i + 1,
        `"${c.nombre}"`,
        `"${c.partido}"`,
        `"${c.provincia}"`,
        `"${c.canton}"`,
        c.congruence.toFixed(2),
        `"${t3[0].tema}"`,
        `"${t3[1].tema}"`,
        `"${t3[2].tema}"`
      ].join(",");
    });

  const csv = "\uFEFF" + headers.join(",") + "\n" + rows.join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `congruencia_${new Date().toISOString().slice(0, 10)}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

function exportJSON() {
  const data = {
    fecha_exportacion: new Date().toISOString(),
    filtros: {
      partido: $("party-select").value || "Todos",
      candidato: $("candidate-select").value || "Todos",
      provincia: $("province-select").value || "Todas",
      canton: $("canton-select").value || "Todos",
      year: $("year-select").value || "Todos"
    },
    candidatos: state.filtered.map(c => ({
      ...c,
      top_3_prioridades: top3Themes(c).map(t => ({ tema: t.tema, valor: t.v })),
      top_3_brechas: topGapThemes(c).map(t => ({ tema: t.tema, brecha: t.gap }))
    }))
  };

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `congruencia_${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

// ═══════════════════════════════════════════════════
// MODAL
// ═══════════════════════════════════════════════════
function showModal(c) {
  updateModalRadar(c);
  $("candidate-modal").classList.remove("hidden");
}

function initModal() {
  const m = $("candidate-modal");
  $("modal-close").addEventListener("click", () => m.classList.add("hidden"));
  m.addEventListener("click", e => { if (e.target === m) m.classList.add("hidden"); });
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && !m.classList.contains("hidden")) m.classList.add("hidden");
  });
}

// ═══════════════════════════════════════════════════
// SELECTORS
// ═══════════════════════════════════════════════════
function initSelectors() {
  // Parties
  fillSelect("party-select", "Todos los partidos", PARTIDOS);

  // Candidates (filtered by party later)
  fillSelect("candidate-select", "Todos los candidatos", CANDIDATOS.map(c => c.nombre));
  // Store candidate names → id mapping via data attributes
  const candSel = $("candidate-select");
  candSel.innerHTML = '<option value="">Todos los candidatos</option>';
  CANDIDATOS.forEach(c => {
    const o = document.createElement("option");
    o.value = c.id;
    o.textContent = `${c.nombre} (${c.canton})`;
    candSel.appendChild(o);
  });

  // Provinces
  fillSelect("province-select", "Todas las provincias", uni(CANDIDATOS, "provincia"));

  // Cantones
  fillSelect("canton-select", "Todos los cantones", uni(CANDIDATOS, "canton"));

  // Years
  fillSelect("year-select", "Todos los años", YEARS.map(String));
  $("year-select").value = "2026";

  // Cascade: party → candidate
  $("party-select").addEventListener("change", () => {
    const p = $("party-select").value;
    const candSel = $("candidate-select");
    candSel.innerHTML = '<option value="">Todos los candidatos</option>';
    const filtered = p ? CANDIDATOS.filter(c => c.partido === p) : CANDIDATOS;
    filtered.forEach(c => {
      const o = document.createElement("option");
      o.value = c.id;
      o.textContent = `${c.nombre} (${c.canton})`;
      candSel.appendChild(o);
    });
    candSel.value = "";
  });

  // Cascade: province → canton
  $("province-select").addEventListener("change", () => {
    const p = $("province-select").value;
    const cantonSel = $("canton-select");
    cantonSel.innerHTML = '<option value="">Todos los cantones</option>';
    const filtered = p ? uni(CANDIDATOS.filter(c => c.provincia === p), "canton") : uni(CANDIDATOS, "canton");
    filtered.forEach(v => {
      const o = document.createElement("option");
      o.value = v;
      o.textContent = v;
      cantonSel.appendChild(o);
    });
    cantonSel.value = "";
  });

  // Candidate select → update radar directly
  $("candidate-select").addEventListener("change", () => {
    const id = $("candidate-select").value;
    if (id) {
      const c = CANDIDATOS.find(x => x.id === Number(id));
      if (c) updateRadar(c);
    }
  });
}

// ═══════════════════════════════════════════════════
// FILTER & REFRESH
// ═══════════════════════════════════════════════════
function refresh() {
  const party = $("party-select").value;
  const candId = $("candidate-select").value;
  const prov = $("province-select").value;
  const canton = $("canton-select").value;
  const yr = $("year-select").value;

  let cands = [...CANDIDATOS];

  if (party) cands = cands.filter(c => c.partido === party);
  if (candId) cands = cands.filter(c => c.id === Number(candId));
  if (prov) cands = cands.filter(c => c.provincia === prov);
  if (canton) cands = cands.filter(c => c.canton === canton);
  if (yr) cands = cands.filter(c => c.year === Number(yr));

  state.filtered = cands;

  updateMap(cands);
  updateTable(cands);
  updateStats(cands);

  // Update radar with best candidate if none selected
  if (!candId && cands.length > 0) {
    const best = cands.reduce((a, b) => a.congruence > b.congruence ? a : b);
    updateRadar(best);
  } else if (candId) {
    const c = CANDIDATOS.find(x => x.id === Number(candId));
    if (c) updateRadar(c);
  }
}

// ═══════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════
function main() {
  initSelectors();
  initMap();
  initModal();

  // Event listeners
  ["party-select", "candidate-select", "province-select", "canton-select", "year-select"].forEach(id => {
    $(id).addEventListener("change", refresh);
  });

  $("export-csv").addEventListener("click", exportCSV);
  $("export-json").addEventListener("click", exportJSON);

  // Initial render
  refresh();
  renderThemesGraph();

  // Re-render themes graph on resize
  let resizeTimer;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      renderThemesGraph();
    }, 300);
  });
}

main().catch(err => {
  console.error(err);
  document.body.insertAdjacentHTML("afterbegin",
    `<div style="background:#7f1d1d;color:#fca5a5;padding:0.75rem;text-align:center;font-size:0.9rem">
      Error al cargar: ${err.message}<br><small>Abra consola (F12).</small></div>`);
});
