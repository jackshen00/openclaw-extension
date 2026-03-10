importScripts('api.js');

const WORKER_ID = "local-xhs-worker-" + Math.floor(Math.random() * 1000);
const PLATFORM = "xhs";
let isPolling = false;

console.log(`Worker ${WORKER_ID} started`);

async function runWorker() {
  if (isPolling) return;
  isPolling = true;

  try {
    const task = await pollTask(WORKER_ID, PLATFORM);
    if (task) {
      console.log("New task received:", task);
      await executeTask(task);
    }
  } catch (error) {
    console.error("Worker cycle error:", error);
  } finally {
    isPolling = false;
  }
}

async function executeTask(task) {
  console.log(`Executing ${task.type} for ${task.target_url}`);
  
  // 1. Update status
  await updateTaskStatus(task.task_id, "opening_page");

  // 2. Open page
  const tab = await chrome.tabs.create({ url: task.target_url, active: true });
  
  // 3. Wait for content script to be ready (placeholder)
  // In real scenario, we'd use message passing
  setTimeout(async () => {
    await updateTaskStatus(task.task_id, "parsing");
    
    // Simulate parsing and report success
    const mockResult = {
      title: "Parsed Title",
      content: "This is a placeholder for actual parsed content."
    };
    
    await reportTaskResult(task.task_id, mockResult);
    console.log(`Task ${task.task_id} completed`);
    
    // Optional: close tab
    // chrome.tabs.remove(tab.id);
  }, 5000);
}

// Start polling every 10 seconds
setInterval(runWorker, 10000);
runWorker();
