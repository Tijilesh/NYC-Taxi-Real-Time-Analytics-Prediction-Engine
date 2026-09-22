const API_BASE = "http://127.0.0.1:8000/api";

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function fetchAnalyticsOverview() {
  const res = await fetch(`${API_BASE}/analytics/overview`);
  return res.json();
}

export async function fetchDataQualitySummary() {
  const res = await fetch(`${API_BASE}/data-quality/summary`);
  return res.json();
}

export async function fetchStreamingStatus() {
  const res = await fetch(`${API_BASE}/streaming/status`);
  return res.json();
}

export async function triggerPipelineRun(sampleSize = 5000) {
  const res = await fetch(`${API_BASE}/pipeline/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sample_size: sampleSize })
  });
  return res.json();
}

export async function uploadDatasetFile(formData) {
  const res = await fetch(`${API_BASE}/pipeline/upload`, {
    method: "POST",
    body: formData
  });
  return res.json();
}

export async function fetchPipelineManifest() {

  const res = await fetch(`${API_BASE}/pipeline/manifest`);
  return res.json();
}

export async function fetchPipelineLineage() {
  const res = await fetch(`${API_BASE}/pipeline/lineage`);
  return res.json();
}

export async function predictTaxiDemand(zoneId, targetDatetime) {
  const res = await fetch(`${API_BASE}/prediction/demand`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      zone_id: Number(zoneId),
      target_datetime: targetDatetime || null
    })
  });
  return res.json();
}
