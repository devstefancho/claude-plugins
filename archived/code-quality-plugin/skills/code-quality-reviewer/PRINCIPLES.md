# Code Quality Principles

Detailed reference for the three core code quality principles assessed by the Code Quality Reviewer skill.

## 1. DRY (Don't Repeat Yourself)

**Definition**: Avoid code duplication. Any knowledge should exist in only one place, reducing maintenance burden and minimizing bugs.

**Why It Matters**:
- Duplicated code creates maintenance nightmares (fix one place, forget another)
- Increases bug introduction risk when updates are missed
- Makes code harder to understand (which version is correct?)
- Wastes development time on repeated implementations

### DRY Violation Patterns

#### Pattern 1: Copy-Pasted Functions
```javascript
// ❌ BAD: Duplicated validation logic
function validateUserEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

function validateSubscriberEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}
```

**Fix**: Extract to shared utility
```javascript
// ✅ GOOD: Single source of truth
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validateEmail(email) {
  return EMAIL_REGEX.test(email);
}
```

#### Pattern 2: Repeated Conditional Logic
```javascript
// ❌ BAD: Same condition checked multiple times
if (user.role === 'admin' || user.role === 'moderator') {
  showAdminPanel();
}

if (user.role === 'admin' || user.role === 'moderator') {
  enableDeletion();
}
```

**Fix**: Extract permission check
```javascript
// ✅ GOOD: Centralized permission logic
function isPrivileged(user) {
  return user.role === 'admin' || user.role === 'moderator';
}

if (isPrivileged(user)) {
  showAdminPanel();
}

if (isPrivileged(user)) {
  enableDeletion();
}
```

#### Pattern 3: Duplicated Error Handling
```javascript
// ❌ BAD: Same error handling everywhere
try {
  const data = await fetchData();
  process(data);
} catch (error) {
  console.error('API Error:', error.message);
  notifyUser('Something went wrong');
}

try {
  const result = await saveData();
  confirm(result);
} catch (error) {
  console.error('API Error:', error.message);
  notifyUser('Something went wrong');
}
```

**Fix**: Extract error handler
```javascript
// ✅ GOOD: Reusable error handler
async function handleAPICall(asyncFn) {
  try {
    return await asyncFn();
  } catch (error) {
    console.error('API Error:', error.message);
    notifyUser('Something went wrong');
  }
}
```

### DRY Checklist
- [ ] Are similar functions combining logic that could be shared?
- [ ] Are conditional patterns repeated across the codebase?
- [ ] Are constants (regex, magic numbers) defined in multiple places?
- [ ] Are helper functions reused appropriately?
- [ ] Are error handling patterns consistent and centralized?

---

## 2. KISS (Keep It Simple, Stupid)

**Definition**: Prefer simple, straightforward solutions over complex ones. Avoid over-engineering.

**Why It Matters**:
- Simple code is easier to understand and maintain
- Complex solutions increase cognitive load and bug risk
- Complex abstractions often aren't needed until proven necessary
- Over-engineering wastes time on premature optimization

### KISS Violation Patterns

#### Pattern 1: Over-Complex Function Logic
```javascript
// ❌ BAD: Overly complex nested conditions
function getDiscount(user, purchase) {
  return user.isPremium
    ? purchase.amount > 1000
      ? user.loyalty > 5
        ? purchase.amount * 0.20
        : purchase.amount * 0.15
      : purchase.amount * 0.10
    : purchase.amount > 5000
      ? purchase.amount * 0.05
      : 0;
}
```

**Fix**: Simplify with explicit conditions
```javascript
// ✅ GOOD: Clear, step-by-step logic
function getDiscount(user, purchase) {
  if (!user.isPremium) {
    return purchase.amount > 5000 ? purchase.amount * 0.05 : 0;
  }

  if (purchase.amount > 1000 && user.loyalty > 5) {
    return purchase.amount * 0.20;
  }

  if (purchase.amount > 1000) {
    return purchase.amount * 0.15;
  }

  return purchase.amount * 0.10;
}
```

#### Pattern 2: Unnecessary Abstraction
```javascript
// ❌ BAD: Over-engineered factory pattern
class UserFactory {
  static create(userData) {
    return new UserBuilder()
      .setName(userData.name)
      .setEmail(userData.email)
      .setRole(userData.role)
      .build();
  }
}

class UserBuilder {
  setName(name) { this.name = name; return this;; }
  setEmail(email) { this.email = email; return this; }
  setRole(role) { this.role = role; return this; }
  build() { return new User(this.name, this.email, this.role); }
}
```

**Fix**: Use simple constructor
```javascript
// ✅ GOOD: Direct instantiation
class User {
  constructor(name, email, role) {
    this.name = name;
    this.email = email;
    this.role = role;
  }
}

const user = new User(userData.name, userData.email, userData.role);
```

#### Pattern 3: Too Many Function Parameters
```javascript
// ❌ BAD: Function signature too complex
function generateReport(userId, startDate, endDate, format,
                       includeDetails, groupBy, sortBy,
                       filterActive, exportPath) {
  // 9 parameters - hard to remember order and meaning
}
```

**Fix**: Use configuration object
```javascript
// ✅ GOOD: Clear, named parameters
function generateReport(userId, options = {}) {
  const {
    startDate,
    endDate,
    format = 'PDF',
    includeDetails = false,
    groupBy = 'date',
    sortBy = 'name',
    filterActive = true,
    exportPath = './reports'
  } = options;
  // Much clearer parameter intent
}
```

### KISS Checklist
- [ ] Can any nested conditions be flattened?
- [ ] Are there unnecessary abstraction layers?
- [ ] Is there a simpler way to achieve the same result?
- [ ] Does the function have too many parameters?
- [ ] Is the code solving the actual problem or an imagined one?

---

## 3. CLEAN CODE (Easy to Read)

**Definition**: Write code that clearly expresses intent and is easy for others (and future you) to understand without extensive documentation.

**Why It Matters**:
- Code is read far more often than written
- Clear code reduces onboarding time for team members
- Self-documenting code reduces comment burden
- Easy-to-read code has fewer bugs (clear intent = fewer mistakes)

### Clean Code Violation Patterns

#### Pattern 1: Unclear Variable Names
```javascript
// ❌ BAD: Cryptic names
const d = new Date();
const ms = new Date().getTime();
const u = users.filter(x => x.a === 'active');
const p = calculatePrice(item, 0.15, 1.2, 2);
```

**Fix**: Use descriptive names
```javascript
// ✅ GOOD: Clear intent
const currentDate = new Date();
const currentTimestamp = new Date().getTime();
const activeUsers = users.filter(user => user.status === 'active');
const finalPrice = calculatePrice(item, taxRate, shippingMultiplier, quantity);
```

#### Pattern 2: Missing Documentation
```javascript
// ❌ BAD: What does this function do?
function proc(arr) {
  return arr.reduce((acc, val) => {
    const x = val.split('_')[1];
    return acc + parseInt(x, 10);
  }, 0);
}
```

**Fix**: Document intent
```javascript
// ✅ GOOD: Clear documentation
/**
 * Extracts numeric IDs from underscore-separated strings
 * and returns their sum.
 *
 * @param {string[]} items - Array of items like "prefix_123_suffix"
 * @returns {number} Sum of all extracted IDs
 */
function sumExtractedIds(items) {
  return items.reduce((total, item) => {
    const id = item.split('_')[1];
    return total + parseInt(id, 10);
  }, 0);
}
```

#### Pattern 3: Magic Values Without Explanation
```javascript
// ❌ BAD: What do these numbers mean?
if (user.age > 18 && user.creditScore > 650 && user.income > 30000) {
  approveLoan();
}

setTimeout(() => refresh(), 5000);
```

**Fix**: Use named constants
```javascript
// ✅ GOOD: Meaning is clear
const MIN_LOAN_AGE = 18;
const MIN_CREDIT_SCORE = 650;
const MIN_ANNUAL_INCOME = 30000;
const CACHE_REFRESH_MS = 5000;

if (user.age > MIN_LOAN_AGE &&
    user.creditScore > MIN_CREDIT_SCORE &&
    user.income > MIN_ANNUAL_INCOME) {
  approveLoan();
}

setTimeout(() => refresh(), CACHE_REFRESH_MS);
```

#### Pattern 4: Comments vs. Self-Documenting Code
```javascript
// ❌ BAD: Requires comments to understand
// Check if user is authorized
if (u.r === 'a' || u.r === 'm') {
  // Show admin panel
  showPanel(true);
}
```

**Fix**: Write self-documenting code
```javascript
// ✅ GOOD: Clear without comments
const isAdmin = user.role === 'admin';
const isModerator = user.role === 'moderator';

if (isAdmin || isModerator) {
  showAdminPanel();
}
```

### Clean Code Checklist
- [ ] Are variable and function names descriptive and meaningful?
- [ ] Is function purpose clear without reading implementation?
- [ ] Are magic values defined as named constants?
- [ ] Is code self-documenting (intent is obvious)?
- [ ] Are complex sections commented with "why", not "what"?
- [ ] Is code logically organized and easy to follow?
- [ ] Could a new team member understand this without asking?

---

## Assessment Guidelines

When reviewing code, apply these principles in order of importance:

1. **CLEAN CODE** - If it's unreadable, other issues become secondary
2. **DRY** - Duplication leads to maintenance problems
3. **KISS** - Unnecessary complexity creates bugs

Use these as guidelines, not strict rules. Context matters - sometimes a slightly larger, simpler function is better than a highly abstracted one.
