# Code Quality Examples

Real-world examples demonstrating DRY, KISS, and CLEAN CODE principles in practical scenarios.

## Example 1: User Authentication Module

### Scenario: User Login and Registration Logic

#### ❌ Before: Violates DRY and CLEAN CODE

```javascript
// auth.js
export function loginUser(email, password) {
  // Validate email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    throw new Error('Invalid email format');
  }

  // Validate password
  if (!password || password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }

  // Authenticate
  const user = database.findUserByEmail(email);
  if (!user) {
    throw new Error('User not found');
  }

  if (!bcrypt.compareSync(password, user.passwordHash)) {
    throw new Error('Invalid password');
  }

  return generateToken(user);
}

export function registerUser(email, password, confirmPassword) {
  // Validate email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    throw new Error('Invalid email format');
  }

  // Validate password
  if (!password || password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }

  // Validate confirm password
  if (password !== confirmPassword) {
    throw new Error('Passwords do not match');
  }

  // Check if user exists
  const existingUser = database.findUserByEmail(email);
  if (existingUser) {
    throw new Error('Email already registered');
  }

  // Create user
  const passwordHash = bcrypt.hashSync(password, 10);
  return database.createUser({
    email,
    passwordHash
  });
}
```

**Issues**:
- Email validation duplicated (DRY violation)
- Password validation duplicated (DRY violation)
- Error messages not consistent
- Unclear variable names (emailRegex could be EMAIL_REGEX)
- Magic number 8 for password length (CLEAN CODE)
- Magic number 10 for bcrypt rounds (CLEAN CODE)

#### ✅ After: DRY, KISS, CLEAN CODE

```javascript
// auth.js
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const MIN_PASSWORD_LENGTH = 8;
const BCRYPT_ROUNDS = 10;

function validateEmail(email) {
  if (!EMAIL_REGEX.test(email)) {
    throw new Error('Invalid email format');
  }
}

function validatePassword(password) {
  if (!password || password.length < MIN_PASSWORD_LENGTH) {
    throw new Error(`Password must be at least ${MIN_PASSWORD_LENGTH} characters`);
  }
}

export async function loginUser(email, password) {
  validateEmail(email);
  validatePassword(password);

  const user = database.findUserByEmail(email);
  if (!user) {
    throw new Error('User not found');
  }

  const isPasswordValid = bcrypt.compareSync(password, user.passwordHash);
  if (!isPasswordValid) {
    throw new Error('Invalid password');
  }

  return generateToken(user);
}

export async function registerUser(email, password, confirmPassword) {
  validateEmail(email);
  validatePassword(password);

  if (password !== confirmPassword) {
    throw new Error('Passwords do not match');
  }

  const existingUser = database.findUserByEmail(email);
  if (existingUser) {
    throw new Error('Email already registered');
  }

  const passwordHash = bcrypt.hashSync(password, BCRYPT_ROUNDS);
  return database.createUser({ email, passwordHash });
}
```

**Improvements**:
- ✅ DRY: Email and password validation extracted to reusable functions
- ✅ CLEAN CODE: Magic values (8, 10) defined as named constants
- ✅ CLEAN CODE: Variable names are clear (isPasswordValid vs implicit boolean)
- ✅ KISS: Functions are shorter and focused
- ✅ DRY: Validation logic centralized

---

## Example 2: E-commerce Order Processing

### Scenario: Calculating Order Total with Taxes, Discounts, and Shipping

#### ❌ Before: Violates KISS and CLEAN CODE

```javascript
function calc(items, c, s, t) {
  let st = items.reduce((a, b) => a + (b.p * b.q), 0);
  let d = 0;

  if (c) {
    if (c.type === 1) d = st * (c.val / 100);
    else if (c.type === 2) d = c.val;
    else if (c.type === 3 && c.minAmount && st > c.minAmount) {
      d = st * (c.val / 100);
    }
  }

  let sh = s ? (st > 100 ? 0 : 15) : 0;
  let tx = t ? ((st - d + sh) * 0.1) : 0;

  return {
    st: st,
    d: d,
    sh: sh,
    tx: tx,
    tt: st - d + sh + tx
  };
}
```

**Issues**:
- Cryptic parameter names (c, s, t, items)
- Cryptic variable names (st, d, sh, tx, tt)
- Magic numbers without explanation (1, 2, 3, 100, 15, 0.1)
- Over-nested conditions (KISS violation)
- No documentation about what the function does
- Return object has abbreviated keys
- Hard to understand discount logic

#### ✅ After: KISS and CLEAN CODE

```javascript
/**
 * Calculates order total including taxes, discounts, and shipping
 * @param {Object[]} items - Array of {price, quantity}
 * @param {Object} discount - Optional {type, value, minAmount}
 * @param {boolean} includeShipping - Whether to add shipping cost
 * @param {boolean} includeTax - Whether to add sales tax
 * @returns {Object} Order summary with breakdown
 */
function calculateOrderTotal(items, discount = null, includeShipping = true, includeTax = true) {
  const SHIPPING_COST = 15;
  const FREE_SHIPPING_THRESHOLD = 100;
  const TAX_RATE = 0.1;

  // Calculate subtotal
  const subtotal = items.reduce((total, item) => {
    return total + (item.price * item.quantity);
  }, 0);

  // Calculate discount
  const discountAmount = calculateDiscount(subtotal, discount);

  // Calculate shipping
  const shippingCost = calculateShipping(subtotal, includeShipping);

  // Calculate tax (applies to subtotal after discount + shipping)
  const taxableAmount = subtotal - discountAmount + shippingCost;
  const taxAmount = includeTax ? taxableAmount * TAX_RATE : 0;

  const total = subtotal - discountAmount + shippingCost + taxAmount;

  return {
    subtotal,
    discountAmount,
    shippingCost,
    taxAmount,
    total
  };
}

function calculateDiscount(subtotal, discount) {
  if (!discount) return 0;

  const PERCENTAGE_DISCOUNT = 'percentage';
  const FIXED_DISCOUNT = 'fixed';
  const TIERED_DISCOUNT = 'tiered';

  switch (discount.type) {
    case PERCENTAGE_DISCOUNT:
      return subtotal * (discount.value / 100);

    case FIXED_DISCOUNT:
      return discount.value;

    case TIERED_DISCOUNT:
      const meetsMinimum = discount.minAmount && subtotal > discount.minAmount;
      return meetsMinimum ? subtotal * (discount.value / 100) : 0;

    default:
      return 0;
  }
}

function calculateShipping(subtotal, includeShipping) {
  const SHIPPING_COST = 15;
  const FREE_SHIPPING_THRESHOLD = 100;

  if (!includeShipping) return 0;
  return subtotal > FREE_SHIPPING_THRESHOLD ? 0 : SHIPPING_COST;
}
```

**Improvements**:
- ✅ CLEAN CODE: Descriptive function and parameter names
- ✅ CLEAN CODE: Magic numbers extracted to named constants
- ✅ CLEAN CODE: Clear documentation with JSDoc
- ✅ KISS: Complex nested logic extracted to separate functions
- ✅ CLEAN CODE: Return object has meaningful property names
- ✅ CLEAN CODE: Discount types defined as constants instead of magic numbers

---

## Example 3: Data Validation Utilities

### Scenario: Form Field Validation

#### ❌ Before: Violates DRY

```javascript
// validationUtils.js
export function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

export function validatePassword(password) {
  return password && password.length >= 8;
}

export function validatePhone(phone) {
  const regex = /^(\+1)?(\d{3})[-.]?(\d{3})[-.]?(\d{4})$/;
  return regex.test(phone);
}

// userForm.js
function handleUserSubmit(userData) {
  if (!userData.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(userData.email)) {
    return { error: 'Invalid email' };
  }

  if (!userData.password || userData.password.length < 8) {
    return { error: 'Password too short' };
  }

  if (!userData.phone || !/^(\+1)?(\d{3})[-.]?(\d{3})[-.]?(\d{4})$/.test(userData.phone)) {
    return { error: 'Invalid phone' };
  }

  return { success: true };
}

// billingForm.js
function handleBillingSubmit(billingData) {
  if (!billingData.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(billingData.email)) {
    return { error: 'Invalid email' };
  }

  if (!billingData.phone || !/^(\+1)?(\d{3})[-.]?(\d{3})[-.]?(\d{4})$/.test(billingData.phone)) {
    return { error: 'Invalid phone' };
  }

  return { success: true };
}
```

**Issues**:
- Validation utilities exist but aren't used (DRY violation)
- Regex patterns duplicated in multiple files (DRY violation)
- Validation logic scattered across components
- No centralized validation error handling

#### ✅ After: DRY, Reusable Validators

```javascript
// validationUtils.js
const VALIDATORS = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE: /^(\+1)?(\d{3})[-.]?(\d{3})[-.]?(\d{4})$/,
  STRONG_PASSWORD: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/
};

const MIN_PASSWORD_LENGTH = 8;

export const validators = {
  email: (value) => VALIDATORS.EMAIL.test(value),
  password: (value) => value && value.length >= MIN_PASSWORD_LENGTH,
  phone: (value) => VALIDATORS.PHONE.test(value),
  required: (value) => !!value && value.trim() !== ''
};

export function validateForm(data, rules) {
  const errors = {};

  Object.entries(rules).forEach(([field, validatorFn]) => {
    if (!validatorFn(data[field])) {
      errors[field] = `Invalid ${field}`;
    }
  });

  return Object.keys(errors).length === 0
    ? { success: true }
    : { error: errors };
}

// userForm.js
import { validators, validateForm } from './validationUtils';

function handleUserSubmit(userData) {
  return validateForm(userData, {
    email: validators.email,
    password: validators.password,
    phone: validators.phone
  });
}

// billingForm.js
import { validators, validateForm } from './validationUtils';

function handleBillingSubmit(billingData) {
  return validateForm(billingData, {
    email: validators.email,
    phone: validators.phone
  });
}
```

**Improvements**:
- ✅ DRY: Regex patterns defined once in VALIDATORS object
- ✅ DRY: Validation logic centralized in reusable functions
- ✅ CLEAN CODE: Named constants for validation rules
- ✅ KISS: Simple validator functions composed together
- ✅ DRY: Generic validateForm handles all form validation

---

## Example 4: API Response Handling

### Scenario: Consistent Error and Success Response Handling

#### ❌ Before: Violates DRY and CLEAN CODE

```javascript
// userService.js
export async function getUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      console.error('HTTP error', response.status);
      return { data: null, error: 'Failed to fetch user' };
    }
    const data = await response.json();
    return { data, error: null };
  } catch (err) {
    console.error('Request failed', err);
    return { data: null, error: 'Network error' };
  }
}

// productService.js
export async function getProduct(id) {
  try {
    const response = await fetch(`/api/products/${id}`);
    if (!response.ok) {
      console.error('HTTP error', response.status);
      return { data: null, error: 'Failed to fetch product' };
    }
    const data = await response.json();
    return { data, error: null };
  } catch (err) {
    console.error('Request failed', err);
    return { data: null, error: 'Network error' };
  }
}

// orderService.js
export async function createOrder(orderData) {
  try {
    const response = await fetch('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderData)
    });
    if (!response.ok) {
      console.error('HTTP error', response.status);
      return { data: null, error: 'Failed to create order' };
    }
    const data = await response.json();
    return { data, error: null };
  } catch (err) {
    console.error('Request failed', err);
    return { data: null, error: 'Network error' };
  }
}
```

**Issues**:
- Error handling pattern repeated in every function (DRY violation)
- Try-catch-response handling duplicated (DRY violation)
- Generic error messages ("Network error", "Failed to fetch")
- No distinction between HTTP errors and network errors

#### ✅ After: DRY with Centralized API Handling

```javascript
// apiClient.js
/**
 * Centralized API request handler with consistent error handling
 */
export async function apiCall(url, options = {}) {
  try {
    const response = await fetch(url, options);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new APIError(
        `HTTP ${response.status}: ${response.statusText}`,
        response.status,
        errorData
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new APIError('Network request failed', null, error);
  }
}

export class APIError extends Error {
  constructor(message, statusCode = null, details = null) {
    super(message);
    this.name = 'APIError';
    this.statusCode = statusCode;
    this.details = details;
  }
}

/**
 * Wraps async functions to return {data, error} format
 */
export async function handleAPIRequest(asyncFn) {
  try {
    const data = await asyncFn();
    return { data, error: null };
  } catch (error) {
    const errorMessage = error instanceof APIError
      ? error.message
      : 'Unexpected error';
    return { data: null, error: errorMessage };
  }
}

// userService.js
import { apiCall, handleAPIRequest } from './apiClient';

export const userService = {
  getUser: (id) => handleAPIRequest(() => apiCall(`/api/users/${id}`)),
  updateUser: (id, data) => handleAPIRequest(() =>
    apiCall(`/api/users/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
  )
};

// productService.js
import { apiCall, handleAPIRequest } from './apiClient';

export const productService = {
  getProduct: (id) => handleAPIRequest(() => apiCall(`/api/products/${id}`)),
  listProducts: () => handleAPIRequest(() => apiCall('/api/products'))
};

// orderService.js
import { apiCall, handleAPIRequest } from './apiClient';

export const orderService = {
  createOrder: (orderData) => handleAPIRequest(() =>
    apiCall('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderData)
    })
  )
};
```

**Improvements**:
- ✅ DRY: API request and error handling centralized in apiClient
- ✅ DRY: All services use the same apiCall and handleAPIRequest
- ✅ CLEAN CODE: APIError class provides clear error structure
- ✅ CLEAN CODE: Service functions are concise and readable
- ✅ KISS: Error handling logic is simple and consistent
- ✅ CLEAN CODE: Consistent {data, error} response format

---

## Summary

These examples demonstrate how applying DRY, KISS, and CLEAN CODE principles makes code:
- **More maintainable** - Changes in one place affect all usages
- **More readable** - Intent is clear, naming is descriptive
- **Less error-prone** - Less duplicated code means fewer places to fix bugs
- **Easier to test** - Centralized logic is easier to unit test
- **Easier to extend** - Adding new features doesn't require duplicating existing patterns
