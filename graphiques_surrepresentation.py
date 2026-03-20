from matplotlib import pyplot as plt

def plot_surrepresentation(candidat, score_departements, n=5):
    """
    Affiche un graphique des principales surreprésentations
    (en valeur absolue) par département pour un candidat donné.

    Paramètres:
        candidat (str): Nom exact du candidat
        score_departements (DataFrame): DataFrame avec les colonnes
                                        'candidat', 'code_departement', 'surrepresentation'
        n (int): Nombre de départements à afficher (défaut: 5)
    """
    df_candidat = score_departements[score_departements['candidat'] == candidat].copy()

    df_candidat['code_departement'] = df_candidat['code_departement'].astype(str).str.zfill(2)

    df_top = df_candidat.reindex(
        df_candidat['surrepresentation'].abs().nlargest(n).index
    )

    df_top = df_top.sort_values('surrepresentation')

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(
        df_top['code_departement'],
        df_top['surrepresentation'],
        color='steelblue'
    )

    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_xlabel('Surreprésentation')
    ax.set_ylabel('Département')
    ax.set_title(f'Top {n} des surreprésentations de {candidat}')

    plt.tight_layout()
    plt.show()

def plot_carte_surrepresentation(candidat, score_departements, departement_borders):
    """
    Affiche une carte choroplèthe de la surreprésentation par département
    pour un candidat donné.
    
    Paramètres:
        candidat (str): Nom exact du candidat
        score_departements (DataFrame): DataFrame avec les colonnes
                                        'candidat', 'code_departement', 'surrepresentation'
        departement_borders (GeoDataFrame): Fond de carte des départements
    """
    df_candidat = score_departements[score_departements['candidat'] == candidat].copy()

    df_candidat = df_candidat[~df_candidat['code_departement'].isin(['fr_etranger'])]
    df_candidat['code_departement'] = df_candidat['code_departement'].astype(str).str.zfill(2)

    carte = departement_borders.merge(
        df_candidat[['code_departement', 'surrepresentation']],
        left_on='INSEE_DEP', 
        right_on='code_departement',
        how='left'
    )

    carte['surrepresentation'] = carte['surrepresentation']

    fig, ax = plt.subplots(figsize=(10, 10))

    carte.plot(
        column='surrepresentation',
        cmap='RdBu_r',       
        legend=True,
        legend_kwds={'label': '(% par rapport\nmoyenne nationale)'},
        ax=ax,
        missing_kwds={'color': 'lightgrey'}
    )

    ax.set_title(f'Surreprésentation de {candidat} par département')
    ax.axis('off')

    plt.tight_layout()
    plt.show()