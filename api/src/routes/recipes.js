const express = require("express");
const store = require("../store/recipesStore");

module.exports = function (keycloak) {
    const router = express.Router();

    router.get("/", (req, res) => {
        res.json(store.readAll());
    });

    router.get("/:id", (req, res) => {
        const id = Number(req.params.id);
        const recipe = store.readAll().find((r) => r.id === id);
        if (!recipe) return res.status(404).json({ message: "Recipe not found" });
        res.json(recipe);
    });

    router.post("/", keycloak.protect(), (req, res) => {
        const recipes = store.readAll();
        const payload = req.body;

        if (!payload.title || !payload.category) {
            return res.status(400).json({ message: "title and category are required" });
        }

        const newRecipe = {
            id: store.nextId(recipes),
            ...payload,
            created_at: new Date().toISOString(),
        };

        recipes.push(newRecipe);
        store.writeAll(recipes);
        res.status(201).json(newRecipe);
    });

    router.put("/:id", keycloak.protect(), (req, res) => {
        const id = Number(req.params.id);
        const payload = req.body;

        const recipes = store.readAll();
        const idx = recipes.findIndex((r) => r.id === id);
        if (idx === -1) return res.status(404).json({ message: "Recipe not found" });

        recipes[idx] = { ...recipes[idx], ...payload, id };
        store.writeAll(recipes);
        res.json(recipes[idx]);
    });

    router.delete("/:id", keycloak.protect(), (req, res) => {
        const id = Number(req.params.id);
        const recipes = store.readAll();
        const idx = recipes.findIndex((r) => r.id === id);
        if (idx === -1) return res.status(404).json({ message: "Recipe not found" });

        const removed = recipes.splice(idx, 1)[0];
        store.writeAll(recipes);
        res.json(removed);
    });

    return router;
};