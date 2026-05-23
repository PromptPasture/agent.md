---
name: codegen-backend
description: Build or modify backend implementation. Use for API routes, services, middleware, workers, persistence, validation, authorization, configuration, observability, and backend behavior tests.
license: MIT
version: 1.1.0
tags:
  - codegen
  - backend
  - engineering
author: Oleg Shulyakov
metadata:
  catalog: software-team-roles
---

# codegen-backend

Implement backend code for APIs, services, workers, persistence, middleware, validation, authorization, configuration, observability, and behavior tests. Use this as a router: identify the backend language from the request and repository, read exactly one language reference, and read at most one framework reference when the framework signal is explicit or unambiguous.

## Variant Detection

**Route from concrete evidence before writing code.**

- **User intent:** Prefer explicit language, framework, runtime, package manager, file path, extension, or named backend surface from the prompt.
- **Repository evidence:** Inspect dependency manifests, source layout, imports, test folders, and CI jobs before choosing a variant. Common signals include `pyproject.toml`, `requirements.txt`, `package.json`, `go.mod`, `pom.xml`, `build.gradle`, `Gemfile`, `Cargo.toml`, `.csproj`, `composer.json`, and `mix.exs`.
- **Owned surface:** Routes, controllers, services, repositories, jobs, workers, middleware, validators, persistence, configuration, observability, and backend tests route to the language that already owns that surface.
- **Adjacent skills:** Use `design-api` for contract-first API design unless the user asks to implement an existing contract. Use specialized auth, GraphQL, real-time, SQL, or test skills when those are the primary artifact rather than backend implementation.
- **Ambiguity:** If multiple backend stacks remain plausible after inspection, ask one short question naming the likely choices.

## Language Routing Table

**Read exactly one language reference for the selected backend stack.**

| Signal | Reference |
| --- | --- |
| FastAPI, Django, Flask, Pydantic, SQLAlchemy, pytest, `pyproject.toml`, `.py` | `references/python.md` |
| Express, Fastify, NestJS, Hono, Zod, Prisma, Vitest/Jest, `package.json`, `.js`, `.ts` | `references/nodejs.md` |
| `net/http`, Chi, Gin, Echo, sqlc, GORM, `go.mod`, `.go` | `references/go.md` |
| Spring Boot, Jakarta, Maven, Gradle, JPA, JUnit, `pom.xml`, `.java` | `references/java.md` |
| Rails, Sinatra, ActiveRecord, Sidekiq, RSpec, `Gemfile`, `.rb` | `references/ruby.md` |
| Axum, Actix Web, Tokio, SQLx, Diesel, `Cargo.toml`, `.rs` | `references/rust.md` |
| ASP.NET Core, Minimal APIs, Controllers, EF Core, xUnit, `.csproj`, `.cs` | `references/csharp.md` |
| Laravel, Symfony, Eloquent, Artisan, Pest/PHPUnit, `composer.json`, `.php` | `references/php.md` |
| Ktor, Kotlin Spring Boot, coroutines, Exposed, Gradle Kotlin DSL, `.kt` | `references/kotlin.md` |
| Phoenix, Plug, Ecto, Oban, ExUnit, `mix.exs`, `.ex`, `.exs` | `references/elixir.md` |
| C services, embedded backends, POSIX sockets, libuv, Mongoose/CivetWeb, CMake, Make, `.c`, `.h` | `references/c.md` |
| C++ services, Boost.Asio/Beast, Drogon, Pistache, gRPC, CMake, Conan, vcpkg, `.cpp`, `.hpp` | `references/cpp.md` |
| VB.NET, ASP.NET, .NET Framework, Windows services, `.vbproj`, `.vb` | `references/visual-basic.md` |
| plumber, Shiny APIs, RServe, batch analytics services, `renv.lock`, `.R`, `.Rmd` | `references/r.md` |
| Delphi/Object Pascal services, RAD Server, DataSnap, Horse, Lazarus, `.pas`, `.dpr` | `references/delphi.md` |
| Fortran numerical services, ISO_C_BINDING, fpm, CMake, batch compute jobs, `.f90`, `.f` | `references/fortran.md` |
| Perl web services, Mojolicious, Dancer2, Catalyst, DBI, CPAN, `cpanfile`, `.pl`, `.pm` | `references/perl.md` |
| Swift server code, Vapor, Hummingbird, SwiftNIO, `Package.swift`, `.swift` | `references/swift.md` |
| Ada services, GNAT, Alire, SPARK, AWS Ada Web Server, `.adb`, `.ads` | `references/ada.md` |
| MATLAB production server code, batch workers, toolboxes, `.m`, `.mlx`, `startup.m` | `references/matlab.md` |

## Framework References

**Add one framework reference only when it materially narrows implementation rules.**

After reading the language reference, read at most one framework reference when the signal is explicit from the prompt or unambiguous from dependencies, imports, and file layout. Keep framework files flat in `references/`.

| Signal | Reference |
| --- | --- |
| FastAPI, Starlette route dependencies | `references/python-fastapi.md` |
| Django, Django REST Framework, `manage.py` | `references/python-django.md` |
| Flask, Flask blueprints | `references/python-flask.md` |
| Express, Express Router | `references/nodejs-express.md` |
| Fastify, Fastify plugins | `references/nodejs-fastify.md` |
| NestJS, modules, providers, decorators | `references/nodejs-nestjs.md` |
| Hono | `references/nodejs-hono.md` |
| Nitro, h3 server handlers | `references/nodejs-nitro.md` |
| Gin | `references/go-gin.md` |
| Chi | `references/go-chi.md` |
| Echo | `references/go-echo.md` |
| Fiber | `references/go-fiber.md` |
| Spring Boot | `references/java-spring-boot.md` |
| Quarkus | `references/java-quarkus.md` |
| Micronaut | `references/java-micronaut.md` |
| Ktor | `references/kotlin-ktor.md` |
| Rails | `references/ruby-rails.md` |
| Sinatra | `references/ruby-sinatra.md` |
| Laravel | `references/php-laravel.md` |
| Symfony | `references/php-symfony.md` |
| Axum | `references/rust-axum.md` |
| Actix Web | `references/rust-actix-web.md` |
| Rocket | `references/rust-rocket.md` |
| ASP.NET Core, Minimal APIs, controllers | `references/csharp-aspnet-core.md` |
| Phoenix | `references/elixir-phoenix.md` |

## Working Rules

**Make the smallest complete backend change that fits the existing system.**

- **Inspect first:** Read the nearby route/controller, service, persistence, validation, error handling, dependency injection, logging, migration, factory, fixture, and test conventions before editing.
- **Follow the local shape:** Put code where the repository already puts similar behavior. Prefer existing helpers, envelopes, domain errors, configuration loaders, database clients, queue abstractions, and test utilities over new patterns.
- **Keep boundaries clear:** Keep transport handlers thin when a service or domain layer exists. Put business rules in the layer that already owns them, and keep persistence details behind the existing repository or ORM boundary.
- **Apply SOLID pragmatically:** Give new functions, services, and domain objects one clear responsibility; keep interfaces narrow; depend on abstractions only when the project already does or when the boundary reduces real coupling or test risk.
- **Preserve contracts:** Treat public API behavior, response shapes, status codes, event payloads, and job side effects as contracts. Avoid breaking changes unless the user asks for them, and update docs, generated specs, or fixtures when the repo keeps them in sync.
- **Secure boundaries:** Validate input at the boundary, enforce authorization before side effects, avoid logging secrets, and store credentials only through existing configuration or secret mechanisms.
- **Handle data safely:** Use transactions for multi-write operations. Make idempotency, retry classification, cancellation, timeouts, pagination stability, and concurrency behavior explicit for jobs, webhooks, payments, imports, and external integrations.
- **Return consistent errors:** Use the project's existing error envelope or framework conventions. Do not expose stack traces, raw SQL errors, tokens, secret material, or sensitive internal IDs in user-facing responses.
- **Test behavior:** Add or update focused tests for the requested behavior, including success, validation failure, authorization failure when relevant, and persistence or transaction edge cases for write flows.
- **Verify locally:** Run the narrowest relevant formatter, linter, typecheck, migration check, and tests available. If a command cannot run, report the failure reason and the exact command.

## Implementation Flow

**Move from evidence to code to verification without inventing parallel architecture.**

1. Identify the language and optional framework, then read the selected reference files.
2. Inspect the closest existing implementation and tests for the same kind of backend surface.
3. Plan the minimal file set across transport, service/domain, persistence, validation, configuration, and tests.
4. Edit code using project conventions, keeping public behavior compatible unless instructed otherwise.
5. Add or update tests that prove the behavior and likely failure paths.
6. Run focused verification commands and fix regressions within the requested scope.

## Output Format

**Report what changed and how it was checked.**

When editing a repository, finish with changed files, commands run, and verification status. Mention unresolved risks only when they affect handoff.

When only drafting code, use this structure:

```text
Assumptions:
- ...

Files:
- path/to/file

Run:
- command

Notes:
- ...
```
