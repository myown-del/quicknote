## 1. Use Case (Interactor) Rules

* Each **use case (interactor)** MUST represent **one application action** (e.g. *CreateNote*, *UpdateNote*).
* Use cases MUST be **independent** of each other.
* Use cases MUST NOT inherit from other use cases or base interactor classes.
* Use cases MUST be **thin**:

  * orchestrate workflow
  * call domain services
  * coordinate repositories
* Use cases MUST NOT contain reusable business logic shared with other use cases.
* Use cases MAY:

  * fetch entities
  * call domain services
  * persist entities
  * raise application-level exceptions

## 2. Application Service Rules

* Business logic reused by multiple use cases MUST be extracted into **application services**.
* Application services:

  * MAY depend on repository interfaces
  * MUST NOT depend on frameworks or infrastructure
* Application services MUST NOT orchestrate full workflows.
* Application services MUST be reusable and independently testable.

## 3. Repository Rules

* Repositories MUST:

  * expose persistence operations only
  * be defined as interfaces in the application/domain layer
* Repositories MUST NOT:

  * contain business rules
  * perform validation unrelated to persistence
* Repositories MUST NOT call other repositories.


## 4. Dependency Direction Rules

* Dependencies MUST point inward:

  * Infrastructure → Application → Domain
* Domain layer MUST NOT depend on:

  * frameworks
  * databases
  * async frameworks
* Application layer MAY depend on:

  * domain layer
  * repository interfaces

---

## 5. Naming Rules

* Use cases MUST be named as verbs:

  * `CreateNoteInteractor`
  * `UpdateNoteInteractor`
* Domain services MUST describe business intent:

  * `KeywordNoteService`
  * `NoteKeywordSyncService`
* Avoid generic names: `Utils`, `Helpers`, `BaseService`

## 6. Design Principle to Follow

> Prefer **composition over inheritance**
> Keep **use cases thin**
> Make **business rules explicit and reusable**

## 7. Development rules
- For new features we always write new tests. Integration tests are priority.
- If we refactor or update old features we should check for tests that need to be rewritten with these features.
