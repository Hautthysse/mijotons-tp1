require("dotenv").config();
const express = require("express");
const cors = require("cors");
const { initKeycloak } = require("./keycloak");
const recipesRoutes = require("./routes/recipes");

const app = express();
app.use(cors({ origin: true }));
app.use(express.json());

const keycloak = initKeycloak(app);

app.get("/health", (req, res) => res.json({ ok: true }));

app.use("/recipes", recipesRoutes(keycloak));

const port = process.env.PORT || 3001;
app.listen(port, () => console.log(`API running on http://localhost:${port}`));