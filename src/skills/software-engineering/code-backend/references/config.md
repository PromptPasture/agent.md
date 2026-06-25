# Configuration and Secrets

---

## Core Rules

- All config values come from environment variables — no hardcoded values in code
- Secrets (DB passwords, API keys, JWT signing keys) never appear in source code or logs
- Validate all config at startup — fail fast with a clear message if a required value is missing
- Never log config values that are or could be secrets

---

## Config Loading Pattern

Load and validate all config at startup before the server starts accepting requests:

```pseudocode
Config:
  port        integer  -- env: PORT,         default: 8080
  databaseURL string   -- env: DATABASE_URL,  required
  jwtSecret   string   -- env: JWT_SECRET,    required, minLength: 32
  logLevel    string   -- env: LOG_LEVEL,     default: "info"
  appEnv      string   -- env: APP_ENV,       default: "development"

function loadConfig() → Config | error:
  config = parseEnv(Config)
  if config.jwtSecret.length < 32:
    return error("JWT_SECRET must be at least 32 characters")
  return config
```

Use the env-parsing and validation library available in the project stack. Call `loadConfig()` once at startup; pass the resulting struct through dependency injection — do not read `os.environ` / `process.env` deep in the call stack.

---

## Startup Validation

Fail fast and loudly when required config is missing:

```text
Error: missing required configuration:
  DATABASE_URL is required
  JWT_SECRET must be at least 32 characters

Set these values in your environment or .env file and restart.
```

The process exits with a non-zero code. Do not start serving traffic with invalid config.

---

## Secret Management

### In development

Use a `.env` file (gitignored). Never commit `.env` to version control.

```text
# .env  (never commit — gitignored)
DATABASE_URL=postgres://user:password@localhost:5432/myapp
JWT_SECRET=dev-secret-at-least-32-characters-long
```

```text
# .env.example  (commit this — safe template)
DATABASE_URL=postgres://user:password@localhost:5432/myapp
JWT_SECRET=<replace-with-32-char-secret>
```

### In production

Inject secrets through the platform's secret management:

|Platform|Mechanism|
|---|---|
|Kubernetes|`Secret` objects mounted as env vars or files|
|AWS|Secrets Manager or Parameter Store (SSM) via env injection|
|GCP|Secret Manager via Workload Identity|
|Heroku|Config Vars|
|Docker / Compose|`secrets:` block or env file excluded from the image|

Never bake secrets into Docker images. Never pass secrets as build args.

---

## Environment-specific Behaviour

Use a single `APP_ENV` variable to gate environment-specific behaviour:

```pseudocode
if config.appEnv == "production":
  enable structured JSON logging
  disable debug endpoints
  enable rate limiting
```

Prefer config flags over environment name checks where possible (e.g., `RATE_LIMIT_ENABLED=true` is better than `if appEnv == "production"`), so behaviour is explicit and testable independently.

---

## What NOT to Do

- Do not hardcode ports, base URLs, DB connection strings, or timeouts.
- Do not log config at startup if it contains secrets. Log a masked summary instead.
- Do not use config files (YAML, TOML, JSON) for secrets. They end up in the repo or image.
- Do not read environment variables deep in the call stack. Read once at startup and pass via struct.
