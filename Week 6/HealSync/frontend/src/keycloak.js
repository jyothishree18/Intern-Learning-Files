
import Keycloak from "keycloak-js";

const keycloak = new Keycloak({
  url: "http://localhost:8080",
  realm: "healsync",
  clientId: "healsync-frontend",
});

let initializationPromise;

export function initKeycloak() {
  if (!initializationPromise) {
    initializationPromise = keycloak.init({
      onLoad: "check-sso",
      pkceMethod: "S256",
      checkLoginIframe: false,
    });
  }

  return initializationPromise;
}

export default keycloak;
