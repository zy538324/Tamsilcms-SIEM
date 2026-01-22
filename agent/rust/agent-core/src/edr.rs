#[derive(Debug, Clone)]
pub struct DetectionSummary {
    pub detection_id: String,
    pub severity: u8,
    pub rule_id: String,
}

pub fn evaluate_rules() -> Vec<DetectionSummary> {
    // TODO: Evaluate behavioural rules in Rust and emit detection summaries.
    vec![DetectionSummary {
        detection_id: "detection-placeholder".to_string(),
        severity: 0,
        rule_id: "rule-placeholder".to_string(),
    }]
}
