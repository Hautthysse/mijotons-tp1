const fs = require("fs");
const path = require("path");

const DB_PATH = path.join(__dirname, "..", "..", "data", "recipes.json");

function readAll() {
    const raw = fs.readFileSync(DB_PATH, "utf-8");
    return JSON.parse(raw);
}

function writeAll(recipes) {
    fs.writeFileSync(DB_PATH, JSON.stringify(recipes, null, 2), "utf-8");
}

function nextId(recipes) {
    const max = recipes.reduce((m, r) => Math.max(m, r.id || 0), 0);
    return max + 1;
}

module.exports = { readAll, writeAll, nextId };