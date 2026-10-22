"""Tests unitaires de la transformation et des contrôles de qualité (sans base de données)."""

import pytest

from src.transform import BUSINESS_KEY, flatten_observation, validate_observations


def test_echantillon_reel_entierement_valide(transform_result):
    assert len(transform_result.observations) == 8
    assert transform_result.quarantine == []


def test_cle_metier_distingue_les_quintiles_de_richesse(transform_result):
    """Le piège du brief client : 8 valeurs pour un même pays et une même année.
    Elles ne sont PAS des doublons, car le quintile de richesse fait partie du grain."""
    observations = transform_result.observations
    assert observations[BUSINESS_KEY].drop_duplicates().shape[0] == 8
    assert set(observations["wealth_quintile"]) >= {"WEALTHQUINTILE_WQ1", "WEALTHQUINTILE_WQ5"}


def test_ventilations_rangees_par_type_et_non_par_position(sample):
    """Si l'OMS place le sexe en Dim2 au lieu de Dim1, il doit quand même aller dans la colonne « sex »."""
    record = sample["observations"][0]
    record["Dim1Type"], record["Dim2Type"] = record["Dim2Type"], record["Dim1Type"]
    record["Dim1"], record["Dim2"] = record["Dim2"], record["Dim1"]
    row = flatten_observation(record)
    assert row["sex"].startswith("SEX_")
    assert row["age_group"].startswith("AGEGROUP_")


@pytest.mark.parametrize("modification, motif_attendu", [
    ({"NumericValue": None}, "valeur absente ou non numérique"),
    ({"NumericValue": 1500.0, "Low": None, "High": None}, "hors bornes de vraisemblance"),
    ({"Low": 80.0}, "intervalle d'incertitude incohérent"),
    ({"SpatialDim": "XXX"}, "lieu absent du référentiel"),
    ({"TimeDim": 1850}, "année invalide"),
    ({"IndicatorCode": "INCONNU_001"}, "indicateur hors référentiel"),
    ({"Dim3Type": "EDUCATIONLEVEL", "Dim3": "EDU_PRIMARY"}, "type de ventilation inconnu"),
    ({"Dim1": "SEX_INEXISTANT"}, "ventilation absente du référentiel"),
])
def test_ligne_invalide_mise_en_quarantaine_avec_son_motif(sample, reference, modification, motif_attendu):
    locations, breakdowns = reference
    sample["observations"][0].update(modification)
    valid, quarantine = validate_observations(sample["observations"], locations, breakdowns)
    assert len(valid) == 7, "les 7 autres lignes doivent rester valides"
    assert len(quarantine) == 1
    assert motif_attendu in quarantine[0]["reason"]
    assert quarantine[0]["raw_record"] == sample["observations"][0], "la ligne d'origine doit être conservée telle quelle"


def test_doublon_de_cle_metier_mis_en_quarantaine(sample, reference):
    locations, breakdowns = reference
    sample["observations"].append(dict(sample["observations"][0]))
    valid, quarantine = validate_observations(sample["observations"], locations, breakdowns)
    assert len(valid) == 8
    assert [q["reason"] for q in quarantine] == ["doublon de clé métier"]


def test_aucune_ligne_perdue_en_silence(sample, reference):
    """Invariant fondamental : valides + quarantaine = lignes extraites."""
    locations, breakdowns = reference
    sample["observations"][1]["NumericValue"] = None
    sample["observations"][2]["SpatialDim"] = "XXX"
    valid, quarantine = validate_observations(sample["observations"], locations, breakdowns)
    assert len(valid) + len(quarantine) == len(sample["observations"])
