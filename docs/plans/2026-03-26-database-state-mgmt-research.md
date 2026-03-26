# Database & State Management Analyzer Research

Deep research conducted 2026-03-26 covering ORM detection, database patterns, state management libraries, and anti-patterns across all major ecosystems.

## Database Detection Checklist

### ORM Detection

#### JS/TS ORMs

| ORM | Dependencies | Config Files | Migration Tool | Migration Dir |
|-----|-------------|-------------|---------------|--------------|
| Prisma | `prisma`, `@prisma/client` | `prisma/schema.prisma` | `prisma migrate` | `prisma/migrations/` |
| Drizzle | `drizzle-orm`, `drizzle-kit` | `drizzle.config.ts` | `drizzle-kit` | `drizzle/`, `migrations/` |
| TypeORM | `typeorm` | `ormconfig.json`, `data-source.ts` | TypeORM CLI | `src/migrations/` |
| Sequelize | `sequelize`, `sequelize-cli` | `.sequelizerc` | `sequelize-cli` | `migrations/` |
| Knex | `knex` | `knexfile.js`, `knexfile.ts` | `knex migrate` | `migrations/` |
| Mongoose | `mongoose` | Schema definition files | N/A (schemaless) | N/A |
| MikroORM | `@mikro-orm/core` | `mikro-orm.config.ts` | `mikro-orm migration:*` | `src/migrations/` |
| Objection | `objection`, `knex` | `knexfile.js` | Knex migrations | `migrations/` |

#### Python ORMs

| ORM | Dependencies | Config Files | Migration Tool | Migration Dir |
|-----|-------------|-------------|---------------|--------------|
| SQLAlchemy | `sqlalchemy`, `alembic` | `alembic.ini` | Alembic | `alembic/versions/` |
| Django ORM | `django` | `settings.py` (DATABASES) | `manage.py migrate` | `*/migrations/` |
| Tortoise | `tortoise-orm`, `aerich` | `TORTOISE_ORM` config | Aerich | `migrations/` |
| SQLModel | `sqlmodel`, `alembic` | `alembic.ini` | Alembic | `alembic/versions/` |
| Peewee | `peewee` | Database initialization | `playhouse.migrate` | Manual |

#### Java ORMs

| ORM | Dependencies | Config Files | Migration Tool | Migration Dir |
|-----|-------------|-------------|---------------|--------------|
| Hibernate/JPA | `hibernate-core`, `spring-data-jpa` | `persistence.xml`, `application.yml` | Flyway/Liquibase | `db/migration/` |
| jOOQ | `jooq` | jOOQ config XML | Flyway/Liquibase | `db/migration/` |
| MyBatis | `mybatis`, `mybatis-spring-boot-starter` | `mybatis-config.xml`, mapper XML | Flyway/Liquibase | `db/migration/` |
| Exposed | `org.jetbrains.exposed` | DSL table definitions | Custom | Manual |

#### Go ORMs

| ORM | Dependencies | Config Files | Migration Tool | Migration Dir |
|-----|-------------|-------------|---------------|--------------|
| GORM | `gorm.io/gorm` | Model struct definitions | `gorm.AutoMigrate` | N/A (auto) |
| Ent | `entgo.io/ent` | `ent/schema/` | `ent migrate` | `ent/migrate/` |
| sqlx | `github.com/jmoiron/sqlx` | Raw SQL | golang-migrate | `migrations/` |
| sqlc | `github.com/sqlc-dev/sqlc` | `sqlc.yaml` | golang-migrate | `migrations/` |

#### Ruby ORMs

| ORM | Dependencies | Config Files | Migration Tool | Migration Dir |
|-----|-------------|-------------|---------------|--------------|
| Active Record | `activerecord` (Rails) | `database.yml` | `rails db:migrate` | `db/migrate/` |
| Sequel | `sequel` | Database connection config | `sequel` migrations | `db/migrations/` |

#### .NET ORMs

| ORM | Dependencies | Config Files | Migration Tool | Migration Dir |
|-----|-------------|-------------|---------------|--------------|
| EF Core | `Microsoft.EntityFrameworkCore` | `DbContext`, `appsettings.json` | `dotnet ef migrations` | `Migrations/` |
| Dapper | `Dapper` | Raw SQL | FluentMigrator/DbUp | `Migrations/` |

### Database Type Detection

| Database | Package Dependencies | URL Patterns |
|----------|---------------------|-------------|
| PostgreSQL | `pg`, `psycopg2`, `pgx`, `npgsql` | `postgresql://`, `postgres://` |
| MySQL | `mysql2`, `mysqlclient`, `go-sql-driver/mysql` | `mysql://`, `mysql2://` |
| SQLite | `better-sqlite3`, `sqlite3`, `rusqlite` | `sqlite:`, `file:` with `.db`/`.sqlite` |
| MongoDB | `mongoose`, `mongodb`, `pymongo`, `mongoid` | `mongodb://`, `mongodb+srv://` |
| Redis | `redis`, `ioredis`, `redis-py`, `go-redis` | `redis://`, `rediss://` |
| MSSQL | `mssql`, `tedious`, `pyodbc` | `mssql://`, `sqlserver://` |
| DynamoDB | `@aws-sdk/client-dynamodb`, `boto3` | AWS config, table definitions |
| Cassandra | `cassandra-driver`, `cassandra` | `cassandra://`, contact points |
| Firebase/Firestore | `firebase-admin`, `@firebase/firestore` | Firebase project config |
| Supabase | `@supabase/supabase-js`, `supabase-py` | `SUPABASE_URL`, `supabase.co` |
| Neon | `@neondatabase/serverless` | `neon://`, `*.neon.tech` |
| PlanetScale | `@planetscale/database` | `mysql://`, PlanetScale config |
| Turso | `@libsql/client`, `libsql` | `libsql://`, `*.turso.io` |
| CockroachDB | `pg` (PostgreSQL compatible) | `postgresql://`, CockroachDB config |

### Connection Pooling

| Tool | Ecosystem | Detection Pattern |
|------|-----------|-------------------|
| PgBouncer | PostgreSQL | `pgbouncer.ini`, port 6432 |
| pgpool-II | PostgreSQL | `pgpool.conf` |
| HikariCP | Java | `HikariConfig`, `spring.datasource.hikari.*` |
| node-postgres pool | Node.js | `new Pool()` from `pg` |
| SQLAlchemy pool | Python | `pool_size`, `create_engine` pool args |
| Prisma connection pool | Node.js | `connection_limit` in Prisma URL |
| c3p0 | Java | `c3p0.properties`, `c3p0-config.xml` |
| DBCP | Java | `commons-dbcp2` dependency |

### Schema Pattern Detection

| Pattern | Detection Method | Significance |
|---------|-----------------|-------------|
| UUID primary keys | `uuid` type in schema, UUID generation | Distributed-friendly IDs |
| Auto-increment | `serial`, `autoIncrement`, `IDENTITY` | Traditional sequential IDs |
| Soft deletes | `deletedAt`, `deleted_at`, `is_deleted` columns | Data preservation pattern |
| Audit fields | `createdAt`, `updatedAt`, `created_at`, `updated_at` | Change tracking |
| User audit fields | `createdBy`, `updatedBy`, `created_by`, `updated_by` | User attribution |
| Multi-tenancy | `tenantId`, `tenant_id`, `organization_id` column | Multi-tenant architecture |
| Polymorphic associations | `*_type` + `*_id` column pairs | Flexible relationships |
| Optimistic locking | `version`, `lock_version`, `@Version` | Concurrent write handling |
| Composite keys | Multiple columns in primary key | Complex key patterns |
| JSON columns | `jsonb`, `json` column types | Flexible schema data |
| Indexes | Index definitions in migrations/schema | Query optimization |
| Unique constraints | Unique index/constraint definitions | Data integrity |
| Full-text search | `tsvector`, full-text index, search config | Search capability |

### Seed Data Detection

| Indicator | Detection Pattern |
|-----------|-------------------|
| Seed directories | `seeds/`, `seeders/`, `db/seeds/` |
| Seed files | `seed.ts`, `seed.py`, `seeds.rb`, `*Seeder.php` |
| Seed scripts | `prisma db seed`, `knex seed:run`, `rails db:seed` in package.json/scripts |
| Factory patterns | `factory_bot`, `faker`, `@faker-js/faker`, `factory.define` |

---

## State Management Detection Checklist

### State Libraries (18 libraries)

| Library | Package | Config/Usage Pattern | Ecosystem |
|---------|---------|---------------------|-----------|
| Zustand | `zustand` | `create()` store | React |
| Redux Toolkit | `@reduxjs/toolkit` | `configureStore()`, slices | React |
| Jotai | `jotai` | `atom()` primitives | React |
| Recoil | `recoil` | `atom()`, `selector()` | React (Meta) |
| Valtio | `valtio` | `proxy()` state | React |
| MobX | `mobx`, `mobx-react-lite` | `makeAutoObservable()` | React |
| XState | `xstate`, `@xstate/react` | `createMachine()` | Framework-agnostic |
| Pinia | `pinia` | `defineStore()` | Vue 3 |
| Vuex | `vuex` | `createStore()` | Vue (legacy) |
| NgRx Store | `@ngrx/store` | `StoreModule.forRoot()` | Angular |
| NgRx Signal Store | `@ngrx/signals` | `signalStore()` | Angular 17+ |
| Effector | `effector` | `createStore()`, `createEvent()` | Framework-agnostic |
| Svelte Runes | Built-in (Svelte 5) | `$state()`, `$derived()` | Svelte |
| Solid Signals | Built-in (SolidJS) | `createSignal()`, `createStore()` | SolidJS |
| React Context | Built-in (React) | `createContext()`, `useContext()` | React |
| Legend State | `@legendapp/state` | `observable()` | React |
| Nanostores | `nanostores` | `atom()`, `map()` | Framework-agnostic |
| TanStack Store | `@tanstack/store` | `new Store()` | Framework-agnostic |

### Data Fetching (11 libraries)

| Library | Package | Pattern | Features |
|---------|---------|---------|----------|
| TanStack Query | `@tanstack/react-query` | `useQuery()`, `useMutation()` | Cache, retry, pagination |
| SWR | `swr` | `useSWR()` | Stale-while-revalidate |
| Apollo Client | `@apollo/client` | `useQuery()`, `gql` | GraphQL client |
| URQL | `urql`, `@urql/core` | `useQuery()` | Lightweight GraphQL |
| Relay | `react-relay` | `useLazyLoadQuery()` | Facebook GraphQL |
| tRPC | `@trpc/client`, `@trpc/server` | `trpc.*.useQuery()` | Type-safe RPC |
| Axios | `axios` | `axios.get()`, interceptors | HTTP client |
| ky | `ky` | `ky.get()` | Modern fetch wrapper |
| ofetch | `ofetch` | `$fetch()` | Nuxt/Nitro fetch |
| got | `got` | `got()` | Node.js HTTP |
| wretch | `wretch` | `wretch().get()` | Fluent fetch wrapper |

### Form State (8 libraries)

| Library | Package | Pattern | Ecosystem |
|---------|---------|---------|-----------|
| React Hook Form | `react-hook-form` | `useForm()` | React |
| Formik | `formik` | `useFormik()`, `<Formik>` | React |
| TanStack Form | `@tanstack/react-form` | `useForm()` | React/Vue/Solid |
| Zod | `zod` | `z.object()` schema | Framework-agnostic |
| Yup | `yup` | `yup.object()` schema | Framework-agnostic |
| Vee-Validate | `vee-validate` | `useForm()`, `useField()` | Vue |
| Angular Reactive Forms | `@angular/forms` | `FormGroup`, `FormControl` | Angular |
| Superforms | `sveltekit-superforms` | `superForm()` | SvelteKit |

### Real-time/WebSocket (11 libraries)

| Library | Package | Protocol | Features |
|---------|---------|----------|----------|
| Socket.IO | `socket.io`, `socket.io-client` | WebSocket + polling | Rooms, namespaces, auto-reconnect |
| Pusher | `pusher`, `pusher-js` | WebSocket | Channels, presence, managed |
| Ably | `ably` | WebSocket | Pub/sub, presence, managed |
| Supabase Realtime | `@supabase/supabase-js` | WebSocket | Postgres changes, presence |
| Firebase Realtime | `firebase/database` | WebSocket | Real-time sync, offline |
| Liveblocks | `@liveblocks/client` | WebSocket | Collaboration, CRDT |
| PartyKit | `partykit` | WebSocket | Edge runtime, durable objects |
| Native WebSocket | `WebSocket` API | WebSocket | Browser built-in |
| ws | `ws` | WebSocket | Node.js WebSocket server |
| SSE | `EventSource` API | Server-Sent Events | Unidirectional streaming |
| ActionCable | `actioncable`, `@rails/actioncable` | WebSocket | Rails integrated |

### Caching Strategies

| Strategy | Implementation | Detection Pattern |
|----------|---------------|-------------------|
| TanStack Query cache | `@tanstack/react-query` | `staleTime`, `gcTime`, `QueryClient` |
| SWR cache | `swr` | `dedupingInterval`, cache provider |
| Apollo cache | `@apollo/client` | `InMemoryCache`, cache policies |
| Redis | `redis`, `ioredis` | Cache-aside pattern, TTL settings |
| Memcached | `memcached`, `memjs` | Key-value caching patterns |
| localStorage | Browser API | `localStorage.setItem/getItem` |
| sessionStorage | Browser API | `sessionStorage.setItem/getItem` |
| IndexedDB | `idb`, `Dexie` | Structured client-side storage |
| Service Worker | `workbox`, SW registration | Request caching, offline support |
| HTTP caching | Headers | `Cache-Control`, `ETag`, `Last-Modified` |
| Next.js ISR/SSG | Next.js built-in | `revalidate`, `generateStaticParams` |

### Anti-Patterns

#### Database Anti-Patterns

| Anti-Pattern | Detection Method | Severity |
|-------------|-----------------|----------|
| N+1 queries | Loop with individual queries, no eager loading | High |
| Raw SQL injection | String concatenation with SQL keywords | Critical |
| Hardcoded connection strings | Database URLs in source code | Critical |
| Missing indexes | Foreign keys without indexes, frequent query columns unindexed | High |
| Unbounded queries | `SELECT *` without LIMIT, no pagination | High |
| Missing transactions | Multi-step writes without transaction wrapper | High |
| No connection pooling | Direct connections in high-traffic apps | Medium |
| Missing migrations | Schema changes without migration files | Medium |
| No seed data | Empty database setup, manual data entry | Low |

#### State Management Anti-Patterns

| Anti-Pattern | Detection Method | Severity |
|-------------|-----------------|----------|
| Direct state mutation | Mutating state objects directly (non-proxy) | High |
| Mixing server/client state | Server data in global state store | High |
| God components | Single component managing excessive state | Medium |
| SSR state mismatch | Hydration errors, missing server state transfer | High |
| Prop drilling | Props passed through 3+ component levels | Medium |
| Context overuse | React Context for frequently changing values | Medium |
| Missing loading states | No pending/error states for async operations | Medium |
| Stale closures | Referencing outdated state in callbacks | High |
| Unnecessary re-renders | Missing memoization, non-atomic updates | Medium |
