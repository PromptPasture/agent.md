# Backend Testing

---

## Core Rules

- Test behaviour, not implementation. Test what a function does, not how it does it.
- Unit tests cover services and pure logic. Integration tests cover repositories and handlers.
- Do not mock the DB in integration tests. Use a real DB (test container or test schema).
- Each test is independent. Seed its own data and clean up after itself.

---

## Test Types

|Type|Scope|Speed|What it tests|
|---|---|---|---|
|Unit|Single function or service|Fast (< 1ms)|Business logic, transformations, error branches|
|Integration|Repository + real DB|Medium (< 100ms)|Queries, transactions, constraint behaviour|
|Handler / API|Full HTTP stack|Medium (< 200ms)|Request parsing, auth, routing, response shape|
|Contract|Against API schema|Medium|Response matches OpenAPI/JSON Schema spec|

---

## Unit Testing Services

Inject repository interfaces — mock the interface, not the DB:

```pseudocode
// Create a mock that fulfils the UserRepository interface
mockRepo = MockUserRepository {
  getByEmail: function(email):
    if email == "existing@example.com":
      return User { id: "1", email: email }
    return NOT_FOUND error
}

service = UserService(repo: mockRepo)

// Test: duplicate email returns CONFLICT
result = service.createUser({ email: "existing@example.com", name: "Test" })
assert result is error
assert result.code == "CONFLICT"
```

---

## Integration Testing Repositories

Use a real DB started via a test container or a dedicated test schema:

```pseudocode
// Setup: start a real DB, run migrations
testDB = startTestDatabase("postgres:16")
runMigrations(testDB)

// Test
function test_UserRepository_Create():
  defer truncate(testDB, "users")

  repo = UserRepository(db: testDB)
  user = repo.create({ email: "test@example.com", name: "Test User" })

  assert user.id is not empty
  assert user.email == "test@example.com"
```

---

## Handler / API Testing

Test the full HTTP stack without starting a real network server:

```pseudocode
// Setup: build the full handler/router chain in-process
server = setupTestServer()

// Test: happy path
function test_CreateUser_Success():
  response = server.POST("/api/v1/users",
    body:    { email: "new@example.com", name: "New User" },
    headers: { Authorization: "Bearer " + adminToken }
  )
  assert response.status == 201
  assert response.body.id is not empty
  assert response.body.email == "new@example.com"

// Test: validation failure
function test_CreateUser_MissingEmail_Returns400():
  response = server.POST("/api/v1/users",
    body:    { name: "No Email" },
    headers: { Authorization: "Bearer " + adminToken }
  )
  assert response.status == 400
  assert response.body.code == "VALIDATION_ERROR"
```

---

## Test Coverage Priorities

Test every case that has meaningful branching:

|Priority|Cases to cover|
|---|---|
|P0|Auth failure (401/403), input validation failure (400), happy path (2xx)|
|P1|Not found (404), conflict (409), service error mapped to 500|
|P2|Edge cases: empty string, max-length input, zero values, null optional fields|
|P3|Concurrent writes (race condition), transaction rollback on partial failure|

---

## Test Naming

Name tests so the failure message explains what went wrong:

```text
createUser_success
createUser_duplicateEmail_returns409
createUser_missingEmail_returns400
createUser_unauthenticated_returns401
createUser_insufficientRole_returns403
```

---

## What NOT to Do

- Do not mock the DB in integration tests. Mocks hide real constraint and query behaviour.
- Do not share state between tests. Each test seeds and cleans its own data.
- Do not test implementation details. Test the public contract (inputs and outputs).
- Do not suppress test output to make logs cleaner. Noisy tests surface real problems.
