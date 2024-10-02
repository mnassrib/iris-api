import numpy as np

def validate_input(data):
    if not data or 'features' not in data:
        return False, "Les données doivent contenir la clé 'features'."
    
    features = data['features']
    
    if not isinstance(features, list) or len(features) != 4:
        return False, "Les 'features' doivent être une liste de 4 éléments."
    
    try:
        # Convertir en tableau numpy pour s'assurer qu'il n'y a que des valeurs numériques
        np.array(features, dtype=float)
    except ValueError:
        return False, "Les 'features' doivent être des valeurs numériques."
    
    return True, None
