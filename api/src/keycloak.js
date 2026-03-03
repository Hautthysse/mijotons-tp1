const session = require("express-session");
const Keycloak = require("keycloak-connect");

function initKeycloak(app) {
    const memoryStore = new session.MemoryStore();

    app.use(
        session({
            secret: "mijotons-secret",
            resave: false,
            saveUninitialized: true,
            store: memoryStore,
        })
    );

    const keycloak = new Keycloak({ store: memoryStore });
    app.use(keycloak.middleware());

    return keycloak;
}

module.exports = { initKeycloak };