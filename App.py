import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Charger le modèle sauvegardé
with open("modele_voiture.pkl", "rb") as file:
    model = pickle.load(file)

# Colonnes attendues par le modèle
colonnes_model = [
    "wheelbase", "carlength", "carwidth", "carheight", "curbweight", "enginesize", "stroke",
    "compressionratio", "horsepower", "peakrpm", "citympg", "highwaympg",
    "fueltypes_gas", "carbody_hardtop", "carbody_hatchback", "carbody_sedan",
    "carbody_wagon", "drivewheels_fwd", "drivewheels_rwd", "enginetype_dohcv",
    "enginetype_l", "enginetype_ohc", "enginetype_ohcf", "enginetype_ohcv",
    "enginetype_rotor", "cylindernumber_five", "cylindernumber_four", 
    "cylindernumber_six", "cylindernumber_three", "cylindernumber_twelve",
    "cylindernumber_two", "fuelsystem_2bbl", "fuelsystem_4bbl", "fuelsystem_idi",
    "fuelsystem_mfi", "fuelsystem_mpfi", "fuelsystem_spdi", "fuelsystem_spfi"
]

# Interface utilisateur
st.title("🚗 Prédiction du Prix d'une Voiture")
st.write("Entrez les caractéristiques du véhicule et obtenez une estimation du prix.")

# 🛢️ Type de carburant
fueltypes = st.selectbox("Type de carburant ℹ️", ["Essence", "Diesel"],
                         help="Essence : Moins cher mais consomme plus.\nDiesel : Plus économique mais entretien plus coûteux.")

# 🚗 Type de carrosserie
carbody = st.selectbox("Type de carrosserie ℹ️", ["Coupé", "Compacte", "Berline", "Break"],
                        help="🔹 **Coupé** : Toit rigide, 2 portes.\n🔹 **Compacte** : Petite, économique.\n🔹 **Berline** : 4 portes, confortable.\n🔹 **Break** : Plus grand espace de chargement.")

# 🔧 Type de traction
drivewheels = st.selectbox("Type de traction ℹ️", ["Traction avant", "Propulsion", "4x4"],
                            help="🔹 **Traction avant (FWD)** : Économique, stable.\n🔹 **Propulsion (RWD)** : Sportif, mais moins stable.\n🔹 **4x4 (AWD/4WD)** : Meilleure adhérence sur routes difficiles.")

# 🏎️ Type de moteur
enginetype = st.selectbox("Type de moteur ℹ️", ["DOHC", "Ligne", "OHC", "OHCF", "OHCV", "Rotatif"],
                           help="🔹 **DOHC** : Double arbre à cames, plus puissant.\n🔹 **Ligne (L)** : Cylindres alignés.\n🔹 **OHC / OHCF / OHCV** : Simples arbres à cames.\n🔹 **Rotatif** : Technologie spéciale (Mazda).")

# 🔢 Nombre de cylindres
cylindernumber = st.selectbox("Nombre de cylindres ℹ️", ["2", "3", "4", "5", "6", "12"],
                               help="Plus de cylindres = Plus de puissance, mais consomme plus.\n🔹 **2 ou 3** : Petites voitures.\n🔹 **4** : Standard.\n🔹 **6** : Sportives & SUV.\n🔹 **12** : Supercars !")

# ⛽ Système de carburant
fuelsystem = st.selectbox("Système de carburant ℹ️", ["Injection MPFI", "Carburateur 2 corps", "Carburateur 4 corps", "Injection directe (IDI)"],
                           help="🔹 **MPFI** : Injection multi-points (moderne, précis).\n🔹 **Carburateur 2/4 corps** : Ancien système.\n🔹 **IDI** : Injection directe pour Diesel.")

# 🔍 Caractéristiques techniques (Sliders)
wheelbase = st.slider("Empattement (cm)", 80, 140, 100)
carlength = st.slider("Longueur du véhicule (cm)", 140, 220, 180)
carwidth = st.slider("Largeur du véhicule (cm)", 60, 90, 70)
carheight = st.slider("Hauteur du véhicule (cm)", 40, 80, 50)
curbweight = st.slider("Poids à vide (kg)", 500, 2500, 1500)
enginesize = st.slider("Taille du moteur (cm³)", 500, 5000, 2000)
stroke = st.slider("Course du piston", 2.0, 5.0, 3.5)
compressionratio = st.slider("Ratio de compression", 5.0, 25.0, 10.0)
horsepower = st.slider("Puissance (ch)", 50, 400, 150)
peakrpm = st.slider("Régime max (rpm)", 4000, 8000, 5500)
citympg = st.slider("Consommation en ville (mpg)", 5, 60, 30)
highwaympg = st.slider("Consommation sur autoroute (mpg)", 5, 60, 40)

# Préparer les entrées sous forme de dictionnaire
input_data = {
    "wheelbase": wheelbase, "carlength": carlength, "carwidth": carwidth, 
    "carheight": carheight, "curbweight": curbweight, "enginesize": enginesize, 
    "stroke": stroke, "compressionratio": compressionratio, "horsepower": horsepower,
    "peakrpm": peakrpm, "citympg": citympg, "highwaympg": highwaympg
}

# Encoder les variables catégoriques
input_data["fueltypes_gas"] = 1 if fueltypes == "Essence" else 0
input_data["carbody_" + carbody.lower()] = 1
input_data["drivewheels_" + drivewheels.lower()] = 1
input_data["enginetype_" + enginetype.lower()] = 1
input_data["cylindernumber_" + cylindernumber] = 1
input_data["fuelsystem_" + fuelsystem.lower().replace(" ", "_")] = 1

# Convertir en DataFrame
input_df = pd.DataFrame([input_data])

# Ajouter les colonnes manquantes avec des zéros
for col in colonnes_model:
    if col not in input_df.columns:
        input_df[col] = 0

# Réorganiser les colonnes
input_df = input_df[colonnes_model]

# Bouton pour faire la prédiction
if st.button(" Prédire le Prix"):
    prix_estime = model.predict(input_df)
    st.success(f" Prix estimé : {prix_estime[0]:,.2f} $")
