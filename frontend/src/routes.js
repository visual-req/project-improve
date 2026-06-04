const LEGACY_FRONTEND_PREFIX = "/frontend";

const ROUTES = [
  { page: "analysis", path: "/analysis" },
  { page: "configSystem", path: "/config/system" },
  { page: "configMetrics", path: "/config/metrics" },
  { page: "concept", path: "/concept" },
  { page: "projectManage", path: "/projects" },
  { page: "actions", path: "/actions" }
];

export function pageToPath(page) {
  const p = String(page || "");
  const found = ROUTES.find((r) => r.page === p);
  return found ? found.path : "/analysis";
}

export function pageToUrl(page) {
  return pageToPath(page);
}

function normalizePathname(pathname) {
  const raw = String(pathname || "");
  if (!raw) return { path: "/analysis", needsRedirect: true };

  if (raw === "/" || raw === "/index.html") return { path: "/analysis", needsRedirect: true };

  if (raw === `${LEGACY_FRONTEND_PREFIX}/index.html`) return { path: "/analysis", needsRedirect: true };
  if (raw === LEGACY_FRONTEND_PREFIX || raw === `${LEGACY_FRONTEND_PREFIX}/`) return { path: "/analysis", needsRedirect: true };

  const normalized = raw.startsWith(`${LEGACY_FRONTEND_PREFIX}/`) ? raw.slice(LEGACY_FRONTEND_PREFIX.length) : raw;
  if (!normalized.startsWith("/")) return { path: "/analysis", needsRedirect: false };

  const rest = normalized;
  if (!rest || rest === "/") return { path: "/analysis", needsRedirect: true };

  const cleaned = rest.endsWith("/") && rest.length > 1 ? rest.slice(0, -1) : rest;
  const shouldRedirect = raw.startsWith(`${LEGACY_FRONTEND_PREFIX}/`) || raw === LEGACY_FRONTEND_PREFIX || raw === `${LEGACY_FRONTEND_PREFIX}/`;
  return { path: cleaned, needsRedirect: shouldRedirect };
}

export function getInitialRoute() {
  try {
    const { path, needsRedirect } = normalizePathname(window.location && window.location.pathname ? window.location.pathname : "");
    const hit = ROUTES.find((r) => r.path === path);
    if (needsRedirect) {
      try {
        window.history.replaceState({}, "", hit ? hit.path : "/analysis");
      } catch {}
    }
    return { page: hit ? hit.page : "analysis" };
  } catch {
    return { page: "analysis" };
  }
}

export function navigateTo(page, opts) {
  const { replace } = opts && typeof opts === "object" ? opts : { replace: false };
  const url = pageToUrl(page);
  try {
    if (replace) window.history.replaceState({}, "", url);
    else window.history.pushState({}, "", url);
  } catch {}
  try {
    window.dispatchEvent(new Event("prjmx:navigation"));
  } catch {}
}

export function listenRouteChange(onChange) {
  const handler = () => {
    try {
      const r = getInitialRoute();
      onChange(r);
    } catch {}
  };
  window.addEventListener("popstate", handler);
  window.addEventListener("prjmx:navigation", handler);
  return () => {
    window.removeEventListener("popstate", handler);
    window.removeEventListener("prjmx:navigation", handler);
  };
}
