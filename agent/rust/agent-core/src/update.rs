#[derive(Debug, Clone)]
pub struct UpdatePlan {
    pub manifest_version: String,
}

pub fn stage_update() -> UpdatePlan {
    // TODO: Verify signed manifest, stage payloads, and prepare rollback metadata.
    UpdatePlan {
        manifest_version: "manifest-placeholder".to_string(),
    }
}
