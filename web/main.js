/* global L, Plotly, d3 */
import { demoAggregates, demoCandidates, demoTurnout } from "./demo-data.js";

const EC_CENTER = [-1.8312, -78.1834];
const state = { aggregates:[], candidates:[], turnout:[], map:null, cantonLayer:null, circleLayer:null };

const $ = (id) => document.getElementById(id);

function pick(path) {
  if (path.startsWith("/aggregates"))  return { aggregates:  demoAggregates };
  if (path.startsWith("/candidates"))  return { candidates:  demoCandidates };
  if (path.startsWith("/turnout"))     return { turnout:     demoTurnout };
  if (path.startsWith("/parties"))     return { parties:     uni(demoCandidates,"party_normalized") };
  if (path.startsWith("/provinces"))   return { provinces:   uni(demoCandidates,"provincia") };
  if (path.startsWith("/cantones"))    return { cantones:    uni(demoCandidates,"canton") };
  if (path.startsWith("/years"))       return { years:       uni(demoTurnout,"year") };
  if (path.startsWith("/dignidades"))  return { dignidades:  uni(demoCandidates,"dignidad") };
  throw new Error("path not found: "+path);
}
function uni(arr,k){return[...new Set(arr.map(x=>x[k]))].filter(Boolean).sort();}

// ═══ MAPA: color por canton con gradiente ═══
function initMap() {
  state.map = L.map("map").setView(EC_CENTER, 6);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom:19, attribution:"&copy; OpenStreetMap | Indice profesionalizacion"
  }).addTo(state.map);
  state.cantonLayer = L.layerGroup().addTo(state.map);
  state.circleLayer = L.layerGroup().addTo(state.map);

  // Legend
  const legend = L.control({position:"bottomright"});
  legend.onAdd = function() {
    const div = L.DomUtil.create("div","info-legend");
    div.innerHTML = `
      <div style="font-size:0.72rem;font-weight:700;margin-bottom:4px">Indice promedio</div>
      <div><i style="background:#ef4444;width:14px;height:14px;display:inline-block;border-radius:3px;vertical-align:middle;margin-right:4px"></i> 0–35</div>
      <div><i style="background:#f97316;width:14px;height:14px;display:inline-block;border-radius:3px;vertical-align:middle;margin-right:4px"></i> 35–50</div>
      <div><i style="background:#f59e0b;width:14px;height:14px;display:inline-block;border-radius:3px;vertical-align:middle;margin-right:4px"></i> 50–65</div>
      <div><i style="background:#84cc16;width:14px;height:14px;display:inline-block;border-radius:3px;vertical-align:middle;margin-right:4px"></i> 65–80</div>
      <div><i style="background:#22c55e;width:14px;height:14px;display:inline-block;border-radius:3px;vertical-align:middle;margin-right:4px"></i> 80–100</div>
    `;
    div.style.cssText = "background:#020617cc;padding:8px 10px;border-radius:6px;color:#e5e7eb;font-size:0.65rem;line-height:1.7;border:1px solid #374151;backdrop-filter:blur(8px);";
    return div;
  };
  legend.addTo(state.map);
}

function colorFor(v){ return v>=80?"#22c55e":v>=65?"#84cc16":v>=50?"#f59e0b":v>=35?"#f97316":"#ef4444"; }

function updateMap(aggregates) {
  state.cantonLayer.clearLayers();
  state.circleLayer.clearLayers();
  if (!aggregates.length) { state.map.setView(EC_CENTER,6); return; }

  // Group by canton to color the canton polygon
  const byCanton = {};
  aggregates.forEach(r => {
    const key = r.canton || r.province;
    if (!byCanton[key]) byCanton[key] = { vals:[], lat:r.lat, lon:r.lon, prov:r.province, party:r.party_normalized };
    byCanton[key].vals.push(r.profesionalizacion_media);
  });

  // Draw canton circles (bigger, semi-transparent)
  Object.entries(byCanton).forEach(([canton, info]) => {
    const avg = info.vals.reduce((a,b)=>a+b,0)/info.vals.length;
    const clr = colorFor(avg);
    // Canton base circle
    const c = L.circleMarker([info.lat, info.lon], {
      radius: 14 + (avg/100)*16,
      color: clr,
      fillColor: clr,
      fillOpacity: 0.3,
      weight: 2,
    });
    c.bindPopup(`<b>${canton}</b><br>Provincia: ${info.prov}<br>Indice promedio: <b>${avg.toFixed(1)}</b>/100<br>Partidos: ${info.vals.length}`);
    c.addTo(state.cantonLayer);
  });

  // Overlay: smaller circles per party in that canton
  aggregates.forEach(r => {
    const c2 = L.circleMarker([r.lat, r.lon], {
      radius: 6 + (r.profesionalizacion_media/100)*10,
      color: colorFor(r.profesionalizacion_media),
      fillColor: colorFor(r.profesionalizacion_media),
      fillOpacity: 0.7,
      weight: 1.5,
    });
    c2.bindPopup(
      `<b>${r.canton || r.province}</b> (${r.province})<br>`+
      `${r.party_normalized}<br>${r.dignidad}<br>Indice: <b>${r.profesionalizacion_media.toFixed(1)}</b>/100`
    );
    c2.on("mouseover", function(){this.setStyle({fillOpacity:1,weight:3});});
    c2.on("mouseout", function(){this.setStyle({fillOpacity:0.7,weight:1.5});});
    c2.addTo(state.circleLayer);
  });

  // Zoom to fit if province selected
  const selProv = $("province-select").value;
  if (selProv && aggregates.length > 0) {
    const lats = aggregates.map(r=>r.lat), lons = aggregates.map(r=>r.lon);
    const bounds = [[Math.min(...lats),Math.min(...lons)],[Math.max(...lats),Math.max(...lons)]];
    state.map.fitBounds(bounds, {padding:[20,20], maxZoom:11});
  } else if (aggregates.length === 1) {
    state.map.setView([aggregates[0].lat, aggregates[0].lon], 11);
  } else {
    state.map.setView(EC_CENTER, 6);
  }
}

// ═══ CHARTS ═══
function updateAcademicBars(cands) {
  const lvls=["primaria","secundaria","tecnico","universitario","posgrado"];
  const cols=["#ef4444","#f97316","#f59e0b","#84cc16","#22c55e"];
  const lbls=["Primaria","Secundaria","Tecnico","Universitario","Posgrado"];
  const cts=lvls.map(l=>cands.filter(c=>c.max_degree===l).length);
  Plotly.newPlot($("academic-bars-chart"),[{
    x:cts,y:lbls,type:"bar",orientation:"h",
    marker:{color:cols,line:{color:"rgba(255,255,255,0.10)",width:1}},
    text:cts.map(v=>v?String(v):""),textposition:"outside",textfont:{color:"#e5e7eb",size:10},
    hovertemplate:"%{x} precandidatos<extra></extra>"
  }],{
    paper_bgcolor:"rgba(0,0,0,0)",plot_bgcolor:"rgba(0,0,0,0)",
    font:{color:"#e5e7eb",size:9},
    margin:{l:105,r:20,t:5,b:20},
    xaxis:{title:"N. precandidatos",gridcolor:"rgba(255,255,255,0.06)"},
    yaxis:{automargin:true,gridcolor:"rgba(255,255,255,0.06)"}
  },{displayModeBar:false,responsive:true});
}

function updateTurnoutSeries(turnout) {
  const grouped = d3.group(turnout,d=>d.canton);
  const traces=[]; let idx=0;
  grouped.forEach((vals,canton)=>{
    vals.sort((a,b)=>a.year-b.year);
    traces.push({
      x:vals.map(d=>d.year),y:vals.map(d=>d.turnout),
      mode:"lines+markers",name:canton,line:{width:2},marker:{size:5},
      hovertemplate:"%{y:.1f}%<extra>%{fullData.name}</extra>",
      visible:idx<6?true:"legendonly"
    }); idx++;
  });
  if(traces.length>12) traces.forEach((t,i)=>{t.visible=i===0;});
  Plotly.newPlot($("turnout-series-chart"),traces,{
    paper_bgcolor:"rgba(0,0,0,0)",plot_bgcolor:"rgba(0,0,0,0)",
    font:{color:"#e5e7eb",size:8},
    margin:{l:40,r:10,t:5,b:30},
    xaxis:{title:"Ano",dtick:1,gridcolor:"rgba(255,255,255,0.06)"},
    yaxis:{title:"Participacion (%)",range:[60,92],gridcolor:"rgba(255,255,255,0.06)"},
    legend:{orientation:"h",y:-0.4,font:{size:7}}
  },{displayModeBar:false,responsive:true});
}

// ═══ STATS ═══
function updateSummaryStats(agg, cands) {
  const avg = agg.length ? (agg.reduce((s,a)=>s+a.profesionalizacion_media,0)/agg.length).toFixed(1) : null;
  const best = agg.length ? agg.reduce((a,b)=>a.profesionalizacion_media>b.profesionalizacion_media?a:b) : null;
  const bestCanton = best ? `${best.canton || best.province}` : "-";
  $("stat-avg").textContent = avg ? `${avg}/100` : "-";
  $("stat-candidates").textContent = cands.length;
  $("stat-parties").textContent = new Set(cands.map(c=>c.party_normalized)).size;
  $("stat-best").innerHTML = best ? `${best.profesionalizacion_media?.toFixed(1)}<br><small>${best.party_normalized}<br>${bestCanton}</small>` : "-";
}

// ═══ TABLE ═══
const DG={primaria:"Primaria",secundaria:"Secundaria",tecnico:"Tecnico",universitario:"Universitario",posgrado:"Posgrado"};

function updateCandidatesTable(cands) {
  const tbody=$("candidates-table-body");
  const sorted=[...cands].sort((a,b)=>b.profesionalizacion-a.profesionalizacion);
  const top=sorted.slice(0,50);
  tbody.innerHTML=top.map((c,i)=>`
    <tr class="candidate-row" data-id="${c.candidate_id}">
      <td>${i+1}</td>
      <td class="cand-name" title="${c.nombre}">${c.nombre}</td>
      <td class="cand-party" title="${c.party_normalized}">${c.party_normalized}</td>
      <td>${c.dignidad}</td>
      <td>${c.provincia}</td>
      <td>${c.canton||"-"}</td>
      <td>${DG[c.max_degree]||c.max_degree}</td>
      <td>${c.years_public_service}a</td>
      <td><span class="prof-badge" style="background:${colorFor(c.profesionalizacion)}">${c.profesionalizacion?.toFixed(1)}</span></td>
      <td><span class="source-badge ${(c.fuente||'').includes('Confirmado')?'source-confirmed':'source-synthetic'}">${(c.fuente||'').includes('Confirmado')?'CONFIRMADO':'sintetico'}</span></td>
    </tr>`).join("");
  tbody.querySelectorAll(".candidate-row").forEach(row=>{
    row.addEventListener("click",()=>{
      const c=cands.find(x=>x.candidate_id===Number(row.dataset.id));
      if(c) showModal(c);
    });
  });
  $("candidates-count").textContent = `Top ${top.length} de ${cands.length}`;
}

// ═══ MODAL ═══
function showModal(c) {
  $("candidate-details").innerHTML=`
    <h3>${c.nombre}</h3>
    <p class="modal-dignidad">${c.dignidad} — ${c.party_normalized}</p>
    <div class="candidate-stats">
      <div class="stat-item"><span class="stat-label">Indice</span><span class="stat-value" style="color:${colorFor(c.profesionalizacion)}">${c.profesionalizacion?.toFixed(1)}/100</span></div>
      <div class="stat-item"><span class="stat-label">Formacion</span><span class="stat-value">${c.score_academico??"-"}/100</span></div>
      <div class="stat-item"><span class="stat-label">Experiencia</span><span class="stat-value">${c.score_experiencia??"-"}/40</span></div>
    </div>
    <table class="detail-table">
      <tr><td><b>Partido</b></td><td>${c.party_normalized}</td></tr>
      <tr><td><b>Provincia</b></td><td>${c.provincia}</td></tr>
      <tr><td><b>Canton</b></td><td>${c.canton||"-"}</td></tr>
      <tr><td><b>Educacion</b></td><td>${DG[c.max_degree]||c.max_degree}</td></tr>
      <tr><td><b>Serv. publico</b></td><td>${c.years_public_service} anos</td></tr>
      <tr><td><b>Fuente</b></td><td style="${(c.fuente||'').includes('Confirmado')?'color:#22c55e':'color:#f59e0b'}">${c.fuente||'No verificada'}</td></tr>
    </table>`;
  $("candidate-modal").classList.remove("hidden");
}

function initModal() {
  const m=$("candidate-modal");
  $("modal-close").addEventListener("click",()=>m.classList.add("hidden"));
  m.addEventListener("click",e=>{if(e.target===m)m.classList.add("hidden");});
  document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!m.classList.contains("hidden"))m.classList.add("hidden");});
}

// ═══ SELECTORS ═══
function initSelectors() {
  const [digs,parties,provs,cantones,years]=[pick("/dignidades"),pick("/parties"),pick("/provinces"),pick("/cantones"),pick("/years")];
  fill("dignidad-select","Todas las dignidades",digs.dignidades);
  fill("party-select","Todos los partidos",parties.parties);
  fill("province-select","Todas las provincias",provs.provinces);
  fill("canton-select","Todos los cantones",cantones.cantones);
  fill("year-select","Todos los anos",years.years);
  $("year-select").value="2026";
  // Cascade province->canton
  $("province-select").addEventListener("change",()=>{
    const p=$("province-select").value;
    const sel=$("canton-select");
    sel.innerHTML='<option value="">Todos los cantones</option>';
    const filtered = p ? uni(state.candidates.filter(c=>c.provincia===p),"canton") : uni(state.candidates,"canton");
    filtered.forEach(v=>{const o=document.createElement("option");o.value=v;o.textContent=v;sel.appendChild(o);});
    sel.value="";
  });
}

function fill(id,allLabel,opts){
  const sel=$(id); sel.innerHTML="";
  const o0=document.createElement("option");o0.value="";o0.textContent=allLabel;sel.appendChild(o0);
  opts.forEach(v=>{const o=document.createElement("option");o.value=v;o.textContent=String(v);sel.appendChild(o);});
}

// ═══ FILTER ═══
function refresh() {
  const dig=$("dignidad-select").value, party=$("party-select").value;
  const prov=$("province-select").value, canton=$("canton-select").value;
  const yr=$("year-select").value;
  let agg=state.aggregates, can=state.candidates, tur=state.turnout;
  if(dig)    {agg=agg.filter(r=>r.dignidad===dig);can=can.filter(c=>c.dignidad===dig);}
  if(party)  {agg=agg.filter(r=>r.party_normalized===party);can=can.filter(c=>c.party_normalized===party);}
  if(prov)   {agg=agg.filter(r=>r.province===prov);can=can.filter(c=>c.provincia===prov);tur=tur.filter(t=>t.province===prov);}
  if(canton) {agg=agg.filter(r=>r.canton===canton);can=can.filter(c=>c.canton===canton);tur=tur.filter(t=>t.canton===canton);}
  if(yr)     {tur=tur.filter(t=>t.year===Number(yr));}
  updateMap(agg); updateAcademicBars(can); updateTurnoutSeries(tur);
  updateSummaryStats(agg,can); updateCandidatesTable(can);
}

// ═══ INIT ═══
async function main() {
  const [a,c,t]=[pick("/aggregates"),pick("/candidates"),pick("/turnout")];
  state.aggregates=a.aggregates; state.candidates=c.candidates; state.turnout=t.turnout;
  initSelectors(); initMap(); initModal();
  $("dignidad-select").addEventListener("change",refresh);
  $("party-select").addEventListener("change",refresh);
  $("province-select").addEventListener("change",refresh);
  $("canton-select").addEventListener("change",refresh);
  $("year-select").addEventListener("change",refresh);
  refresh();
}

main().catch(err=>{
  console.error(err);
  document.body.insertAdjacentHTML("afterbegin",
    `<div style="background:#7f1d1d;color:#fca5a5;padding:0.75rem;text-align:center;font-size:0.9rem">
      Error al cargar: ${err.message}<br><small>Abra consola (F12).</small></div>`);
});
