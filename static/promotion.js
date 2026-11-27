// AI assistance: ChatGPT helped display live Stream Analytics results.
function displayResults(id, rows, columns, emptyMessage) {
  const body = document.getElementById(id);
  const fragment = document.createDocumentFragment();
  for (const result of rows) {
    const row = document.createElement("tr");
    for (const column of columns) {
      row.insertCell().textContent = result[column];
    }
    fragment.append(row);
  }
  if (!rows.length) {
    const row = document.createElement("tr");
    const cell = row.insertCell();
    cell.colSpan = columns.length;
    cell.textContent = emptyMessage;
    fragment.append(row);
  }
  body.replaceChildren(fragment);
}

async function refreshPromotion() {
  const status = document.getElementById("promotion-status");
  try {
    const response = await fetch("/api/promotion", {cache: "no-store"});
    if (!response.ok) throw new Error("Unavailable");
    const results = await response.json();
    displayResults("promotion-traffic", results.traffic, ["window_end", "device", "event_count"], "Waiting for device traffic.");
    displayResults("promotion-alerts", results.alerts, ["alert_time", "click_count"], "No spike alerts received yet.");
    status.textContent = "";
  } catch {
    status.textContent = "Analytics refresh failed. Retrying in ten seconds.";
  } finally {
    setTimeout(refreshPromotion, 10000);
  }
}
refreshPromotion();
