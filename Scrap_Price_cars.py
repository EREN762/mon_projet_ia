import pandas as pd # manipulation et analyse de donnée
import numpy as np # calcule sur les matrices
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import pickle


#charger les données à partir 'un fichier csv
data = pd.read_csv('scrap_price.csv')


#afficher les info du fichier pour une analyse
#print(data.info())
#-----------------NETTOYAGE DES DONNEES
# Extraire uniquement la marque depuis la colonne "name" (ex: "Toyota Corolla" → "Toyota")
#data["marque"] = data["name"].apply(lambda x: x.split()[0])  # Garde seulement le premier mot

#Suppression des colonnes non pertinentes
colones_a_supprimer = ['ID','aspiration','doornumbers','enginelocation',"name","symboling","boreratio"]
data = data.drop(columns=colones_a_supprimer)
# Vérifier les changements
#print(data.info())  # Vérifie que les colonnes ont bien été supprimées et que "marque" existe
#print(data.head())  # Affiche les 5 premières lignes

#------------------------TRANSFORMER LES VARIABLES CATEGORIQUES EN NOMBRES
# Identification des colonnes catégoriques
colonnes_categoriques = [ "fueltypes", "carbody", "drivewheels", "enginetype", "cylindernumber", "fuelsystem"]
# Convertir les variables catégoriques en variables numériques (One-Hot Encoding)
data = pd.get_dummies(data, columns=colonnes_categoriques, drop_first=True)

#-----------------------------NETTOYAGE DES DONNEES
# 1️ Vérifier s’il y a des valeurs manquantes
data.isnull().sum()
# - Option 1 : Supprimer les lignes avec des valeurs manquantes
data = data.dropna()


#--------------------------SEPARERATION DES DONNEES POUR L'ENTRAINEMENT
# 1️⃣ Séparer les features (X) et la target (y)
X= data.drop(columns=['price']) # On enlève la colonne "price" qui est la cible
y=data['price'] # La colonne cible


# 2️⃣ Diviser les données en train (80%) et test (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# # Vérifier les tailles des ensembles
# print(f" Nombre d'échantillons d'entraînement : {X_train.shape[0]}")
# print(f" Nombre d'échantillons de test : {X_test.shape[0]}")


#--------------------ENTRAINEMENT DU MODELE -------------------------------------
model =  RandomForestRegressor(n_estimators=100, random_state=42)
# Entraîner le modèle sur les données d'entraînement
model.fit(X_train,y_train)
#------------------------PREDICTION-------------------------------------------
# Prédire les prix pour les données de test
y_pred = model.predict(X_test)
# 4️⃣ Évaluer la performance du modèle
mae = mean_absolute_error(y_test, y_pred)  # Erreur absolue moyenne
mse = mean_squared_error(y_test, y_pred)  # Erreur quadratique moyenne
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)  # Score R² (coefficient de détermination)

# 5️⃣ Afficher les résultats
print(" Évaluation du modèle :")
print(f" Mean Absolute Error (MAE) : {mae:.2f}")
print(f" Mean Squared Error (MSE) : {mse:.2f}")
print(f" Root Mean Squared Error (RMSE) : {rmse:.2f}")
print(f" R² Score : {r2:.4f}")  # Plus proche de 1, mieux c'est !

import pickle

# Sauvegarder le modèle
with open("modele_voiture.pkl", "wb") as file:
    pickle.dump(model, file)

print(" Modèle sauvegardé avec succès !")


