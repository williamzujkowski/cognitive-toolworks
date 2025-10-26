// Pact Consumer Test: Mobile App → User Service (@pact-foundation/pact v12.x)
const { PactV3, MatchersV3 } = require('@pact-foundation/pact');
const { getUserById } = require('./api-client');

const provider = new PactV3({
  consumer: 'mobile-app',
  provider: 'user-service',
});

describe('User API Contract', () => {
  it('gets user by ID', () => {
    provider
      .given('user 123 exists')
      .uponReceiving('a request for user 123')
      .withRequest({ method: 'GET', path: '/users/123' })
      .willRespondWith({
        status: 200,
        body: {
          id: MatchersV3.like(123),
          name: MatchersV3.like('Alice'),
          email: MatchersV3.email('alice@example.com'),
        },
      });

    return provider.executeTest(async (mockServer) => {
      const user = await getUserById(mockServer.url, 123);
      expect(user.name).toBe('Alice');
    });
  });
});