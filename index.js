import { spawn } from "child_process";
const python = spawn("python", ["./test.py", 10]);

python.stdout.on("data", (data) => {
  const eventIDs = data.toString().split(",");
  console.log(eventIDs);
});

python.on("close", (code) => {
  console.log("child process exited with code ", code);
});
