const CACHE_NAME = "sibs-v4-cache-v1";
const urlsToCache = [
    "/",
    "/static/css/styles.css",
    "/static/js/index.js",
    "/static/lib/mdui.css",
    "/static/lib/mdui.global.js",
    "/static/lib/socket.io.min.js",
    "/static/img/favicon.ico",
];

// Install service worker and cache resources
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log("Opened cache");
            return cache.addAll(urlsToCache);
        }),
    );
});

// Fetch from cache, fall back to network
self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            // Cache hit - return response
            if (response) {
                return response;
            }
            return fetch(event.request);
        }),
    );
});

// Update service worker
self.addEventListener("activate", (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                }),
            );
        }),
    );
});
