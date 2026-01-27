const CACHE_NAME = "sibs-v4-cache-v1";

// Install service worker (no caching)
self.addEventListener("install", (event) => {
    console.log("Service Worker installed (no caching)");
    self.skipWaiting();
});

// Fetch directly from network, no caching
self.addEventListener("fetch", (event) => {
    event.respondWith(
        fetch(event.request).catch(() => {
            // If network fails, just fail (no cache fallback)
            return new Response("Network error", {
                status: 408,
                headers: { "Content-Type": "text/plain" },
            });
        }),
    );
});

// Clear all existing caches on activation
self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches
            .keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        console.log("Deleting cache:", cacheName);
                        return caches.delete(cacheName);
                    }),
                );
            })
            .then(() => {
                console.log("All caches cleared");
                return self.clients.claim();
            }),
    );
});
