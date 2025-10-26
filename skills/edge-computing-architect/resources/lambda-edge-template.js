// AWS Lambda@Edge Template for Viewer Request
// Reference: https://aws.amazon.com/lambda/edge/

exports.handler = async (event) => {
  const request = event.Records[0].cf.request
  const headers = request.headers

  // Add security headers
  headers['strict-transport-security'] = [{
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubdomains; preload'
  }]

  headers['x-content-type-options'] = [{
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  }]

  headers['x-frame-options'] = [{
    key: 'X-Frame-Options',
    value: 'DENY'
  }]

  // A/B test routing
  const abTestCookie = headers.cookie?.[0]?.value.match(/ab_test=(\w+)/)
  if (!abTestCookie) {
    const variant = Math.random() < 0.5 ? 'A' : 'B'
    headers['cookie'] = [{
      key: 'Cookie',
      value: `ab_test=${variant}`
    }]
  }

  return request
}
