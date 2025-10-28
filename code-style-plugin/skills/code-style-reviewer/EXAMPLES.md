# Code Style Examples - 좋은 코드 vs 나쁜 코드

## TypeScript / JavaScript 예제

### 예제 1: 단일책임원칙 (SRP)

#### ❌ 나쁜 예
```typescript
class UserManager {
  // 여러 책임을 가짐: 사용자 데이터, 검증, 저장, 이메일 발송

  async createUser(userData: any) {
    // 1. 검증
    if (!userData.email) throw new Error("Email required");
    if (!userData.name) throw new Error("Name required");
    if (userData.email.length < 5) throw new Error("Invalid email");

    // 2. 데이터 변환
    const user = {
      id: Math.random().toString(),
      email: userData.email,
      name: userData.name,
      createdAt: new Date(),
      role: 'user'
    };

    // 3. 저장
    const db = require('./db');
    db.save('users', user);

    // 4. 이메일 발송
    const mailer = require('nodemailer');
    await mailer.send({
      to: user.email,
      subject: 'Welcome',
      html: `<h1>Welcome ${user.name}</h1>`
    });

    // 5. 로깅
    console.log(`User created: ${user.id}`);
    const logger = require('./logger');
    logger.log('user_created', { userId: user.id, email: user.email });

    return user;
  }
}
```

#### ✅ 좋은 예
```typescript
// 각각의 책임을 분리
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

### 예제 2: DRY (Don't Repeat Yourself)

#### ❌ 나쁜 예
```typescript
// 반복되는 검증 로직
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

// 반복되는 API 호출 패턴
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

#### ✅ 좋은 예
```typescript
// 공통 검증 함수
function isValidEmail(email: string): boolean {
  if (!email) return false;
  if (email.trim().length === 0) return false;
  return email.includes('@');
}

// 모든 곳에서 재사용
const isUserEmailValid = isValidEmail(userEmail);
const isProductEmailValid = isValidEmail(productEmail);
const isOrgEmailValid = isValidEmail(orgEmail);

// 공통 API 클라이언트
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

// 사용
const apiClient = new ApiClient(apiKey, 'https://api.example.com');
const users = await apiClient.fetch<User[]>('/users');
const products = await apiClient.fetch<Product[]>('/products');
const orders = await apiClient.fetch<Order[]>('/orders');
```

---

### 예제 3: 단순화 우선 (Simplicity First)

#### ❌ 나쁜 예
```typescript
// 불필요한 추상화와 복잡한 로직
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

// 깊은 중첩
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

#### ✅ 좋은 예
```typescript
// 단순하고 명확한 구현
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

// Early return으로 중첩 제거
function hasCreateUserPermission(user: User): boolean {
  if (!user?.isActive) return false;
  if (!user.roles || user.roles.length === 0) return false;

  const adminRole = user.roles.find(role => role.name === 'admin');
  return adminRole?.permissions?.includes('create_user') ?? false;
}

// Optional chaining과 nullish coalescing
function canCreateUser(user: User): boolean {
  return user?.isActive &&
         user?.roles?.some(r => r.name === 'admin' && r.permissions?.includes('create_user')) ?? false;
}
```

---

### 예제 4: YAGNI (You Aren't Gonna Need It)

#### ❌ 나쁜 예
```typescript
// 사용되지 않는 기능들
interface UserService {
  // 현재 사용: 필수
  getUser(id: string): Promise<User>;
  createUser(email: string, name: string): Promise<User>;

  // 사용 안 함: "나중에 필요할 것 같아서" 추가
  archiveUser(id: string): Promise<void>;
  restoreUser(id: string): Promise<void>;
  bulkCreateUsers(users: UserInput[]): Promise<User[]>;
  exportUsersToCSV(filter?: any): Promise<string>;
  generateUserReport(startDate: Date, endDate: Date): Promise<Report>;
  predictChurn(userId: string): Promise<number>;
}

// 사용되지 않는 매개변수
function fetchUserData(
  userId: string,
  includeProfilePicture?: boolean,  // 사용 안 함
  includeFollowers?: boolean,        // 사용 안 함
  analyzeActivity?: boolean,         // 사용 안 함
  includeFuturePreferences?: boolean // 사용 안 함
): User {
  const user = getUser(userId);
  // userId와 기본 정보만 사용
  return user;
}

// 주석 처리된 코드
function saveData(data: any) {
  // const oldWay = JSON.stringify(data);
  // localStorage.setItem('data', oldWay);

  // if (someLegacyCondition) {
  //   sendToOldServer(data);
  // }

  sendToNewServer(data);
}
```

#### ✅ 좋은 예
```typescript
// 필요한 기능만 정의
interface UserService {
  getUser(id: string): Promise<User>;
  createUser(email: string, name: string): Promise<User>;
  // 필요하면 나중에 추가
}

// 필요한 매개변수만
function fetchUserData(userId: string): User {
  return getUser(userId);
}

// 필요하면 나중에 새 함수로 추가
function fetchUserWithFollowers(userId: string): UserWithFollowers {
  const user = getUser(userId);
  const followers = getFollowers(userId);
  return { ...user, followers };
}

// 깔끔한 코드: 주석 처리 제거
function saveData(data: any) {
  sendToNewServer(data);
}
```

---

### 예제 5: 타입 안전성 (Type Safety)

#### ❌ 나쁜 예
```typescript
// any 타입 남용
function processData(data: any): any {
  return data.map((item: any) => {
    return {
      name: item.name,
      value: item.value * 2
    };
  });
}

// 타입이 없는 함수
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// 암묵적 any
function filterData(array, key, value) {
  return array.filter(item => item[key] === value);
}

// 잘못된 타입 사용
type UserData = {
  [key: string]: any  // 이것도 any와 마찬가지
};

const user: UserData = {
  name: 'John',
  age: 30,
  email: true  // 타입 체크 불가
};
```

#### ✅ 좋은 예
```typescript
// 명확한 타입 정의
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

// 명시적 타입과 반환형
interface CartItem {
  price: number;
  quantity: number;
}

function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// 제네릭으로 유연성 유지
function filterByProperty<T>(
  array: T[],
  key: keyof T,
  value: T[keyof T]
): T[] {
  return array.filter(item => item[key] === value);
}

// 명확한 타입 정의
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

// unknown으로 안전하게 처리
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

### 예제 6: 명명규칙 (Naming Conventions)

#### ❌ 나쁜 예
```typescript
// 의미없는 이름
const x = 10;
const temp = user;
const tmp1 = calculateTotal(items);
const a = getData();
const fn = (b) => b * 2;

// 일관성 없는 명명
const max_count = 100;
const itemTotal = 50;
const MaxValue = 200;
const user_status = 'active';

// 너무 긴 이름
const userDataThatWillBeProcessedAndStoredButNotDeletedOrModifiedInAnyWayShapeOrForm = user;

// 약어 남용
const usr = getUser();
const adr = getAddress();
const phn = getPhone();
const nps = calculateScore();

// 부정확한 이름
const userData = items;  // userData인데 items를 저장?
const getTotalPrice = () => items.length;  // getTotalPrice인데 길이를 반환?
```

#### ✅ 좋은 예
```typescript
// 명확한 이름
const maxRetries = 10;
const userProfile = user;
const cartTotal = calculateTotal(items);
const userData = getData();
const doubleValue = (value: number) => value * 2;

// 일관성 있는 명명 (camelCase)
const maxCount = 100;
const itemTotal = 50;
const maxValue = 200;
const userStatus = 'active';

// 적절한 길이의 이름
const userForProcessing = user;

// 완전한 이름 사용
const user = getUser();
const address = getAddress();
const phone = getPhone();
const netPromoterScore = calculateScore();

// 정확한 이름
const cartItems = items;
const totalPrice = items.reduce((sum, item) => sum + item.price, 0);
```

---

## 함수 크기 비교

### ❌ 나쁜 예 - 너무 큰 함수
```typescript
// 함수가 50줄 이상
async function handleUserRegistration(request: any) {
  const { email, password, firstName, lastName, phone, address, city, state, zip, country, dateOfBirth, acceptTerms } = request.body;

  if (!email) throw new Error('Email is required');
  if (!password) throw new Error('Password is required');
  // ... 더 많은 검증

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

  // ... 더 많은 코드

  return { success: true, userId: user.id };
}
```

### ✅ 좋은 예 - 작고 집중된 함수들
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

// 각 함수는 한 가지 일만 함
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

## 종합 예제: 실제 개선 사례

### 요구사항
"상품 주문 처리 함수를 작성하세요"

#### ❌ 나쁜 구현 (30줄 이상)
```typescript
async function processOrder(orderData: any) {
  // SRP 위반: 여러 책임
  // DRY 위반: 반복되는 검증
  // YAGNI 위반: 불필요한 기능
  // 명명규칙: 일관성 없음
  // 타입 안전: any 사용

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

#### ✅ 좋은 구현 (SRP, DRY, 단순화, YAGNI, 타입 안전)
```typescript
// === 타입 정의 ===
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

// === 검증 계층 (SRP: 검증만 담당) ===
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

// === 가격 계산 계층 (SRP: 계산만 담당, DRY: 중복 로직 제거) ===
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
    return getProduct(productId);  // 외부 함수 호출
  }
}

// === 주문 생성 계층 (SRP: 주문 생성만 담당) ===
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

// === 저장소 계층 (SRP: 저장만 담당) ===
class OrderRepository {
  async save(order: Order): Promise<void> {
    await db.insert('orders', order);
  }

  async findById(orderId: string): Promise<Order | null> {
    return db.findById('orders', orderId);
  }
}

// === 메인 서비스 (조율만 담당) ===
class OrderService {
  constructor(
    private validator: OrderValidator,
    private pricingService: OrderPricingService,
    private factory: OrderFactory,
    private repository: OrderRepository
  ) {}

  async createOrder(request: CreateOrderRequest): Promise<CreateOrderResponse> {
    // 1. 검증
    this.validator.validateCreateRequest(request);

    // 2. 사용자 확인
    const user = await getUser(request.userId);
    if (!user) throw new Error('User not found');

    // 3. 가격 계산
    const total = await this.pricingService.calculateTotal(request.items);

    // 4. 주문 생성
    const order = this.factory.create(request.userId, request.items, total);

    // 5. 저장
    await this.repository.save(order);

    // 6. 응답
    return {
      orderId: order.id,
      total: order.total
    };
  }
}

// === 사용 예 ===
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

**개선 사항:**

1. **SRP**: 각 클래스가 하나의 책임만 가짐
2. **DRY**: 검증 로직이 한 곳에서만 정의됨
3. **단순화**: 메인 로직이 명확하고 읽기 쉬움
4. **YAGNI**: 필요한 기능만 구현
5. **타입 안전**: 모든 함수에 명확한 타입 정의
6. **명명규칙**: 일관성 있는 네이밍
7. **테스트 용이**: 각 클래스를 독립적으로 테스트 가능

---

이 예제들을 참고하여 코드를 작성하고 검토해보세요!
