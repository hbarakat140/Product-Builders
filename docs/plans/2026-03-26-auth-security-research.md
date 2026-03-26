# Auth & Security Analyzer Research

Deep research conducted 2026-03-26 covering authentication strategies, security detection patterns, and anti-patterns across all major ecosystems.

## Auth Detection Checklist

### Auth Strategies/Protocols

| Strategy | Description | Key Indicators |
|----------|-------------|----------------|
| JWT | JSON Web Tokens for stateless auth | `jsonwebtoken`, `jose`, token decode/verify calls |
| OAuth2 | Delegated authorization | `/authorize`, `/token` endpoints, client_id/secret |
| OIDC | OpenID Connect (identity layer on OAuth2) | `openid` scope, id_token, userinfo endpoint |
| SAML | Security Assertion Markup Language | SAML metadata XML, assertion consumer service |
| API Keys | Static key-based access | `x-api-key` header, API key middleware |
| Passkeys/WebAuthn | Passwordless FIDO2 auth | `@simplewebauthn/*`, navigator.credentials, attestation |
| Magic Links | Email-based passwordless auth | Token-in-URL patterns, email sending + token verification |
| Session-based | Server-side session with cookies | `express-session`, session middleware, session store |
| Basic Auth | HTTP Basic Authentication | `Authorization: Basic`, base64 credentials |

Each strategy has specific libraries and config files per ecosystem that should be detected.

### OAuth Providers to Detect

| Provider | Config Identifiers |
|----------|-------------------|
| Google | `GOOGLE_CLIENT_ID`, `google` provider config, `accounts.google.com` |
| GitHub | `GITHUB_CLIENT_ID`, `github` provider config, `github.com/login/oauth` |
| Microsoft/Azure AD | `AZURE_AD_CLIENT_ID`, `microsoft` provider, `login.microsoftonline.com` |
| Apple | `APPLE_CLIENT_ID`, `apple` provider, `appleid.apple.com` |
| Facebook | `FACEBOOK_APP_ID`, `facebook` provider, `graph.facebook.com` |
| Twitter/X | `TWITTER_CLIENT_ID`, `twitter` provider, `api.twitter.com` |
| Discord | `DISCORD_CLIENT_ID`, `discord` provider, `discord.com/api/oauth2` |
| Okta | `OKTA_DOMAIN`, `okta` provider, `*.okta.com` |

### Auth Libraries Per Ecosystem

#### JS/TS

| Library | Package | Config Files | Notes |
|---------|---------|-------------|-------|
| next-auth / Auth.js v5 | `next-auth`, `@auth/core` | `auth.ts`, `auth.config.ts`, `[...nextauth]/route.ts` | Most popular Next.js auth |
| Clerk | `@clerk/nextjs`, `@clerk/clerk-react` | `middleware.ts` with `clerkMiddleware` | Managed auth service |
| Supabase Auth | `@supabase/supabase-js`, `@supabase/auth-helpers-*` | `supabase/config.toml` | Supabase integrated auth |
| Firebase Auth | `firebase/auth`, `firebase-admin/auth` | `firebase.json`, `firebaseConfig` | Google Firebase auth |
| Passport | `passport`, `passport-*` | Strategy configuration files | Modular auth middleware |
| Auth0 | `@auth0/nextjs-auth0`, `auth0-js` | `auth0` config, `.auth0` | Managed identity platform |
| Lucia | `lucia` | `lucia.ts`, `lucia.d.ts` | Deprecated March 2025 -- flag as legacy |
| better-auth | `better-auth` | `auth.ts` with `betterAuth()` | Rising alternative to Lucia |

#### Python

| Library | Package | Config Files | Notes |
|---------|---------|-------------|-------|
| django-allauth | `django-allauth` | `INSTALLED_APPS`, `SOCIALACCOUNT_PROVIDERS` | 21k+ repos, most popular Django auth |
| django.contrib.auth | Built-in | `AUTH_USER_MODEL`, `AUTHENTICATION_BACKENDS` | Django built-in auth |
| flask-login | `flask-login` | `LoginManager()` initialization | Flask session auth |
| flask-jwt-extended | `flask-jwt-extended` | `JWTManager()` initialization | Flask JWT auth |
| authlib | `authlib` | OAuth client/server config | Generic OAuth library |
| fastapi-users | `fastapi-users` | Router configuration | FastAPI auth |

#### Java

| Library | Package | Config Files | Notes |
|---------|---------|-------------|-------|
| Spring Security | `spring-boot-starter-security` | `SecurityFilterChain` bean, `SecurityConfig` | Most popular Java auth |
| JJWT | `io.jsonwebtoken:jjwt-*` | JWT builder/parser usage | Java JWT library |
| Keycloak | `keycloak-spring-boot-starter` | `keycloak.json`, realm config | Identity/access management |

#### Go

| Library | Package | Config Files | Notes |
|---------|---------|-------------|-------|
| golang-jwt/jwt | `github.com/golang-jwt/jwt` | Token creation/validation | Go JWT standard |
| goth | `github.com/markbates/goth` | Provider configuration | Multi-provider OAuth |
| go-oidc | `github.com/coreos/go-oidc` | OIDC provider/verifier setup | OIDC for Go |
| go-webauthn | `github.com/go-webauthn/webauthn` | WebAuthn config | Passkey support |

#### Ruby

| Library | Gem | Config Files | Notes |
|---------|-----|-------------|-------|
| Devise | `devise` | `devise.rb` initializer, `devise` routes | Most popular Ruby auth |
| OmniAuth | `omniauth`, `omniauth-*` | Strategy configuration | Multi-provider OAuth |
| Sorcery | `sorcery` | `sorcery.rb` initializer | Lightweight auth |
| Doorkeeper | `doorkeeper` | `doorkeeper.rb` initializer | OAuth2 provider |
| Rodauth | `rodauth` | `rodauth` plugin configuration | Modern Ruby auth |

#### C#/.NET

| Library | Package | Config Files | Notes |
|---------|---------|-------------|-------|
| ASP.NET Identity | `Microsoft.AspNetCore.Identity` | `IdentityDbContext`, `AddIdentity()` | Built-in .NET auth |
| Duende IdentityServer | `Duende.IdentityServer` | IdentityServer config | OpenID Connect server |
| Microsoft.Identity.Web | `Microsoft.Identity.Web` | `AddMicrosoftIdentityWebApp()` | Azure AD integration |

### MFA/2FA Detection

| Method | Libraries/Indicators | Detection Pattern |
|--------|---------------------|-------------------|
| TOTP | `otplib`, `speakeasy`, `pyotp`, `java-totp` | QR code generation, secret storage, 6-digit verify |
| SMS | Twilio (`twilio`), Vonage (`@vonage/server-sdk`) | Phone number storage, SMS send calls |
| Email OTP | Email sending + OTP generation | Short-lived codes, email templates |
| Push | Duo (`@duosecurity/duo_web`), Auth0 Guardian | Push notification triggers |
| Hardware Keys | WebAuthn (`@simplewebauthn/*`) | Credential creation, assertion |
| Backup/Recovery Codes | Hashed code storage | Batch code generation, one-time use |

### Session Management Verification

| Check | Best Practice | Detection Method |
|-------|--------------|-----------------|
| HttpOnly | Must be set on session cookies | Cookie configuration parsing |
| Secure | Must be set in production | Cookie configuration parsing |
| SameSite | Should be `Strict` or `Lax` | Cookie configuration parsing |
| `__Host-` prefix | Recommended for sensitive cookies | Cookie name pattern matching |
| Session rotation | Must rotate on auth state change | Session regenerate calls after login |
| Expiry | Must have reasonable TTL | Session maxAge/expires configuration |
| ID length | Minimum 128 bits of entropy | Session ID generation config |

---

## Security Detection Checklist

### OWASP Top 10:2025 Mapping

| # | Category | Static Detection Methods |
|---|----------|------------------------|
| A01 | Broken Access Control | Missing auth middleware on routes, no role checks, IDOR patterns, CORS misconfiguration |
| A02 | Cryptographic Failures | Weak algorithms (MD5, SHA1 for passwords), hardcoded keys, HTTP links, missing TLS |
| A03 | Injection | Raw SQL concatenation, unsanitized template rendering, eval/exec with user input |
| A04 | Insecure Design | Missing rate limiting, no account lockout, no CAPTCHA, missing business logic validation |
| A05 | Security Misconfiguration | Debug mode enabled, default credentials, unnecessary features enabled, missing headers |
| A06 | Vulnerable/Outdated Components | Known CVEs in dependencies, deprecated packages, missing lock files |
| A07 | Identification/Authentication Failures | Weak password rules, missing MFA, session fixation, credential stuffing vulnerability |
| A08 | Software/Data Integrity Failures | Missing SRI hashes, unsigned updates, unsafe deserialization, no CI/CD pipeline security |
| A09 | Security Logging/Monitoring Failures | No auth event logging, missing error logging, no intrusion detection |
| A10 | Server-Side Request Forgery (SSRF) | Unvalidated URL inputs, internal network access, cloud metadata access |

### Security Headers

| Header | Recommended Value | Risk if Missing |
|--------|------------------|----------------|
| Content-Security-Policy (CSP) | Strict policy, no `unsafe-inline` | XSS attacks |
| Strict-Transport-Security (HSTS) | `max-age=31536000; includeSubDomains; preload` | Downgrade attacks |
| X-Frame-Options | `DENY` or `SAMEORIGIN` | Clickjacking |
| X-Content-Type-Options | `nosniff` | MIME type sniffing |
| Permissions-Policy | Restrict camera, microphone, geolocation | Feature abuse |
| Referrer-Policy | `strict-origin-when-cross-origin` or `no-referrer` | Information leakage |

### Rate Limiting Libraries

| Ecosystem | Libraries |
|-----------|-----------|
| Express/Node | `express-rate-limit`, `@nestjs/throttler`, `rate-limiter-flexible` |
| Python | `django-ratelimit`, `django-axes`, `slowapi`, `flask-limiter` |
| Java | `bucket4j`, `resilience4j`, `guava RateLimiter` |
| Go | `golang.org/x/time/rate`, `limiter` |
| Ruby | `rack-attack`, `ratelimit` |
| .NET | `AspNetCoreRateLimit`, built-in rate limiting (.NET 7+) |

### Secrets Management

| Tool | Type | Detection Pattern |
|------|------|-------------------|
| HashiCorp Vault | Self-hosted | `vault` CLI, `VAULT_ADDR`, vault client libraries |
| AWS Secrets Manager | Cloud | `@aws-sdk/client-secrets-manager`, `secretsmanager` API calls |
| Azure Key Vault | Cloud | `@azure/keyvault-secrets`, Key Vault URL patterns |
| GCP Secret Manager | Cloud | `@google-cloud/secret-manager`, Secret Manager API |
| Doppler | SaaS | `doppler` CLI, `DOPPLER_TOKEN` |
| Infisical | SaaS/Self-hosted | `@infisical/sdk`, `INFISICAL_TOKEN` |
| 1Password CLI | CLI | `op://` references, `OP_SERVICE_ACCOUNT_TOKEN` |
| dotenv-vault | File-based | `.env.vault`, `DOTENV_KEY` |
| SOPS | Encryption | `.sops.yaml`, encrypted YAML/JSON files |
| Sealed Secrets | Kubernetes | `SealedSecret` CRD, `kubeseal` |

### Input Validation Libraries

| Ecosystem | Libraries |
|-----------|-----------|
| JS/TS | `zod`, `joi`, `yup`, `valibot`, `class-validator`, `ajv`, `typebox` |
| Python | `pydantic`, `marshmallow`, `cerberus`, `voluptuous` |
| Java | `hibernate-validator` (JSR 380), `jakarta.validation` |
| Go | `github.com/go-playground/validator`, `ozzo-validation` |
| Ruby | `dry-validation`, `activemodel validations` |
| .NET | `FluentValidation`, Data Annotations |

### Dependency Vulnerability Scanning

| Tool | Type | Detection Pattern |
|------|------|-------------------|
| Snyk | SaaS | `.snyk`, `snyk` in CI, `SNYK_TOKEN` |
| Dependabot | GitHub | `.github/dependabot.yml` |
| Renovate | Self-hosted/SaaS | `renovate.json`, `renovate.json5` |
| Socket | SaaS | Socket CI integration, `socket.yml` |
| npm audit | Built-in | `npm audit` in CI scripts |
| pip-audit | CLI | `pip-audit` in CI scripts |
| Bandit | CLI (Python) | `bandit` in CI, `.bandit` config |
| Semgrep | CLI/SaaS | `.semgrep.yml`, semgrep in CI |
| Trivy | CLI | `trivy` in CI, Trivy config |
| OWASP Dependency-Check | CLI | `dependency-check` in CI |
| Brakeman | CLI (Ruby) | `brakeman` in CI, `.brakeman.yml` |
| gosec | CLI (Go) | `gosec` in CI |
| bundler-audit | CLI (Ruby) | `bundler-audit` in CI |

### Common Anti-Patterns

#### Critical Severity

| Anti-Pattern | Detection | Impact |
|-------------|-----------|--------|
| Hardcoded secrets in source | Regex for API keys, passwords, tokens in code | Credential exposure |
| JWT `alg: none` accepted | Algorithm validation config | Authentication bypass |
| SQL injection via concatenation | String concatenation with SQL keywords | Data breach |
| `eval()` with user input | `eval`, `exec`, `Function()` with dynamic args | Remote code execution |
| Missing authentication on routes | Unprotected route handlers | Unauthorized access |
| Hardcoded credentials | Username/password in source | Account compromise |

#### High Severity

| Anti-Pattern | Detection | Impact |
|-------------|-----------|--------|
| Wildcard CORS (`*`) | `Access-Control-Allow-Origin: *` | Cross-origin attacks |
| Missing HTTPS enforcement | No HSTS, HTTP links in config | Data interception |
| No CSRF protection | Missing CSRF tokens/middleware | Cross-site request forgery |
| No rate limiting | Missing rate limit middleware | Brute force, DoS |
| Weak password hashing | MD5, SHA1, unsalted hashes | Password cracking |
| Missing input validation | No validation before DB operations | Injection attacks |
| Disabled security headers | Explicitly disabled or missing headers | Various attacks |
| Logging sensitive data | Passwords, tokens in log output | Information exposure |

#### Medium Severity

| Anti-Pattern | Detection | Impact |
|-------------|-----------|--------|
| Debug mode in production | `DEBUG=True`, `NODE_ENV=development` in deploy | Information disclosure |
| Deprecated auth libraries | Lucia, old passport strategies | Unmaintained security |
| Missing error handling | Unhandled promise rejections, bare except | Information leakage |
| Overly permissive file uploads | No file type/size validation | Malware upload |
| Missing session rotation | No session regeneration on login | Session fixation |
| Verbose error messages | Stack traces in API responses | Information disclosure |
| Missing Content-Security-Policy | No CSP header | XSS attacks |
| Insecure cookie settings | Missing HttpOnly, Secure, SameSite | Session hijacking |
| No account lockout | Unlimited login attempts | Brute force |
| Missing audit logging | No logging of auth events | Forensic gaps |
| Outdated TLS configuration | TLS 1.0/1.1, weak ciphers | Protocol attacks |
| Missing CORS configuration | No CORS policy defined | Unexpected access |
