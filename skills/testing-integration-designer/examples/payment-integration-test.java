// Payment API Integration Test Example (Spring Boot + TestContainers + WireMock)
@SpringBootTest
@Testcontainers
@AutoConfigureMockMvc
class PaymentServiceIntegrationTest {

  @Container
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15-alpine")
    .withDatabaseName("testdb");

  @Autowired
  private MockMvc mockMvc;

  @Autowired
  private TransactionRepository transactionRepo;

  private WireMockServer wireMockServer;

  @BeforeEach
  void setup() {
    wireMockServer = new WireMockServer(8089);
    wireMockServer.start();
    configureFor("localhost", 8089);
  }

  @Test
  void processPayment_validCard_createsTransaction() throws Exception {
    // Arrange: Mock Stripe API
    stubFor(post("/v1/charges")
      .willReturn(ok().withBody("{\"id\":\"ch_123\",\"status\":\"succeeded\"}")));

    // Act: Send payment request
    mockMvc.perform(post("/payments")
      .contentType(MediaType.APPLICATION_JSON)
      .content("{\"amount\":1000,\"currency\":\"USD\"}"))
      .andExpect(status().isCreated());

    // Assert: Verify transaction persisted
    assertEquals(1, transactionRepo.count());
    verify(postRequestedFor(urlEqualTo("/v1/charges")));
  }
}
