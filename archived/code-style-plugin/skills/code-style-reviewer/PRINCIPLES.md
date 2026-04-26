# Code Style Principles - Detailed Guide

## 1. Single Responsibility Principle (SRP)

### Concept
"A class or function should have only one reason to change"

### Why is it important?
- Makes code easier to understand and maintain
- Simplifies testing
- Increases reusability
- Minimizes change impact

### Checklist
- [ ] Does the function perform only one task?
- [ ] Could the function change for multiple reasons?
- [ ] Does the class have multiple responsibilities?
- [ ] Does the function name accurately describe what it does?
- [ ] Can you describe the function in one sentence?

### Bad Example
```typescript
// Function with multiple responsibilities
function processUserOrder(userId: string, items: Item[]) {
  // 1. User validation
  const user = validateUser(userId);

  // 2. Create order
  const order = createOrder(user, items);

  // 3. Process payment
  processPayment(order);

  // 4. Send email
  sendEmail(user.email, "Order confirmed");

  // 5. Logging
  logTransaction(order);
}
```

### Good Example
```typescript
// Each function has only one responsibility
function processUserOrder(userId: string, items: Item[]) {
  const user = validateUser(userId);
  const order = createOrder(user, items);
  handlePayment(order);
  notifyUser(user, order);
  recordTransaction(order);
}

// Handles only payment
function handlePayment(order: Order): void {
  processPayment(order);
}

// Handles only notification
function notifyUser(user: User, order: Order): void {
  sendEmail(user.email, "Order confirmed");
}

// Handles only logging
function recordTransaction(order: Order): void {
  logTransaction(order);
}
```

---

## 2. DRY (Don't Repeat Yourself)

### Concept
"The same code should be written only once"

### Why is it important?
- Bug fixes are needed in only one place
- Code becomes more concise
- Maintenance costs decrease
- Consistency is guaranteed

### Checklist
- [ ] Are there repeating patterns or logic?
- [ ] Can similar functions be consolidated?
- [ ] Has common logic been extracted into utility functions?
- [ ] Is there copy-pasted code?
- [ ] Is the same regex or logic in multiple places?

### Bad Example
```typescript
// Repeated validation logic
function createUser(email: string, name: string) {
  if (!email || email.length === 0) {
    throw new Error("Email is required");
  }
  if (!name || name.length === 0) {
    throw new Error("Name is required");
  }
  // Create user...
}

function createPost(title: string, content: string) {
  if (!title || title.length === 0) {
    throw new Error("Title is required");
  }
  if (!content || content.length === 0) {
    throw new Error("Content is required");
  }
  // Create post...
}
```

### Good Example
```typescript
// Manage validation logic in one place
function validateRequired(value: string, fieldName: string): void {
  if (!value || value.length === 0) {
    throw new Error(`${fieldName} is required`);
  }
}

function createUser(email: string, name: string) {
  validateRequired(email, "Email");
  validateRequired(name, "Name");
  // Create user...
}

function createPost(title: string, content: string) {
  validateRequired(title, "Title");
  validateRequired(content, "Content");
  // Create post...
}
```

---

## 3. Simplicity First

### Concept
"Prefer simple, easy-to-understand code over complex abstractions"

### Why is it important?
- New team members understand code quickly
- Fewer bugs
- Easier maintenance
- Avoids over-engineering

### Checklist
- [ ] Can you read and easily understand the code?
- [ ] Are there unnecessary abstractions?
- [ ] Is there deep nesting? (3+ levels)
- [ ] Is there overly clever code?
- [ ] Does a single line do too many things?

### Bad Example
```typescript
// Unnecessary abstraction and complexity
interface Strategy {
  execute(data: any): any;
}

class ComplexStrategy implements Strategy {
  execute = (data) => {
    return [data].reduce((acc, val) => ({
      ...acc,
      ...Object.entries(val).reduce((a, [k, v]) =>
        ({ ...a, [k]: typeof v === 'number' ? v * 2 : v }), {})
    }), {});
  };
}

// Deep nesting
if (user) {
  if (user.isActive) {
    if (user.permissions) {
      if (user.permissions.includes('admin')) {
        // Actual work
      }
    }
  }
}
```

### Good Example
```typescript
// Simple and clear implementation
function doubleNumbers(obj: Record<string, any>): Record<string, any> {
  return Object.entries(obj).reduce((acc, [key, value]) => {
    acc[key] = typeof value === 'number' ? value * 2 : value;
    return acc;
  }, {} as Record<string, any>);
}

// Remove nesting with early return
function checkAdminPermission(user: User): boolean {
  if (!user) return false;
  if (!user.isActive) return false;
  if (!user.permissions) return false;
  return user.permissions.includes('admin');
}

// Even better approach
function isAdmin(user: User): boolean {
  return user?.isActive && user?.permissions?.includes('admin') ?? false;
}
```

---

## 4. YAGNI (You Aren't Gonna Need It)

### Concept
"Don't implement features that are not currently needed"

### Why is it important?
- Reduces code complexity
- Reduces the amount of code to maintain
- Enables more flexible response to future changes
- Eliminates sources of unnecessary bugs

### Checklist
- [ ] Is there unused code?
- [ ] Are there unused parameters?
- [ ] Are there features added "just in case"?
- [ ] Is there untested code?
- [ ] Is there commented-out code?

### Bad Example
```typescript
// Unused features and parameters
interface UserService {
  // Currently not used but added "just in case"
  createUser(email: string, name: string, preferredLanguage?: string): User;
  updateUser(id: string, data: Partial<User>): User;
  deleteUser(id: string): void;
  // Added "just in case"
  suspendUser(id: string, reason: string): User;
  archiveUser(id: string): User;
}

function getUserFullInfo(userId: string, includeAnalytics?: boolean, includeHistory?: boolean, includeFuturePredictions?: boolean) {
  // Currently not using includeAnalytics and includeFuturePredictions
  const user = getUser(userId);
  // ...
}
```

### Good Example
```typescript
// Implement only needed features
interface UserService {
  createUser(email: string, name: string): User;
  updateUser(id: string, data: Partial<User>): User;
  deleteUser(id: string): void;
  // Add when needed
}

function getUserFullInfo(userId: string) {
  const user = getUser(userId);
  // Return only needed information
  return {
    id: user.id,
    email: user.email,
    name: user.name
  };
}

// Add when needed in the future
function getUserWithAnalytics(userId: string) {
  const user = getUser(userId);
  const analytics = getAnalytics(userId);
  return { ...user, analytics };
}
```

---

## 5. Type Safety

### Concept
"Avoid `any` type and use clear type definitions" (TypeScript)

### Why is it important?
- Catch runtime errors during development
- IDE autocomplete becomes accurate
- Code refactoring is safe
- Intent becomes clear

### Checklist
- [ ] Is `any` type used?
- [ ] Do all function parameters have types defined?
- [ ] Are return types explicit?
- [ ] Are object shapes defined with `interface`?
- [ ] When using `unknown` type, are there type guards?

### Bad Example
```typescript
// any type overuse
function processData(data: any): any {
  return data.map((item: any) => {
    return {
      ...item,
      value: item.value * 2
    };
  });
}

// Function without types
function getUserData(id) {
  // ...
  return user;
}

// Implicit any
function filterItems(items, predicate) {
  return items.filter(predicate);
}
```

### Good Example
```typescript
// Clear type definitions
interface DataItem {
  id: string;
  value: number;
  name: string;
}

function processData(data: DataItem[]): DataItem[] {
  return data.map(item => ({
    ...item,
    value: item.value * 2
  }));
}

// Explicit return type
interface User {
  id: string;
  email: string;
  name: string;
}

function getUserData(id: string): User {
  // ...
  return user;
}

// Maintain flexibility with generics
function filterItems<T>(items: T[], predicate: (item: T) => boolean): T[] {
  return items.filter(predicate);
}

// Type guards required when using unknown
function process(data: unknown): void {
  if (typeof data === 'string') {
    console.log(data.toUpperCase());
  } else if (Array.isArray(data)) {
    console.log(data.length);
  }
}
```

---

## 6. Naming Conventions

### Concept
"Code is written for humans, and clear names convey the intent of the code"

### Checklist
- [ ] Are variable names meaningful and clear?
- [ ] Do function names start with verbs?
- [ ] Are class names nouns in PascalCase?
- [ ] Are constants in UPPER_SNAKE_CASE?
- [ ] Are naming conventions consistent?

### Bad Example
```typescript
// Meaningless names
const x = 10;
const temp = userData;
const fn = (a) => a * 2;

// Inconsistent naming
const max_count = 100;
const itemTotal = 50;
const MaxValue = 200;

// Name too long
const userDataForProcessingAndStorageButNotForDeletionOrModification = user;
```

### Good Example
```typescript
// Clear names
const maxRetries = 10;
const userProfile = userData;
const doubleNumber = (value: number) => value * 2;

// Consistent naming (camelCase for variables/functions)
const maxCount = 100;
const itemTotal = 50;
const maxValue = 200;

// Appropriate length
const userForProcessing = user;
```

### Naming Convention Summary

| Target | Rule | Example |
|--------|------|---------|
| Variable | camelCase | `userName`, `isActive`, `itemCount` |
| Function | camelCase + verb | `getUserData`, `validateEmail`, `calculateTotal` |
| Class | PascalCase | `UserService`, `ValidationHelper`, `ApiClient` |
| Constant | UPPER_SNAKE_CASE | `MAX_RETRY`, `DEFAULT_TIMEOUT`, `API_KEY` |
| File | lowercase + kebab-case | `user-service.ts`, `api-client.ts` |
| Interface | PascalCase + I prefix (optional) | `IUser` or `User` |
| Enum | PascalCase | `UserStatus`, `PaymentMethod` |

---

## Comprehensive Checklist

Items to check during code review:

### Structure
- [ ] Do functions/classes have only one responsibility? (SRP)
- [ ] Has repeated code been extracted? (DRY)
- [ ] Is the code simple and easy to understand? (Simplicity)

### Functionality
- [ ] Are only needed features implemented? (YAGNI)
- [ ] Is there no unused code?
- [ ] Are types safely defined? (Type Safety)

### Style
- [ ] Are naming conventions consistent?
- [ ] Is code formatting consistent?
- [ ] Are comments appropriately written?

### Testing
- [ ] Is the function size testable?
- [ ] Are edge cases handled?
- [ ] Is error handling appropriate?
