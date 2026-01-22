#[derive(Debug, Clone)]
pub struct EvidenceRecord {
    pub evidence_id: String,
    pub sha256: String,
}

pub fn package_evidence() -> EvidenceRecord {
    // TODO: Bundle artefacts, hash contents, and store immutable references.
    EvidenceRecord {
        evidence_id: "evidence-placeholder".to_string(),
        sha256: "sha256-placeholder".to_string(),
    }
}
