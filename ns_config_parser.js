var express = require("express");
var app = express();
var handlebars = require("express-handlebars").create({
    defaultLayout: "main"
});
var bodyParser = require("body-parser");
var spawnSync = require("child_process").spawnSync;

app.use(bodyParser.text());
app.use(express.static("public"));

app.engine("handlebars", handlebars.engine);
app.set("view engine", "handlebars");
let port = process.env.PORT || 34567;

//
// Get Current Table
//
app.get("/", function(req, res, next) {
    context = {};
    res.render("home", context);
});

//
// Receive NetScaler config file in Body of POST
//
app.post("/config", function(req, res, next) {
    config = req.body;
    config = config.replace(/"/g, '\\"');

    var process = spawnSync("python3", ["./NS_Doc_Python.py", config]);
    let errorText = process.stderr.toString().trim();
    if (errorText) {
        errorObj = { stack: errorText };
        next(errorObj);
    } else {
        res.type("plain/text");
        res.status(200);
        res.send(process.stdout.toString());
    }
});

//
// Generic Error
//
app.use(function(err, req, res, next) {
    console.error(err.stack);
    res.type("plain/text");
    res.status(500);
    res.send("500 - Server Error");
});

//
// Launch Node Server
//
app.listen(port, function() {
    console.log(
        "Node started on http://localhost:" +
            app.get("port") +
            "; press Ctrl-C to terminate."
    );
});
