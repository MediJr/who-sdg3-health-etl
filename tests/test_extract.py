"""Tests unitaires de l'extraction (sans appel réseau : la session HTTP est simulée)."""

import pytest

from src.extract import _write_atomic, build_session, fetch_odata, read_raw


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self.payload


class FakeSession:
    """Session HTTP simulée : renvoie des réponses préparées à l'avance, dans l'ordre."""
    def __init__(self, payloads):
        self.payloads = list(payloads)
        self.calls = []

    def get(self, url, params=None, timeout=None):
        self.calls.append(url)
        return FakeResponse(self.payloads.pop(0))


def test_pagination_odata_suivie_jusqu_a_la_derniere_page():
    session = FakeSession([
        {"value": [{"id": 1}, {"id": 2}], "@odata.nextLink": "https://exemple/page2"},
        {"value": [{"id": 3}]},
    ])
    result = fetch_odata(session, "https://exemple/page1")
    assert result["record_count"] == 3
    assert session.calls == ["https://exemple/page1", "https://exemple/page2"]


def test_structure_inattendue_fait_echouer_explicitement():
    """Mieux vaut planter que charger n'importe quoi si l'API change de format."""
    with pytest.raises(ValueError, match="value"):
        fetch_odata(FakeSession([{"error": "maintenance"}]), "https://exemple")


def test_ecriture_atomique_relisible_et_sans_fichier_temporaire(tmp_path):
    path = tmp_path / "lot" / "indicateur.json.gz"
    _write_atomic(path, {"value": [{"pays": "Sénégal"}]})
    assert read_raw(path) == {"value": [{"pays": "Sénégal"}]}
    assert list(path.parent.iterdir()) == [path]


def test_reessais_uniquement_sur_les_erreurs_temporaires():
    retry = build_session().get_adapter("https://").max_retries
    assert {429, 500, 502, 503, 504} <= set(retry.status_forcelist)
    assert 404 not in retry.status_forcelist, "une page introuvable ne le deviendra pas en réessayant"
    assert retry.respect_retry_after_header
