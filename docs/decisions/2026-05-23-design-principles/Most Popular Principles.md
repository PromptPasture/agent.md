# Most Popular Principles

These principles are skills disguised as rules.
While they are written as strict rules, applying them in the real world requires deep judgment, balance, and practice.

## Why they are Skills

* Context matters: Blindly following them as absolute rules leads to over-engineered, complex code.
* Trade-offs: You must learn when to break one principle to satisfy another (e.g., DRY vs. KISS).
* Nuance: Knowing how and when to apply them to a specific problem is a craft learned over time.

## Why they look like Rules

* Guardrails: They serve as strict guidelines for beginners to prevent common architectural mistakes.
* Common language: They give teams a shared standard to evaluate code quality during reviews.

## SOLID

* SRP (Single Responsibility Principle): A class should have only one reason to change.
* OCP (Open/Closed Principle): Software entities should be open for extension but closed for modification.
* LSP (Liskov Substitution Principle): Subclasses must be substitutable for their superclasses without breaking the system.
* ISP (Interface Segregation Principle): Clients should not be forced to depend on interfaces they do not use.
* DIP (Dependency Inversion Principle): High-level modules should depend on abstractions, not on low-level details.

## Other principals

* DRY (Don't Repeat Yourself): Every piece of knowledge or logic must have a single, unambiguous representation within a system to prevent duplicate code.
* KISS (Keep It Simple, Stupid): Systems work best if they are kept simple rather than made complicated; avoid over-engineering and unnecessary complexity.
* YAGNI (You Aren't Gonna Need It): Do not add functionality or code until it is absolutely necessary, preventing wasted time and bloated codebases.
* Law of Demeter (Principle of Least Knowledge): A module or object should not know about the internal details of the objects it manipulates; "talk to friends, not strangers."
* Composition Over Inheritance: Achieve polymorphic behavior and code reuse by combining objects (has-a) rather than inheriting from a base class (is-a).
* Boy Scout Rule: Always leave the code cleaner than you found it, promoting continuous, incremental improvement of the codebase.
* CQS (Command-Query Separation): A method should either perform an action (command) or return data (query), but never both at the same time.
* SoC (Separation of Concerns): Divide a computer program into distinct sections, where each section addresses a separate, specific feature or aspect.
