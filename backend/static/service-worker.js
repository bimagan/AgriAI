self.addEventListener("install", e => {
    e.waitUntil(
        caches.open("agri-cache").then(cache => {
            return cache.addAll([
                "/",
                "/dashboard",
                "/static/css/style.css",
                "/static/js/app.js"
            ]);
        })
    );
});
