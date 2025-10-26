// k6 E-Commerce Checkout Load Test (1000 users, SLI validation)
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '3m', target: 1000 },
    { duration: '10m', target: 1000 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<800'],
    http_req_failed: ['rate<0.005'],
  },
};

export default function () {
  const payload = JSON.stringify({
    cart_id: `cart-${__VU}-${__ITER}`,
    payment_method: 'card',
  });
  const res = http.post('https://api.example.com/checkout', payload, {
    headers: { 'Content-Type': 'application/json' },
  });
  check(res, {
    'status 200': (r) => r.status === 200,
    'checkout success': (r) => r.json('status') === 'completed',
  });
  sleep(Math.random() * 3 + 2);
}