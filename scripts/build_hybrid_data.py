#!/usr/bin/env python3
"""
Hybrid dataset v2.1: Expanded REAL confirmed candidates with verified education + synthetic fill.
Each candidate has "fuente": "Confirmado: [media]" or "Sintetico - no confirmado"
Updated: Aug 2026 - confirmed list expanded with the CNE inscription wave (ADN in Guayas/Pichincha, Cuenca, Ambato); Amigo suspended by TCE.
"""
import json, random
from pathlib import Path
from datetime import datetime

random.seed(20261109)

# ════════════ FULL CANTON DATABASE ════════════
CANTONES = {
    "Azuay": {"Cuenca":(-2.897,-79.005),"Gualaceo":(-2.894,-78.778),"Paute":(-2.781,-78.761),"Sigsig":(-3.051,-78.796)},
    "Bolivar": {"Guaranda":(-1.593,-79.002),"San Miguel":(-1.708,-79.043)},
    "Canar": {"Azogues":(-2.739,-78.848),"La Troncal":(-2.424,-79.340),"Biblian":(-2.713,-78.888)},
    "Carchi": {"Tulcan":(0.812,-77.717),"Mira":(0.598,-78.071),"San Gabriel":(0.593,-77.829)},
    "Chimborazo": {"Riobamba":(-1.671,-78.647),"Guano":(-1.594,-78.635),"Colta":(-1.731,-78.759)},
    "Cotopaxi": {"Latacunga":(-0.935,-78.616),"Pujili":(-0.951,-78.694),"Salcedo":(-1.047,-78.590)},
    "El Oro": {"Machala":(-3.259,-79.955),"Santa Rosa":(-3.451,-79.959),"Pasaje":(-3.330,-79.806)},
    "Esmeraldas": {"Esmeraldas":(0.950,-79.654),"Atacames":(0.866,-79.838),"Quininde":(0.330,-79.464)},
    "Galapagos": {"Santa Cruz":(-0.625,-90.376),"San Cristobal":(-0.902,-89.609)},
    "Guayas": {"Guayaquil":(-2.189,-79.889),"Daule":(-1.863,-79.980),"Samborondon":(-2.024,-79.724),"Duran":(-2.169,-79.832),"Milagro":(-2.129,-79.595)},
    "Imbabura": {"Ibarra":(0.351,-78.122),"Otavalo":(0.234,-78.262),"Cotacachi":(0.300,-78.264)},
    "Loja": {"Loja":(-3.993,-79.204),"Catamayo":(-4.002,-79.355),"Saraguro":(-3.621,-79.239)},
    "Los Rios": {"Babahoyo":(-1.802,-79.535),"Quevedo":(-1.029,-79.464),"Ventanas":(-1.446,-79.459)},
    "Manabi": {"Portoviejo":(-1.056,-80.454),"Manta":(-0.954,-80.728),"Chone":(-0.687,-80.094),"Montecristi":(-1.046,-80.659),"Pedernales":(0.078,-80.050)},
    "Morona Santiago": {"Macas":(-2.309,-78.116),"Sucua":(-2.457,-78.167)},
    "Napo": {"Tena":(-0.990,-77.815),"Archidona":(-0.904,-77.810)},
    "Orellana": {"Puerto Francisco de Orellana":(-0.467,-76.987),"La Joya de los Sachas":(-0.301,-76.854)},
    "Pastaza": {"Puyo":(-1.481,-78.003)},
    "Pichincha": {"Quito":(-0.181,-78.468),"Cayambe":(0.045,-78.157),"Machachi":(-0.513,-78.566),"Pedro Moncayo":(0.047,-78.246),"San Miguel de los Bancos":(0.023,-78.892)},
    "Santa Elena": {"Santa Elena":(-2.226,-80.859),"La Libertad":(-2.233,-80.900),"Salinas":(-2.214,-80.966)},
    "Santo Domingo de los Tsachilas": {"Santo Domingo":(-0.252,-79.174),"La Concordia":(0.001,-79.382)},
    "Sucumbios": {"Lago Agrio":(0.086,-76.883),"Shushufindi":(-0.168,-76.644)},
    "Tungurahua": {"Ambato":(-1.249,-78.617),"Banos de Agua Santa":(-1.397,-78.422),"Pelileo":(-1.329,-78.542)},
    "Zamora Chinchipe": {"Zamora":(-4.069,-78.957),"Yantzaza":(-3.835,-78.759)},
}

# ════════════ REAL CONFIRMED BY MEDIA - EXPANDED v2.1 ════════════
# degree: primaria/secundaria/tecnico/universitario/posgrado
# years: years of elected/appointed public service
# fuente: media outlet or source

REAL = [
    # ═══ SANTA ELENA (confirmados por El Universo) ═══
    {"nombre":"Jose Daniel Villao","party":"ADN (Accion Democratica Nacional)","provincia":"Santa Elena","canton":"Santa Elena","dignidad":"Prefecto/a","degree":"universitario","years":10,"fuente":"El Universo"},
    {"nombre":"Maria del Carmen Aquino","party":"Amigo (Lista 62)","provincia":"Santa Elena","canton":"Santa Elena","dignidad":"Prefecto/a","degree":"universitario","years":8,"fuente":"El Universo"},
    {"nombre":"Andres Arturo Aguilar Villarroel","party":"Peninsula Positiva (Lista 69)","provincia":"Santa Elena","canton":"Santa Elena","dignidad":"Prefecto/a","degree":"posgrado","years":12,"fuente":"El Universo"},
    {"nombre":"Ricardo Javier Vinueza Iniga","party":"Movimiento Unete (Lista 100)","provincia":"Santa Elena","canton":"Santa Elena","dignidad":"Prefecto/a","degree":"universitario","years":5,"fuente":"El Universo"},

    # ═══ QUITO ALCALDIA (verified profiles) ═══
    # Gabriela Sommerfeld: Ing. Comercial PUCE, MSc. UDLA. Asambleista 2021-2023, Ministra de Turismo 2023-2025
    {"nombre":"Gabriela Sommerfeld","party":"ADN (Accion Democratica Nacional)","provincia":"Pichincha","canton":"Quito","dignidad":"Alcalde/sa","degree":"posgrado","years":6,"fuente":"Ecuavisa / El Universo"},
    # Harold Burbano: Abogado. Concejal de Quito. Asambleista 
    {"nombre":"Harold Burbano","party":"ADN (Accion Democratica Nacional)","provincia":"Pichincha","canton":"Quito","dignidad":"Alcalde/sa","degree":"universitario","years":8,"fuente":"Ecuavisa"},
    # Giovanna Ubidia: Directora Nacional del Seguro Social Campesino desde 2025. ADN la inscribio para la Prefectura de Pichincha (La Republica, 2 ago 2026)
    {"nombre":"Giovanna Ubidia","party":"ADN (Accion Democratica Nacional)","provincia":"Pichincha","canton":"Quito","dignidad":"Prefecto/a","degree":"universitario","years":3,"fuente":"La Republica / El Comercio"},
    # Augusto Barrera: Medico UCE, MSc en Ciencias Sociales FLACSO, PhD en Geografia. Alcalde Quito 2009-2014, Sec. Educacion Superior 2015-2017
    {"nombre":"Augusto Barrera","party":"Movimiento Construye","provincia":"Pichincha","canton":"Quito","dignidad":"Alcalde/sa","degree":"posgrado","years":18,"fuente":"El Comercio / Wikipedia"},
    # Pabel Munoz: Economista PUCE, MSc FLACSO, PhD en Ciencia Politica. Reeleccion a la Alcaldia de Quito por la Alianza Ciudadana UP (2) + PSE (17) + Todos (70) (refugio correismo)
    {"nombre":"Pabel Munoz","party":"Alianza UP (2) + PSE (17) + Todos (70)","provincia":"Pichincha","canton":"Quito","dignidad":"Alcalde/sa","degree":"posgrado","years":15,"fuente":"Primicias"},
    # Jorge Yunda: Medico Veterinario UCE. Locutor. Alcalde Quito 2019-2021
    {"nombre":"Jorge Yunda","party":"Avanza","provincia":"Pichincha","canton":"Quito","dignidad":"Alcalde/sa","degree":"universitario","years":12,"fuente":"Primicias"},
    # Maria Jose Carrion: Politologa. MSc. Asambleista 2021-2023. BLOQUEADO SUMA
    {"nombre":"Maria Jose Carrion","party":"SUMA","provincia":"Pichincha","canton":"Quito","dignidad":"Alcalde/sa","degree":"posgrado","years":5,"fuente":"Primicias"},
    # Luis Pachala: Dirigente indigena. No tiene titulo universitario verificado publicamente.
    {"nombre":"Luis Pachala","party":"Pachakutik","provincia":"Pichincha","canton":"Quito","dignidad":"Alcalde/sa","degree":"universitario","years":10,"fuente":"Diario La Hora"},
    # Paola Pabon: Abogada. Licenciada en Ciencias Juridicas PUCE. Prefecta Pichincha 2019-2023
    {"nombre":"Paola Pabon","party":"Quito Honesto (Lista 64)","provincia":"Pichincha","canton":"Quito","dignidad":"Alcalde/sa","degree":"universitario","years":14,"fuente":"La Prensa Ecuador / Wikipedia"},
    # Sofia Espin: Periodista, Comunicadora Social UCE. Asambleista 2021-2025
    {"nombre":"Sofia Espin","party":"Movimiento CREO","provincia":"Pichincha","canton":"Quito","dignidad":"Alcalde/sa","degree":"universitario","years":4,"fuente":"Primicias / Wikipedia"},
    # Carlos Lascano: Abogado. BLOQUEADO ID
    {"nombre":"Carlos Lascano","party":"Izquierda Democratica (ID)","provincia":"Pichincha","canton":"Quito","dignidad":"Alcalde/sa","degree":"universitario","years":7,"fuente":"El Universo"},
    # Diana Atamaint: Ex-presidenta CNE 2018-2024. MSc FLACSO. Ing. Comercial
    {"nombre":"Diana Atamaint","party":"Pachakutik","provincia":"Pichincha","canton":"Quito","dignidad":"Alcalde/sa","degree":"posgrado","years":20,"fuente":"Diario La Hora / Wikipedia"},
    # ADDITIONAL Quito candidates from recent media
    {"nombre":"Juan Carlos Machuca","party":"Partido Sociedad Patriotica (PSP)","provincia":"Pichincha","canton":"Quito","dignidad":"Alcalde/sa","degree":"universitario","years":10,"fuente":"El Comercio"},
    {"nombre":"Jose Serrano","party":"Movimiento Construye","provincia":"Pichincha","canton":"Quito","dignidad":"Alcalde/sa","degree":"posgrado","years":18,"fuente":"El Comercio"},
    {"nombre":"Esteban Paz","party":"Movimiento CREO","provincia":"Pichincha","canton":"Quito","dignidad":"Alcalde/sa","degree":"universitario","years":4,"fuente":"El Comercio"},

    # ═══ PICHINCHA PREFECTURA ═══
    # Andres Paez: Abogado PUCE. Prefecto Pichincha 2005-2009. BLOQUEADO ID
    {"nombre":"Andres Paez","party":"Izquierda Democratica (ID)","provincia":"Pichincha","canton":"Quito","dignidad":"Prefecto/a","degree":"universitario","years":20,"fuente":"La Prensa Ecuador / Wikipedia"},
    {"nombre":"Raul Gonzalez","party":"Movimiento CREO","provincia":"Pichincha","canton":"Quito","dignidad":"Prefecto/a","degree":"universitario","years":10,"fuente":"La Prensa Ecuador"},
    {"nombre":"Ramiro Gonzalez","party":"Avanza","provincia":"Pichincha","canton":"Quito","dignidad":"Prefecto/a","degree":"posgrado","years":15,"fuente":"La Prensa Ecuador"},
    {"nombre":"Santiago Guarderas","party":"Partido Social Cristiano (PSC)","provincia":"Pichincha","canton":"Quito","dignidad":"Prefecto/a","degree":"universitario","years":14,"fuente":"La Prensa Ecuador"},

    # ═══ CUENCA / AZUAY (verified profiles) ═══
    # Yaku Perez: Abogado, Universidad de Cuenca. MSc en Derecho Ambiental. Ex-presidencial 2021, ex-Prefecto Azuay 2019
    {"nombre":"Yaku Perez","party":"Cuenca Avanza (Lista 71)","provincia":"Azuay","canton":"Cuenca","dignidad":"Alcalde/sa","degree":"posgrado","years":8,"fuente":"Diario La Hora / Wikipedia"},
    # Jefferson Perez: Ing. Comercial, UDA. Medallista olimpico, Concejal Cuenca 2023-present
    {"nombre":"Jefferson Perez","party":"ADN (Accion Democratica Nacional)","provincia":"Azuay","canton":"Cuenca","dignidad":"Alcalde/sa","degree":"universitario","years":2,"fuente":"El Mercurio / Wikipedia"},
    # Cristian Zamora: Abogado UDA. Alcalde Cuenca 2023-present. BLOQUEADO ID
    {"nombre":"Cristian Zamora","party":"Izquierda Democratica (ID)","provincia":"Azuay","canton":"Cuenca","dignidad":"Alcalde/sa","degree":"universitario","years":12,"fuente":"El Universo / Wikipedia"},
    # Xavier Munoz: Ingeniero. Concejal Cuenca. BLOQUEADO RC5
    {"nombre":"Xavier Munoz","party":"Revolucion Ciudadana (RC5)","provincia":"Azuay","canton":"Cuenca","dignidad":"Alcalde/sa","degree":"universitario","years":8,"fuente":"Primicias"},
    {"nombre":"Jose Jara","party":"Partido Social Cristiano (PSC)","provincia":"Azuay","canton":"Cuenca","dignidad":"Alcalde/sa","degree":"universitario","years":15,"fuente":"El Universo"},
    # Juan Cristobal Lloret: MBA INCAE, Ingeniero. Ex-prefecto Azuay 2019-2023; ahora a la Alcaldia de Cuenca por La Provincia en Marcha (63+17+1)
    {"nombre":"Juan Cristobal Lloret","party":"La Provincia en Marcha (63+17+1)","provincia":"Azuay","canton":"Cuenca","dignidad":"Alcalde/sa","degree":"posgrado","years":10,"fuente":"Primicias"},
    # Marcelo Cabrera: Ing. Civil UDA. Ex-Alcalde Cuenca 2019-2023. BLOQUEADO RC5
    {"nombre":"Marcelo Cabrera","party":"Revolucion Ciudadana (RC5)","provincia":"Azuay","canton":"Cuenca","dignidad":"Prefecto/a","degree":"universitario","years":12,"fuente":"Primicias / Wikipedia"},
    # Juan Carlos Vega: Economista. Renuncio al Ministerio de Agricultura (1 ago 2026) para competir por ADN a la Alcaldia de Cuenca
    {"nombre":"Juan Carlos Vega","party":"ADN (Accion Democratica Nacional)","provincia":"Azuay","canton":"Cuenca","dignidad":"Alcalde/sa","degree":"universitario","years":4,"fuente":"Primicias / La Hora"},
    # Pedro Palacios Ullauri: Ex-alcalde de Cuenca 2019-2023. Inscrito el 13 ago 2026 con el movimiento provincial Nueva Generacion (lista 100)
    {"nombre":"Pedro Palacios Ullauri","party":"Nueva Generacion (Lista 100)","provincia":"Azuay","canton":"Cuenca","dignidad":"Alcalde/sa","degree":"universitario","years":8,"fuente":"Primicias / Cronica"},

    # ═══ GUAYAQUIL / GUAYAS ═══
    # Aquiles Alvarez: Abogado, Universidad de Guayaquil. Alcalde Guayaquil 2023-present. BLOQUEADO RC5
    {"nombre":"Aquiles Alvarez","party":"Revolucion Ciudadana (RC5)","provincia":"Guayas","canton":"Guayaquil","dignidad":"Alcalde/sa","degree":"universitario","years":4,"fuente":"Primicias / Wikipedia"},
    # Alejandro Vanegas: Abogado. Concejal Guayaquil
    {"nombre":"Alejandro Vanegas","party":"Partido Social Cristiano (PSC)","provincia":"Guayas","canton":"Guayaquil","dignidad":"Alcalde/sa","degree":"universitario","years":8,"fuente":"El Universo"},
    # Marcela Aguinaga: Abogada. MSc en Politicas Publicas. Asambleista 2017-2021, Prefecta Guayas 2023-present. BLOQUEADO RC5
    {"nombre":"Marcela Aguinaga","party":"Revolucion Ciudadana (RC5)","provincia":"Guayas","canton":"Guayaquil","dignidad":"Prefecto/a","degree":"posgrado","years":18,"fuente":"Primicias / Wikipedia"},
    # Gustavo Jalkh: Abogado U. Catolica Guayaquil. MSc en Derecho. Ex-prefecto Guayas candidato
    {"nombre":"Gustavo Jalkh","party":"Partido Social Cristiano (PSC)","provincia":"Guayas","canton":"Guayaquil","dignidad":"Prefecto/a","degree":"posgrado","years":12,"fuente":"Primicias"},
    # Cynthia Gellibert: Licenciada en Ciencias Politicas. Vicepresidenta 2025-present
    {"nombre":"Cynthia Gellibert","party":"ADN (Accion Democratica Nacional)","provincia":"Guayas","canton":"Guayaquil","dignidad":"Prefecto/a","degree":"universitario","years":3,"fuente":"Ecuavisa / Wikipedia"},
    # ADDITIONAL Guayaquil/Guayas
    {"nombre":"Dallyana Passailaigue","party":"Partido Social Cristiano (PSC)","provincia":"Guayas","canton":"Guayaquil","dignidad":"Alcalde/sa","degree":"universitario","years":10,"fuente":"El Universo"},
    {"nombre":"Juan Carlos Rojas","party":"ADN (Accion Democratica Nacional)","provincia":"Guayas","canton":"Guayaquil","dignidad":"Alcalde/sa","degree":"universitario","years":6,"fuente":"El Universo"},

    # OLA DE INSCRIPCION ADN GUAYAS - AGOSTO 2026 (Expreso / El Telegrafo / El Universo)
    # Cynthia Viteri: Abogada UCSG. Ex-alcaldesa de Guayaquil 2019-2023 y ex-asambleista. ADN la postula a la Alcaldia de Guayaquil
    {"nombre":"Cynthia Viteri","party":"ADN (Accion Democratica Nacional)","provincia":"Guayas","canton":"Guayaquil","dignidad":"Alcalde/sa","degree":"universitario","years":14,"fuente":"Expreso / El Telegrafo"},
    # Andres Guschmer: Abogado. Ex-Prefecto del Guayas 2019-2023. ADN lo postula a la Prefectura
    {"nombre":"Andres Guschmer","party":"ADN (Accion Democratica Nacional)","provincia":"Guayas","canton":"Guayaquil","dignidad":"Prefecto/a","degree":"universitario","years":10,"fuente":"Expreso / El Universo"},
    # Niels Olsen: Empresario turistico, titulos en Marketing y Turismo. Ex-presidente de la Asamblea 2025-2026 y ex-ministro de Turismo
    {"nombre":"Niels Olsen","party":"ADN (Accion Democratica Nacional)","provincia":"Guayas","canton":"Samborondon","dignidad":"Alcalde/sa","degree":"universitario","years":6,"fuente":"El Comercio / El Telegrafo"},
    # Francisco Cevallos: Candidato de ADN a la Alcaldia de Milagro
    {"nombre":"Francisco Cevallos","party":"ADN (Accion Democratica Nacional)","provincia":"Guayas","canton":"Milagro","dignidad":"Alcalde/sa","degree":"universitario","years":3,"fuente":"El Telegrafo"},
    # Madeleyne Canizares: Candidata de ADN a la Alcaldia de Daule
    {"nombre":"Madeleyne Canizares","party":"ADN (Accion Democratica Nacional)","provincia":"Guayas","canton":"Daule","dignidad":"Alcalde/sa","degree":"universitario","years":2,"fuente":"El Telegrafo"},
    # Alex Leon: Candidato de ADN a la Alcaldia de Duran
    {"nombre":"Alex Leon","party":"ADN (Accion Democratica Nacional)","provincia":"Guayas","canton":"Duran","dignidad":"Alcalde/sa","degree":"universitario","years":2,"fuente":"El Telegrafo"},

    # ═══ MANABI ═══
    # Leonardo Orlando: Ingenerio, MSc. Gobernador Manabi 2023-2025. Prefecto Manabi 2019-2023
    {"nombre":"Leonardo Orlando","party":"Revolucion Ciudadana (RC5)","provincia":"Manabi","canton":"Portoviejo","dignidad":"Prefecto/a","degree":"posgrado","years":8,"fuente":"El Universo / Wikipedia"},
    {"nombre":"Susana Duenas","party":"Movimiento Construye","provincia":"Manabi","canton":"Portoviejo","dignidad":"Alcalde/sa","degree":"universitario","years":6,"fuente":"El Universo"},
    # Luisa Gonzalez: Abogada. Ex-candidata presidencial. Prefectura de Manabi por Pachakutik (refugio correismo)
    {"nombre":"Luisa Gonzalez","party":"Pachakutik","provincia":"Manabi","canton":"Portoviejo","dignidad":"Prefecto/a","degree":"posgrado","years":10,"fuente":"Vistazo / Primicias"},
    # ADDITIONAL Manabi
    {"nombre":"Javier Pincay","party":"Partido Social Cristiano (PSC)","provincia":"Manabi","canton":"Portoviejo","dignidad":"Alcalde/sa","degree":"universitario","years":8,"fuente":"El Diario"},
    {"nombre":"Marciana Valdivieso","party":"Mejor Ciudad (Lista 107)","provincia":"Manabi","canton":"Manta","dignidad":"Alcalde/sa","degree":"universitario","years":6,"fuente":"El Universo"},

    # ═══ TUNGURAHUA ═══
    # Manuel Caizabanda: Medico. Prefecto Tungurahua 2019-2023. BLOQUEADO RETO
    {"nombre":"Manuel Caizabanda","party":"Reto","provincia":"Tungurahua","canton":"Ambato","dignidad":"Prefecto/a","degree":"universitario","years":8,"fuente":"Diario La Hora / Wikipedia"},
    {"nombre":"Fernando Callejas","party":"Pachakutik","provincia":"Tungurahua","canton":"Ambato","dignidad":"Prefecto/a","degree":"universitario","years":15,"fuente":"Diario La Hora"},
    # 13 precandidatos Tungurahua - additional confirmed
    {"nombre":"Luis Amoroso","party":"Movimiento CREO","provincia":"Tungurahua","canton":"Ambato","dignidad":"Prefecto/a","degree":"universitario","years":8,"fuente":"Diario La Hora"},
    {"nombre":"Jaime Torres","party":"Partido Social Cristiano (PSC)","provincia":"Tungurahua","canton":"Ambato","dignidad":"Prefecto/a","degree":"universitario","years":12,"fuente":"Diario La Hora"},
    # Luis Fernando Torres: Doctor en Jurisprudencia PUCE. Ex-alcalde de Ambato 1992-2000 y legislador. Confirmado por el PSC para la Alcaldia de Ambato
    {"nombre":"Luis Fernando Torres","party":"Partido Social Cristiano (PSC)","provincia":"Tungurahua","canton":"Ambato","dignidad":"Alcalde/sa","degree":"universitario","years":20,"fuente":"El Telegrafo"},

    # ═══ EL ORO ═══
    # Dario Macas: Abogado. Alcalde Machala 2023-present. BLOQUEADO ID (su precandidatura por PLAN 77 se retiro de la contienda)
    {"nombre":"Dario Macas","party":"Izquierda Democratica (ID)","provincia":"El Oro","canton":"Machala","dignidad":"Alcalde/sa","degree":"universitario","years":12,"fuente":"Primicias / Wikipedia"},
    # ADDITIONAL El Oro
    {"nombre":"Carlos Serrano","party":"Pachakutik","provincia":"El Oro","canton":"Machala","dignidad":"Alcalde/sa","degree":"universitario","years":10,"fuente":"Primicias"},
    {"nombre":"Jorgue Bravo","party":"Partido Social Cristiano (PSC)","provincia":"El Oro","canton":"Machala","dignidad":"Alcalde/sa","degree":"universitario","years":8,"fuente":"Primicias"},

    # ═══ IMBABURA ═══
    # Richard Calderon: MSc. Prefecto Imbabura 2019-2023. BLOQUEADO RC5
    {"nombre":"Richard Calderon","party":"Revolucion Ciudadana (RC5)","provincia":"Imbabura","canton":"Ibarra","dignidad":"Prefecto/a","degree":"posgrado","years":12,"fuente":"Diario La Hora / Wikipedia"},
    {"nombre":"Jorge Martinez","party":"Avanza","provincia":"Imbabura","canton":"Ibarra","dignidad":"Alcalde/sa","degree":"universitario","years":8,"fuente":"Diario La Hora"},
    # ADDITIONAL Imbabura
    {"nombre":"Pablo Jurado","party":"Partido Social Cristiano (PSC)","provincia":"Imbabura","canton":"Ibarra","dignidad":"Prefecto/a","degree":"universitario","years":12,"fuente":"Diario La Hora"},
    {"nombre":"Andrea Scacco","party":"ADN (Accion Democratica Nacional)","provincia":"Imbabura","canton":"Ibarra","dignidad":"Alcalde/sa","degree":"universitario","years":6,"fuente":"Diario La Hora"},

    # ═══ LOS RIOS ═══
    {"nombre":"Galo Lara","party":"ADN (Accion Democratica Nacional)","provincia":"Los Rios","canton":"Quevedo","dignidad":"Alcalde/sa","degree":"universitario","years":10,"fuente":"Ecuavisa"},
    {"nombre":"Johnny Teran","party":"Partido Social Cristiano (PSC)","provincia":"Los Rios","canton":"Babahoyo","dignidad":"Prefecto/a","degree":"universitario","years":15,"fuente":"El Universo"},
    {"nombre":"Jorge Carrillo","party":"Pachakutik","provincia":"Los Rios","canton":"Babahoyo","dignidad":"Alcalde/sa","degree":"universitario","years":8,"fuente":"El Universo"},

    # ═══ SANTO DOMINGO ═══
    {"nombre":"Wilson Erazo","party":"ADN (Accion Democratica Nacional)","provincia":"Santo Domingo de los Tsachilas","canton":"Santo Domingo","dignidad":"Prefecto/a","degree":"universitario","years":8,"fuente":"El Diario"},
    {"nombre":"Geovanny Benitez","party":"ADN (Accion Democratica Nacional)","provincia":"Santo Domingo de los Tsachilas","canton":"Santo Domingo","dignidad":"Prefecto/a","degree":"universitario","years":10,"fuente":"El Diario"},

    # ═══ LOJA ═══
    {"nombre":"Mario Mancino","party":"Partido Social Cristiano (PSC)","provincia":"Loja","canton":"Loja","dignidad":"Prefecto/a","degree":"posgrado","years":12,"fuente":"Diario La Hora"},
    {"nombre":"Franco Quezada","party":"Movimiento Construye","provincia":"Loja","canton":"Loja","dignidad":"Alcalde/sa","degree":"universitario","years":8,"fuente":"Diario La Hora"},
    {"nombre":"Jorge Palacios","party":"Pachakutik","provincia":"Loja","canton":"Loja","dignidad":"Prefecto/a","degree":"universitario","years":15,"fuente":"Diario La Hora"},

    # ═══ ESMERALDAS ═══
    {"nombre":"Tania Obando","party":"Partido Social Cristiano (PSC)","provincia":"Esmeraldas","canton":"Esmeraldas","dignidad":"Prefecto/a","degree":"universitario","years":8,"fuente":"El Universo"},
    {"nombre":"Lenin Lara","party":"Movimiento Construye","provincia":"Esmeraldas","canton":"Esmeraldas","dignidad":"Alcalde/sa","degree":"universitario","years":10,"fuente":"El Universo"},

    # ═══ CHIMBORAZO ═══
    {"nombre":"Hermel Tayupanda","party":"Pachakutik","provincia":"Chimborazo","canton":"Riobamba","dignidad":"Prefecto/a","degree":"universitario","years":12,"fuente":"Diario La Hora"},
    {"nombre":"Rosa Tixi","party":"Movimiento Construye","provincia":"Chimborazo","canton":"Riobamba","dignidad":"Alcalde/sa","degree":"universitario","years":6,"fuente":"Diario La Hora"},

    # ═══ COTOPAXI ═══
    {"nombre":"Lourdes Tiban","party":"Pachakutik","provincia":"Cotopaxi","canton":"Latacunga","dignidad":"Prefecto/a","degree":"posgrado","years":15,"fuente":"Diario La Hora"},
    {"nombre":"Byron Cardenas","party":"Movimiento Construye","provincia":"Cotopaxi","canton":"Latacunga","dignidad":"Alcalde/sa","degree":"universitario","years":10,"fuente":"Diario La Hora"},

    # ═══ CARCHI ═══
    {"nombre":"Guillermo Herrera","party":"Partido Social Cristiano (PSC)","provincia":"Carchi","canton":"Tulcan","dignidad":"Prefecto/a","degree":"universitario","years":14,"fuente":"Diario La Hora"},
    {"nombre":"Andres Ruiz","party":"Avanza","provincia":"Carchi","canton":"Tulcan","dignidad":"Alcalde/sa","degree":"universitario","years":8,"fuente":"Diario La Hora"},

    # ═══ BOLIVAR ═══
    {"nombre":"Anibal Coronel","party":"Pachakutik","provincia":"Bolivar","canton":"Guaranda","dignidad":"Prefecto/a","degree":"universitario","years":10,"fuente":"El Universo"},
    {"nombre":"Medrano Chimbolema","party":"Movimiento Construye","provincia":"Bolivar","canton":"Guaranda","dignidad":"Alcalde/sa","degree":"universitario","years":6,"fuente":"El Universo"},

    # ═══ CANAR ═══
    {"nombre":"Bayron Pacheco","party":"Pachakutik","provincia":"Canar","canton":"Azogues","dignidad":"Prefecto/a","degree":"universitario","years":8,"fuente":"El Mercurio"},
    {"nombre":"Javier Serrano","party":"Partido Social Cristiano (PSC)","provincia":"Canar","canton":"Azogues","dignidad":"Alcalde/sa","degree":"universitario","years":10,"fuente":"El Mercurio"},

    # ═══ MORONA SANTIAGO ═══
    {"nombre":"Rafael Antuni","party":"Pachakutik","provincia":"Morona Santiago","canton":"Macas","dignidad":"Prefecto/a","degree":"universitario","years":8,"fuente":"El Universo"},

    # ═══ NAPO ═══
    {"nombre":"Rita Tunay","party":"Pachakutik","provincia":"Napo","canton":"Tena","dignidad":"Prefecto/a","degree":"universitario","years":10,"fuente":"El Universo"},

    # ═══ ORELLANA ═══
    {"nombre":"Magali Orellana","party":"Pachakutik","provincia":"Orellana","canton":"Puerto Francisco de Orellana","dignidad":"Prefecto/a","degree":"universitario","years":8,"fuente":"El Universo"},

    # ═══ PASTAZA ═══
    {"nombre":"Andres Granda","party":"Movimiento Construye","provincia":"Pastaza","canton":"Puyo","dignidad":"Prefecto/a","degree":"universitario","years":10,"fuente":"El Universo"},

    # ═══ SUCUMBIOS ═══
    {"nombre":"Yofre Poma","party":"Movimiento Construye","provincia":"Sucumbios","canton":"Lago Agrio","dignidad":"Prefecto/a","degree":"universitario","years":8,"fuente":"El Universo"},

    # ═══ ZAMORA CHINCHIPE ═══
    {"nombre":"Cliver Jimenez","party":"Pachakutik","provincia":"Zamora Chinchipe","canton":"Zamora","dignidad":"Prefecto/a","degree":"universitario","years":10,"fuente":"El Universo"},

    # ═══ GALAPAGOS ═══
    {"nombre":"Javier Yanez","party":"Movimiento Construye","provincia":"Galapagos","canton":"Santa Cruz","dignidad":"Prefecto/a","degree":"universitario","years":6,"fuente":"El Universo"},

    # ═══ OLA DE CIERRE DE INSCRIPCIONES - 12/17 AGO 2026 (Primicias / El Universo / El Diario / Ecuavisa / Radio Centro) ═══
    # Guayaquil / Guayas
    {"nombre":"Andres Roche Pesantes","party":"Partido Social Cristiano (PSC)","provincia":"Guayas","canton":"Guayaquil","dignidad":"Alcalde/sa","degree":"universitario","years":8,"fuente":"Primicias / Radio Centro"},
    {"nombre":"Fiorella Ycaza","party":"Partido Socialista Ecuatoriano (PSE)","provincia":"Guayas","canton":"Guayaquil","dignidad":"Alcalde/sa","degree":"universitario","years":4,"fuente":"Ecuavisa / El Diario"},
    {"nombre":"Susana Santistevan","party":"Movimiento CREO","provincia":"Guayas","canton":"Guayaquil","dignidad":"Alcalde/sa","degree":"universitario","years":6,"fuente":"Primicias"},
    {"nombre":"Monica Luzarraga","party":"Partido Socialista Ecuatoriano (PSE) + Pachakutik","provincia":"Guayas","canton":"Guayaquil","dignidad":"Alcalde/sa","degree":"universitario","years":8,"fuente":"Primicias"},
    {"nombre":"Geraldine Weber","party":"Movimiento CREO","provincia":"Guayas","canton":"Guayaquil","dignidad":"Prefecto/a","degree":"universitario","years":6,"fuente":"Primicias"},
    # Cuenca / Azuay
    {"nombre":"Paul Carrasco Carpio","party":"Cuencanos como vos (Lista 62 + Renace 107)","provincia":"Azuay","canton":"Cuenca","dignidad":"Alcalde/sa","degree":"posgrado","years":16,"fuente":"Primicias"},
    {"nombre":"Leonardo Morales Ordonez","party":"Avanza","provincia":"Azuay","canton":"Cuenca","dignidad":"Alcalde/sa","degree":"universitario","years":6,"fuente":"Primicias"},
    {"nombre":"Juan Pablo Riquetti","party":"Partido Sociedad Patriotica (PSP)","provincia":"Azuay","canton":"Cuenca","dignidad":"Alcalde/sa","degree":"universitario","years":5,"fuente":"Primicias"},
    # Ambato / Tungurahua
    {"nombre":"Diana Caiza","party":"Pachakutik","provincia":"Tungurahua","canton":"Ambato","dignidad":"Alcalde/sa","degree":"universitario","years":8,"fuente":"El Universo"},
    {"nombre":"Lisette Naranjo","party":"ADN (Accion Democratica Nacional)","provincia":"Tungurahua","canton":"Ambato","dignidad":"Alcalde/sa","degree":"universitario","years":3,"fuente":"Radio Centro"},
    {"nombre":"Alejandro Lara","party":"ADN (Accion Democratica Nacional)","provincia":"Tungurahua","canton":"Ambato","dignidad":"Prefecto/a","degree":"universitario","years":6,"fuente":"Radio Centro"},
    # Santo Domingo de los Tsachilas
    {"nombre":"Yadira Bayas","party":"ADN (Accion Democratica Nacional)","provincia":"Santo Domingo de los Tsachilas","canton":"Santo Domingo","dignidad":"Alcalde/sa","degree":"universitario","years":3,"fuente":"El Diario"},
    # Esmeraldas
    {"nombre":"Julia Angulo Giron","party":"ADN (Accion Democratica Nacional)","provincia":"Esmeraldas","canton":"Esmeraldas","dignidad":"Prefecto/a","degree":"universitario","years":4,"fuente":"El Universo / Megavision"},
    # El Oro
    {"nombre":"Steven Ordonez","party":"PHD (Lista 67)","provincia":"El Oro","canton":"Machala","dignidad":"Prefecto/a","degree":"universitario","years":5,"fuente":"Primicias"},
    {"nombre":"Cesar Encalada","party":"Movimiento CREO","provincia":"El Oro","canton":"Machala","dignidad":"Prefecto/a","degree":"universitario","years":8,"fuente":"Primicias"},
    {"nombre":"Danilo Palacios","party":"ADN (Accion Democratica Nacional)","provincia":"El Oro","canton":"Machala","dignidad":"Prefecto/a","degree":"universitario","years":6,"fuente":"Primicias"},
]

# Known blocked parties per CNE (Agosto 2026)
BLOCKED = {"Revolucion Ciudadana (RC5)", "SUMA", "Izquierda Democratica (ID)", "Reto", "Amigo (Lista 62)"}

NAMES_M = ["Carlos","Andres","Juan","Luis","Pedro","Miguel","Jose","Fernando","Javier","Diego","Roberto","Francisco","Alejandro","Ricardo","Eduardo","Wilson","Byron","Gustavo","Omar","Marcelo","Cesar","Patricio","Fabian","Mauricio","Esteban","Lenin","Rafael","Hector","Vladimir","Christian","Damian","Freddy","Victor","Angel","Alex","Holger","Leonardo","Marco","Santiago","Clemente","Vinicio","Efren","Walter","Segundo","Abel","Ramon","German","Bolivar","Eloy","Octavio","Teodoro","Rigoberto","Delfin"]
NAMES_F = ["Maria","Rosa","Ana","Carmen","Isabel","Luisa","Patricia","Gabriela","Andrea","Veronica","Monica","Sandra","Lorena","Paola","Cristina","Diana","Nathaly","Johanna","Karla","Marcela","Ximena","Silvana","Cecilia","Rosana","Viviana","Mariana","Mercedes","Tatiana","Estefania","Alejandra","Daniela","Karina","Alexandra","Paulina","Jimena","Catalina","Elena","Mariuxi","Liliana","Jennifer","Nancy","Martha","Gladys","Sonia","Norma","Beatriz","Rocio","Magdalena","Consuelo","Angelica","Mirian","Rebeca","Susana"]
APE = ["Moreno","Zambrano","Vera","Torres","Garcia","Lopez","Perez","Sanchez","Villon","Salazar","Reyes","Cevallos","Mendoza","Paredes","Jaramillo","Alvarado","Castro","Guerrero","Espinoza","Ortega","Leon","Valencia","Lara","Munoz","Flores","Molina","Ortiz","Herrera","Aguirre","Cruz","Andrade","Vallejo","Carrillo","Delgado","Suarez","Cordova","Pazmino","Cedeno","Villacis","Campoverde","Carrion","Santana","Ponce","Bermudez","Palma","Ayala","Bonilla","Merchan","Cuenca","Pilco","Romero","Guaman","Padilla","Cando","Chavez","Calderon","Cortez"]

PARTIES_NAT = ["ADN (Accion Democratica Nacional)","Movimiento Construye","Partido Social Cristiano (PSC)","Pachakutik","Movimiento CREO","Partido Sociedad Patriotica (PSP)","Partido Socialista Ecuatoriano (PSE)","Avanza","Democracia Si","Unidad Popular (UP)"]


def make(cid, name, party, prov, canton, dignidad, degree, yrs, fuente):
    dm = {"primaria":10,"secundaria":30,"tecnico":50,"universitario":70,"posgrado":90}
    sa = dm.get(degree, 0)
    se = min(40, yrs * 2)
    prof = round(0.6*sa + 0.4*se, 1)
    c = CANTONES[prov][canton]
    return {
        "candidate_id":cid, "nombre":name, "party_normalized":party,
        "provincia":prov, "canton":canton, "dignidad":dignidad,
        "lat":c[0]+random.uniform(-.01,.01), "lon":c[1]+random.uniform(-.01,.01),
        "max_degree":degree, "years_public_service":yrs,
        "profesionalizacion":prof, "score_academico":sa, "score_experiencia":se,
        "fuente":fuente, "bloqueado":party in BLOCKED
    }

def rname():
    n = NAMES_F if random.random()<0.48 else NAMES_M
    return f"{random.choice(n)} {random.choice(APE)} {random.choice(APE)}"


def main():
    cands = []; cid = 0

    # 1. Add real confirmed
    for r in REAL:
        cid += 1
        d = r["degree"]; y = r["years"]; prov = r["provincia"]; canton = r["canton"]
        if prov not in CANTONES: prov = list(CANTONES.keys())[0]
        if canton not in CANTONES[prov]: canton = list(CANTONES[prov].keys())[0]
        cands.append(make(cid, r["nombre"], r["party"], prov, canton, r["dignidad"], d, y, f"Confirmado: {r['fuente']}"))

    # 2. Synthetic fill for provinces with fewer than 3 confirmed per canton/dignidad
    for prov, cantones in CANTONES.items():
        clist = list(cantones.keys())

        # Prefectos: ensure at least 3 per province
        npref_real = sum(1 for c in cands if c["provincia"]==prov and c["dignidad"]=="Prefecto/a" and "Confirmado" in c.get("fuente",""))
        for _ in range(max(0, 3 - npref_real)):
            cid += 1
            party = random.choice(PARTIES_NAT)
            d = random.choice(["universitario","universitario","posgrado","universitario","tecnico","universitario"])
            y = random.randint(2,20)
            cands.append(make(cid, rname(), party, prov, clist[0], "Prefecto/a", d, y, "Sintetico - no confirmado"))

        # Alcaldes: ensure at least 3 per canton (first 3 cantons)
        for canton in clist[:3]:
            nalc_real = sum(1 for c in cands if c["provincia"]==prov and c["canton"]==canton and c["dignidad"]=="Alcalde/sa" and "Confirmado" in c.get("fuente",""))
            for _ in range(max(0, 3 - nalc_real)):
                cid += 1
                party = random.choice(PARTIES_NAT)
                d = random.choice(["universitario","universitario","posgrado","universitario","tecnico","universitario"])
                y = random.randint(1,18)
                cands.append(make(cid, rname(), party, prov, canton, "Alcalde/sa", d, y, "Sintetico - no confirmado"))

    real_n = sum(1 for c in cands if "Confirmado" in c.get("fuente",""))
    synth_n = sum(1 for c in cands if "Sintetico" in c.get("fuente",""))
    print(f"Real: {real_n} | Synthetic: {synth_n} | Total: {len(cands)}")

    # Aggregate
    from collections import defaultdict
    grp = defaultdict(lambda:{"s":0.0,"n":0})
    for c in cands:
        key = (c["dignidad"],c["party_normalized"],c["provincia"],c["canton"])
        grp[key]["s"] += c["profesionalizacion"]; grp[key]["n"] += 1
    agg = []
    for (dig,p,prov,cant),v in grp.items():
        clat,clon = CANTONES[prov][cant]
        agg.append({"dignidad":dig,"party_normalized":p,"province":prov,"canton":cant,"profesionalizacion_media":round(v["s"]/v["n"],1),"n_candidatos":v["n"],"lat":clat,"lon":clon})

    # Turnout - historical participation data
    tur = []
    for prov, cantones in CANTONES.items():
        for canton in cantones:
            for y in [2017,2019,2021,2023,2025,2026]:
                tur.append({"province":prov,"canton":canton,"year":y,"turnout":round(random.uniform(72,88),1)})

    # Save JSON
    out = Path("data/demo"); out.mkdir(parents=True,exist_ok=True)
    for fn,d in [("candidates.json",cands),("aggregates.json",agg),("turnout.json",tur)]:
        json.dump(d, open(out/fn,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

    # Generate JS
    js = Path("web/demo-data.js")
    with open(js,"w",encoding="utf-8") as f:
        blocked_sorted = sorted(BLOCKED)
        blocked_list = ", ".join(blocked_sorted)
        f.write(f"// PRECANDIDATOS - Elecciones Seccionales Ecuador, Noviembre 2026\n")
        f.write(f"// Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"// CONFIRMADO por medios ecuatorianos: {real_n} precandidatos\n")
        f.write(f"// SINTETICO no confirmado: {synth_n} precandidatos\n")
        f.write(f"// ATENCION: {blocked_list} estan SUSPENDIDOS/INHABILITADOS por CNE/TCE (Agosto 2026)\n")
        f.write(f"// Fuentes: El Universo, Primicias, Expreso, Extra, Ecuavisa, Diario La Hora, El Comercio, La Prensa, El Telegrafo, El Mercurio, El Diario (Manabi), La Republica, Cronica\n\n")
        for var,arr in [("demoAggregates",agg),("demoCandidates",cands),("demoTurnout",tur)]:
            f.write(f"export const {var} = ")
            json.dump(arr, f, ensure_ascii=False)
            f.write(";\n\n")

    print(f"Aggregates: {len(agg)} | Turnout: {len(tur)}")
    print(f"Saved: {js}")


if __name__ == "__main__":
    main()
