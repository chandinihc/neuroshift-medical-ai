from app import generate_privacy_deletion_certificate


def test_generate_privacy_deletion_certificate_contains_required_fields():
    cert = generate_privacy_deletion_certificate(
        patient_name="Aisha Khan",
        hospital_name="NeuroShift Medical Center",
        deleted_by="Admin001",
        deleted_on="2026-09-28",
    )

    assert "Aisha Khan" in cert
    assert "NeuroShift Medical Center" in cert
    assert "DELETED" in cert.upper()
    assert "will not be used" in cert.lower()
    assert "seal" in cert.lower() or "official hospital seal" in cert.lower()
