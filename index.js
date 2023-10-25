// import express JS module into app
// and creates its variable.
import express from "express";
import { spawn } from "child_process";
let app = express();

app.listen(3000, function () {
  console.log("server running on port 3000");
});

app.get("/", callName);

function callName(req, res) {
  let process = spawn("python", ["./env/venv/crawler.py", req.query.page]);
  let result = "";
  process.stdout.on("data", function (data) {
    result = data.toString();
    console.log(result);
  });

  pythonProcess.stdout.on("end", () => {
    try {
      console.log(JSON.parse(result));
    } catch (e) {
      console.log(result);
    }
  });
}

// save code as start.js
