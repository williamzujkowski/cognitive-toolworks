// Cloudflare Worker Template for Edge Caching
// Reference: https://workers.cloudflare.com/

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  const cacheKey = new Request(url.toString(), request)
  const cache = caches.default

  // Try cache first
  let response = await cache.match(cacheKey)
  if (response) {
    return response
  }

  // Cache miss - fetch from origin
  response = await fetch(request)

  // Cache successful responses
  if (response.ok) {
    const cacheControl = response.headers.get('Cache-Control')
    if (!cacheControl || !cacheControl.includes('no-store')) {
      response = new Response(response.body, response)
      response.headers.set('Cache-Control', 'public, max-age=60')
      event.waitUntil(cache.put(cacheKey, response.clone()))
    }
  }

  return response
}
