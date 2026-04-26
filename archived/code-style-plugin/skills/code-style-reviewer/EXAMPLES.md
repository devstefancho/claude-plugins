# Code Style Examples - Good Code vs Bad Code

## TypeScript / JavaScript Examples

### Example 1: Single Responsibility Principle (SRP)

#### ❌ Bad Example
```typescript
class UserManager {
  // Has multiple responsibilities: user data, validation, storage, email sending

  async createUser(userData: any) {
    // 1. Validation
    if (!userData.email) throw new Error("Email required");
    if (!userData.name) throw new Error("Name required");
    if (userData.email.length < 5) throw new Error("Invalid email");

    // 2. Data transformation
    const user = {
      id: Math.random().toString(),
      email: userData.email,
      name: userData.name,
      createdAt: new Date(),
      role: 'user'
    };

    // 3. Storage
    const db = require('./db');
    db.save('users', user);

    // 4. Email sending
    const mailer = require('nodemailer');
    await mailer.send({
      to: user.email,
      subject: 'Welcome',
      html: `<h1>Welcome ${user.name}</h1>`
    });

    // 5. Logging
    console.log(`User created: ${user.id}`);
    const logger = require('./logger');
    logger.log('user_created', { userId: user.id, email: user.email });

    return user;
  }
}
```

#### ✅ Good Example
```typescript
// Separate responsibilities
class UserValidator {
  validate(userData: UserInput): void {
    if (!userData.email) throw new Error("Email required");
    if (!userData.name) throw new Error("Name required");
    if (!this.isValidEmail(userData.email)) throw new Error("Invalid email");
  }

  private isValidEmail(email: string): boolean {
    return email.includes('@') && email.length >= 5;
  }
}

class UserFactory {
  create(userData: UserInput): User {
    return {
      id: this.generateId(),
      email: userData.email,
      name: userData.name,
      createdAt: new Date(),
      role: 'user'
    };
  }

  private generateId(): string {
    return Math.random().toString();
  }
}

class UserRepository {
  async save(user: User): Promise<void> {
    const db = require('./db');
    await db.save('users', user);
  }
}

class UserNotificationService {
  async notifyNewUser(user: User): Promise<void> {
    const mailer = require('nodemailer');
    await mailer.send({
      to: user.email,
      subject: 'Welcome',
      html: `<h1>Welcome ${user.name}</h1>`
    });
  }
}

class UserLogger {
  logCreation(user: User): void {
    const logger = require('./logger');
    logger.log('user_created', { userId: user.id, email: user.email });
  }
}

class UserService {
  constructor(
    private validator: UserValidator,
    private factory: UserFactory,
    private repository: UserRepository,
    private notificationService: UserNotificationService,
    private logger: UserLogger
  ) {}

  async createUser(userData: UserInput): Promise<User> {
    this.validator.validate(userData);
    const user = this.factory.create(userData);
    await this.repository.save(user);
    await this.notificationService.notifyNewUser(user);
    this.logger.logCreation(user);
    return user;
  }
}
```

---

### Example 2: DRY (Don't Repeat Yourself)

#### ❌ Bad Example
```typescript
// Repeated validation logic
function validateUserEmail(email: string): boolean {
  if (!email) return false;
  if (email.trim().length === 0) return false;
  if (!email.includes('@')) return false;
  return true;
}

function validateProductEmail(email: string): boolean {
  if (!email) return false;
  if (email.trim().length === 0) return false;
  if (!email.includes('@')) return false;
  return true;
}

function validateOrganizationEmail(email: string): boolean {
  if (!email) return false;
  if (email.trim().length === 0) return false;
  if (!email.includes('@')) return false;
  return true;
}

// Repeated API call pattern
async function getUsersFromAPI(apiKey: string): Promise<any> {
  const response = await fetch('https://api.example.com/users', {
    headers: { 'Authorization': `Bearer ${apiKey}` }
  });
  if (!response.ok) throw new Error('API Error');
  return response.json();
}

async function getProductsFromAPI(apiKey: string): Promise<any> {
  const response = await fetch('https://api.example.com/products', {
    headers: { 'Authorization': `Bearer ${apiKey}` }
  });
  if (!response.ok) throw new Error('API Error');
  return response.json();
}

async function getOrdersFromAPI(apiKey: string): Promise<any> {
  const response = await fetch('https://api.example.com/orders', {
    headers: { 'Authorization': `Bearer ${apiKey}` }
  });
  if (!response.ok) throw new Error('API Error');
  return response.json();
}
```

#### ✅ Good Example
```typescript
// Common validation function
function isValidEmail(email: string): boolean {
  if (!email) return false;
  if (email.trim().length === 0) return false;
  return email.includes('@');
}

// Reuse everywhere
const isUserEmailValid = isValidEmail(userEmail);
const isProductEmailValid = isValidEmail(productEmail);
const isOrgEmailValid = isValidEmail(orgEmail);

// Common API client
class ApiClient {
  constructor(private apiKey: string, private baseUrl: string) {}

  async fetch<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      headers: { 'Authorization': `Bearer ${this.apiKey}` }
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return response.json();
  }
}

// Usage
const apiClient = new ApiClient(apiKey, 'https://api.example.com');
const users = await apiClient.fetch<User[]>('/users');
const products = await apiClient.fetch<Product[]>('/products');
const orders = await apiClient.fetch<Order[]>('/orders');
```

---

### Example 3: Simplicity First

#### ❌ Bad Example
```typescript
// Unnecessary abstraction and complex logic
interface DataProcessor {
  process(data: any[]): any[];
}

class ComplexDataProcessor implements DataProcessor {
  process = (data: any[]): any[] =>
    [data]
      .reduce((acc: any, val: any) =>
        [val]
          .reduce((a: any, item: any) =>
            [item]
              .reduce((b: any, i: any) =>
                ({
                  ...b,
                  ...Object.entries(i).reduce((c: any, [k, v]: any) =>
                    ({
                      ...c,
                      [k]: typeof v === 'number' ? v * 2 : v
                    }), {})
                }), {}), [])[0], {});
}

// Deep nesting
function checkPermissions(user: User): boolean {
  if (user) {
    if (user.isActive) {
      if (user.roles) {
        if (user.roles.length > 0) {
          if (user.roles.some((role: Role) => role.name === 'admin')) {
            if (user.roles[0].permissions) {
              if (user.roles[0].permissions.includes('create_user')) {
                return true;
              }
            }
          }
        }
      }
    }
  }
  return false;
}
```

#### ✅ Good Example
```typescript
// Simple and clear implementation
function doubleNumbers<T extends Record<string, any>>(data: T[]): T[] {
  return data.map(item => {
    const result = { ...item };
    Object.entries(result).forEach(([key, value]) => {
      if (typeof value === 'number') {
        result[key] = value * 2;
      }
    });
    return result;
  });
}

// Remove nesting with early return
function hasCreateUserPermission(user: User): boolean {
  if (!user?.isActive) return false;
  if (!user.roles || user.roles.length === 0) return false;

  const adminRole = user.roles.find(role => role.name === 'admin');
  return adminRole?.permissions?.includes('create_user') ?? false;
}

// Optional chaining and nullish coalescing
function canCreateUser(user: User): boolean {
  return user?.isActive &&
         user?.roles?.some(r => r.name === 'admin' && r.permissions?.includes('create_user')) ?? false;
}
```

---

### Example 4: YAGNI (You Aren't Gonna Need It)

#### ❌ Bad Example
```typescript
// Unused features
interface UserService {
  // Currently used: required
  getUser(id: string): Promise<User>;
  createUser(email: string, name: string): Promise<User>;

  // Not used: added "just in case"
  archiveUser(id: string): Promise<void>;
  restoreUser(id: string): Promise<void>;
  bulkCreateUsers(users: UserInput[]): Promise<User[]>;
  exportUsersToCSV(filter?: any): Promise<string>;
  generateUserReport(startDate: Date, endDate: Date): Promise<Report>;
  predictChurn(userId: string): Promise<number>;
}

// Unused parameters
function fetchUserData(
  userId: string,
  includeProfilePicture?: boolean,  // Not used
  includeFollowers?: boolean,        // Not used
  analyzeActivity?: boolean,         // Not used
  includeFuturePreferences?: boolean // Not used
): User {
  const user = getUser(userId);
  // Only uses userId and basic info
  return user;
}

// Commented-out code
function saveData(data: any) {
  // const oldWay = JSON.stringify(data);
  // localStorage.setItem('data', oldWay);

  // if (someLegacyCondition) {
  //   sendToOldServer(data);
  // }

  sendToNewServer(data);
}
```

#### ✅ Good Example
```typescript
// Define only needed features
interface UserService {
  getUser(id: string): Promise<User>;
  createUser(email: string, name: string): Promise<User>;
  // Add later when needed
}

// Only needed parameters
function fetchUserData(userId: string): User {
  return getUser(userId);
}

// Add as a new function when needed later
function fetchUserWithFollowers(userId: string): UserWithFollowers {
  const user = getUser(userId);
  const followers = getFollowers(userId);
  return { ...user, followers };
}

// Clean code: remove commented-out code
function saveData(data: any) {
  sendToNewServer(data);
}
```

---

### Example 5: Type Safety

#### ❌ Bad Example
```typescript
// any type overuse
function processData(data: any): any {
  return data.map((item: any) => {
    return {
      name: item.name,
      value: item.value * 2
    };
  });
}

// Function without types
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Implicit any
function filterData(array, key, value) {
  return array.filter(item => item[key] === value);
}

// Wrong type usage
type UserData = {
  [key: string]: any  // Same as any
};

const user: UserData = {
  name: 'John',
  age: 30,
  email: true  // Cannot type check
};
```

#### ✅ Good Example
```typescript
// Clear type definitions
interface DataItem {
  name: string;
  value: number;
}

function processData(data: DataItem[]): DataItem[] {
  return data.map(item => ({
    name: item.name,
    value: item.value * 2
  }));
}

// Explicit types and return type
interface CartItem {
  price: number;
  quantity: number;
}

function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// Maintain flexibility with generics
function filterByProperty<T>(
  array: T[],
  key: keyof T,
  value: T[keyof T]
): T[] {
  return array.filter(item => item[key] === value);
}

// Clear type definition
interface User {
  name: string;
  age: number;
  email: string;
}

const user: User = {
  name: 'John',
  age: 30,
  email: 'john@example.com'
};

// Safe handling with unknown
function process(data: unknown): void {
  if (typeof data === 'string') {
    console.log(data.toUpperCase());
  } else if (typeof data === 'number') {
    console.log(data * 2);
  } else if (Array.isArray(data)) {
    console.log(data.length);
  }
}
```

---

### Example 6: Naming Conventions

#### ❌ Bad Example
```typescript
// Meaningless names
const x = 10;
const temp = user;
const tmp1 = calculateTotal(items);
const a = getData();
const fn = (b) => b * 2;

// Inconsistent naming
const max_count = 100;
const itemTotal = 50;
const MaxValue = 200;
const user_status = 'active';

// Name too long
const userDataThatWillBeProcessedAndStoredButNotDeletedOrModifiedInAnyWayShapeOrForm = user;

// Abbreviation overuse
const usr = getUser();
const adr = getAddress();
const phn = getPhone();
const nps = calculateScore();

// Inaccurate names
const userData = items;  // userData but stores items?
const getTotalPrice = () => items.length;  // getTotalPrice but returns length?
```

#### ✅ Good Example
```typescript
// Clear names
const maxRetries = 10;
const userProfile = user;
const cartTotal = calculateTotal(items);
const userData = getData();
const doubleValue = (value: number) => value * 2;

// Consistent naming (camelCase)
const maxCount = 100;
const itemTotal = 50;
const maxValue = 200;
const userStatus = 'active';

// Appropriate length names
const userForProcessing = user;

// Use complete names
const user = getUser();
const address = getAddress();
const phone = getPhone();
const netPromoterScore = calculateScore();

// Accurate names
const cartItems = items;
const totalPrice = items.reduce((sum, item) => sum + item.price, 0);
```

---

## Function Size Comparison

### ❌ Bad Example - Function too large
```typescript
// Function over 50 lines
async function handleUserRegistration(request: any) {
  const { email, password, firstName, lastName, phone, address, city, state, zip, country, dateOfBirth, acceptTerms } = request.body;

  if (!email) throw new Error('Email is required');
  if (!password) throw new Error('Password is required');
  // ... more validation

  const hashedPassword = await hashPassword(password);
  const user = {
    email,
    password: hashedPassword,
    firstName,
    lastName,
    phone,
    address,
    city,
    state,
    zip,
    country,
    dateOfBirth,
    acceptTerms,
    createdAt: new Date(),
    lastLogin: null,
    isActive: true,
    preferences: {}
  };

  const existingUser = await db.findUser(email);
  if (existingUser) throw new Error('User already exists');

  await db.save('users', user);

  const emailToken = generateToken();
  await db.save('email_tokens', { userId: user.id, token: emailToken });

  const mailer = require('nodemailer');
  await mailer.send({
    to: email,
    subject: 'Verify your email',
    html: `<a href="...">Verify</a>`
  });

  // ... more code

  return { success: true, userId: user.id };
}
```

### ✅ Good Example - Small, focused functions
```typescript
async function handleUserRegistration(request: RegisterRequest): Promise<RegisterResponse> {
  const userData = request.body;

  validateUserInput(userData);
  const existingUser = await userRepository.findByEmail(userData.email);
  if (existingUser) throw new Error('User already exists');

  const user = await userService.registerUser(userData);
  await emailService.sendVerificationEmail(user);

  return { success: true, userId: user.id };
}

// Each function does one thing
function validateUserInput(userData: UserInput): void {
  if (!userData.email) throw new Error('Email is required');
  if (!userData.password) throw new Error('Password is required');
}

async function registerUser(userData: UserInput): Promise<User> {
  const hashedPassword = await hashPassword(userData.password);
  return userRepository.save({ ...userData, password: hashedPassword });
}

async function sendVerificationEmail(user: User): Promise<void> {
  const token = generateToken();
  await tokenRepository.save({ userId: user.id, token });
  await mailer.send({
    to: user.email,
    subject: 'Verify your email',
    html: `<a href="...">Verify</a>`
  });
}
```

---

## Comprehensive Example: Real Improvement Case

### Requirements
"Write a product order processing function"

#### ❌ Bad Implementation (30+ lines)
```typescript
async function processOrder(orderData: any) {
  // SRP violation: multiple responsibilities
  // DRY violation: repeated validation
  // YAGNI violation: unnecessary features
  // Naming convention: inconsistent
  // Type safety: any usage

  if (!orderData) throw new Error("Order data required");
  if (!orderData.userId) throw new Error("User ID required");
  if (!orderData.items || orderData.items.length === 0) throw new Error("Items required");

  let total = 0;
  for (let i = 0; i < orderData.items.length; i++) {
    if (!orderData.items[i].productId) throw new Error("Product ID required");
    if (!orderData.items[i].quantity || orderData.items[i].quantity <= 0) throw new Error("Quantity must be > 0");

    const product = await getProduct(orderData.items[i].productId);
    total += product.price * orderData.items[i].quantity;
  }

  if (total <= 0) throw new Error("Total must be > 0");

  const user = await getUser(orderData.userId);
  if (!user) throw new Error("User not found");

  const order = {
    id: Math.random().toString(),
    userId: user.id,
    items: orderData.items,
    total: total,
    status: 'pending',
    createdAt: new Date(),
    completedAt: null
  };

  const result = await db.insert('orders', order);

  const message = `Order created: ${order.id}. Total: $${total}`;
  console.log(message);

  return { orderId: order.id, total: total, message: message };
}
```

#### ✅ Good Implementation (SRP, DRY, Simplicity, YAGNI, Type Safety)
```typescript
// === Type Definitions ===
interface OrderItem {
  productId: string;
  quantity: number;
}

interface CreateOrderRequest {
  userId: string;
  items: OrderItem[];
}

interface Order {
  id: string;
  userId: string;
  items: OrderItem[];
  total: number;
  status: 'pending' | 'completed' | 'cancelled';
  createdAt: Date;
}

interface CreateOrderResponse {
  orderId: string;
  total: number;
}

// === Validation Layer (SRP: validation only) ===
class OrderValidator {
  validateCreateRequest(request: CreateOrderRequest): void {
    this.validateNotEmpty(request, 'Order data');
    this.validateNotEmpty(request.userId, 'User ID');
    this.validateItems(request.items);
  }

  private validateNotEmpty<T>(value: T, fieldName: string): void {
    if (!value) throw new Error(`${fieldName} is required`);
  }

  private validateItems(items: OrderItem[]): void {
    if (!Array.isArray(items) || items.length === 0) {
      throw new Error('At least one item is required');
    }

    items.forEach((item, index) => {
      if (!item.productId) throw new Error(`Item ${index}: Product ID is required`);
      if (!item.quantity || item.quantity <= 0) throw new Error(`Item ${index}: Quantity must be > 0`);
    });
  }
}

// === Pricing Layer (SRP: calculation only, DRY: removes duplicate logic) ===
class OrderPricingService {
  async calculateTotal(items: OrderItem[]): Promise<number> {
    let total = 0;

    for (const item of items) {
      const product = await this.getProduct(item.productId);
      total += product.price * item.quantity;
    }

    return total;
  }

  private async getProduct(productId: string): Promise<{ price: number }> {
    return getProduct(productId);  // External function call
  }
}

// === Order Creation Layer (SRP: order creation only) ===
class OrderFactory {
  create(userId: string, items: OrderItem[], total: number): Order {
    return {
      id: this.generateId(),
      userId,
      items,
      total,
      status: 'pending',
      createdAt: new Date()
    };
  }

  private generateId(): string {
    return `order_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

// === Repository Layer (SRP: storage only) ===
class OrderRepository {
  async save(order: Order): Promise<void> {
    await db.insert('orders', order);
  }

  async findById(orderId: string): Promise<Order | null> {
    return db.findById('orders', orderId);
  }
}

// === Main Service (orchestration only) ===
class OrderService {
  constructor(
    private validator: OrderValidator,
    private pricingService: OrderPricingService,
    private factory: OrderFactory,
    private repository: OrderRepository
  ) {}

  async createOrder(request: CreateOrderRequest): Promise<CreateOrderResponse> {
    // 1. Validate
    this.validator.validateCreateRequest(request);

    // 2. Verify user
    const user = await getUser(request.userId);
    if (!user) throw new Error('User not found');

    // 3. Calculate price
    const total = await this.pricingService.calculateTotal(request.items);

    // 4. Create order
    const order = this.factory.create(request.userId, request.items, total);

    // 5. Save
    await this.repository.save(order);

    // 6. Response
    return {
      orderId: order.id,
      total: order.total
    };
  }
}

// === Usage Example ===
const orderService = new OrderService(
  new OrderValidator(),
  new OrderPricingService(),
  new OrderFactory(),
  new OrderRepository()
);

const response = await orderService.createOrder({
  userId: 'user123',
  items: [
    { productId: 'prod1', quantity: 2 },
    { productId: 'prod2', quantity: 1 }
  ]
});
```

**Improvements:**

1. **SRP**: Each class has only one responsibility
2. **DRY**: Validation logic defined in one place
3. **Simplicity**: Main logic is clear and easy to read
4. **YAGNI**: Only needed features implemented
5. **Type Safety**: Clear type definitions for all functions
6. **Naming Conventions**: Consistent naming
7. **Testability**: Each class can be tested independently

---

Use these examples as references when writing and reviewing code!
