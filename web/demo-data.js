// Datos de ejemplo para la demo pública (sin necesidad de API real)

export const demoAggregates = [
  {
    province: "Guayas",
    party_normalized: "PARTIDO A",
    profesionalizacion_media: 72.5,
    lat: -2.1833,
    lon: -79.8833,
  },
  {
    province: "Pichincha",
    party_normalized: "PARTIDO B",
    profesionalizacion_media: 65.2,
    lat: -0.2299,
    lon: -78.5249,
  },
  {
    province: "Manabí",
    party_normalized: "PARTIDO A",
    profesionalizacion_media: 68.1,
    lat: -0.8133,
    lon: -80.1978,
  },
];

export const demoCandidates = [
  {
    candidate_id: 1,
    name: "Candidato 1",
    party_normalized: "PARTIDO A",
    province: "Guayas",
    profesionalizacion: 78.0,
    max_degree: "posgrado",
    years_public_service: 10,
  },
  {
    candidate_id: 2,
    name: "Candidato 2",
    party_normalized: "PARTIDO A",
    province: "Guayas",
    profesionalizacion: 68.5,
    max_degree: "universitario",
    years_public_service: 5,
  },
  {
    candidate_id: 3,
    name: "Candidato 3",
    party_normalized: "PARTIDO B",
    province: "Pichincha",
    profesionalizacion: 70.0,
    max_degree: "universitario",
    years_public_service: 8,
  },
];

export const demoTurnout = [
  { province: "Guayas", canton: "Guayaquil", year: 2017, turnout: 78.2 },
  { province: "Guayas", canton: "Guayaquil", year: 2021, turnout: 75.5 },
  { province: "Guayas", canton: "Guayaquil", year: 2025, turnout: 79.1 },
  { province: "Guayas", canton: "Daule", year: 2017, turnout: 80.0 },
  { province: "Guayas", canton: "Daule", year: 2021, turnout: 77.3 },
  { province: "Guayas", canton: "Daule", year: 2025, turnout: 81.4 },
  { province: "Pichincha", canton: "Quito", year: 2017, turnout: 82.0 },
  { province: "Pichincha", canton: "Quito", year: 2021, turnout: 80.1 },
  { province: "Pichincha", canton: "Quito", year: 2025, turnout: 83.0 },
];
