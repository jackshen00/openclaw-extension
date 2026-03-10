const API_BASE = "http://localhost:8000";

async function pollTask(workerId, platform) {
  try {
    const response = await fetch(`${API_BASE}/tasks/poll`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        worker_id: workerId,
        platform: platform,
        capabilities: ["profile_parse", "note_parse"]
      })
    });
    if (response.status === 200) {
      return await response.json();
    }
    return null;
  } catch (error) {
    console.error("Polling error:", error);
    return null;
  }
}

async function updateTaskStatus(taskId, status) {
  try {
    await fetch(`${API_BASE}/tasks/${taskId}/status`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: status })
    });
  } catch (error) {
    console.error("Status update error:", error);
  }
}

async function reportTaskResult(taskId, result) {
  try {
    await fetch(`${API_BASE}/tasks/${taskId}/result`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ result: result })
    });
  } catch (error) {
    console.error("Result reporting error:", error);
  }
}
