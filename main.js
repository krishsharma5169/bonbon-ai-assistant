const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");
const path = require("path");

let pythonProcess = null;

function startBackend() {

  const pythonPath = "C:\\Users\\deads\\AppData\\Local\\Python\\bin\\python.exe";

  const rootPath = app.isPackaged
    ? path.join(process.resourcesPath, "app.asar.unpacked")
    : __dirname;

  console.log("Root path:", rootPath);

  pythonProcess = spawn(pythonPath, [
    "-m",
    "uvicorn",
    "backend.main:app",
    "--host",
    "127.0.0.1",
    "--port",
    "8000"
  ], {
    cwd: rootPath
  });

  pythonProcess.stdout.on("data", (data) => {
    console.log(`PYTHON: ${data}`);
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`PYTHON ERROR: ${data}`);
  });

  pythonProcess.on("close", (code) => {
    console.log(`Python exited with code ${code}`);
  });
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    backgroundColor: "#0f172a"
  });

  // Give backend time to start
  setTimeout(() => {
    win.loadURL("http://127.0.0.1:8000");
  }, 2000);
}

app.whenReady().then(() => {
  startBackend();
  createWindow();
});

app.on("window-all-closed", () => {
  if (pythonProcess) pythonProcess.kill();
  if (process.platform !== "darwin") app.quit();
});