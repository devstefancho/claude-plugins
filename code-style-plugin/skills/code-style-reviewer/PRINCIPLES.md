# Code Style Principles - 상세 가이드

## 1. 단일책임원칙 (Single Responsibility Principle - SRP)

### 개념
"하나의 클래스나 함수는 하나의 변경 이유만 가져야 한다"

### 왜 중요한가?
- 코드 이해와 유지보수가 쉬워집니다
- 테스트가 간단해집니다
- 재사용성이 높아집니다
- 변경 영향도가 최소화됩니다

### 체크리스트
- [ ] 함수가 한 가지 작업만 수행하는가?
- [ ] 함수가 여러 이유로 변경될 가능성이 있는가?
- [ ] 클래스가 여러 책임을 가지고 있는가?
- [ ] 함수의 이름이 무엇을 하는지 정확히 설명하는가?
- [ ] 함수를 한 문장으로 설명할 수 있는가?

### 나쁜 예
```typescript
// 여러 책임을 가진 함수
function processUserOrder(userId: string, items: Item[]) {
  // 1. 사용자 검증
  const user = validateUser(userId);

  // 2. 주문 생성
  const order = createOrder(user, items);

  // 3. 결제 처리
  processPayment(order);

  // 4. 이메일 발송
  sendEmail(user.email, "Order confirmed");

  // 5. 로깅
  logTransaction(order);
}
```

### 좋은 예
```typescript
// 각 함수가 하나의 책임만 가짐
function processUserOrder(userId: string, items: Item[]) {
  const user = validateUser(userId);
  const order = createOrder(user, items);
  handlePayment(order);
  notifyUser(user, order);
  recordTransaction(order);
}

// 결제만 담당
function handlePayment(order: Order): void {
  processPayment(order);
}

// 알림만 담당
function notifyUser(user: User, order: Order): void {
  sendEmail(user.email, "Order confirmed");
}

// 로깅만 담당
function recordTransaction(order: Order): void {
  logTransaction(order);
}
```

---

## 2. DRY (Don't Repeat Yourself)

### 개념
"같은 코드는 한 번만 작성해야 한다"

### 왜 중요한가?
- 버그 수정이 한 곳에서만 필요합니다
- 코드가 간결해집니다
- 유지보수 비용이 감소합니다
- 일관성이 보장됩니다

### 체크리스트
- [ ] 반복되는 패턴이나 로직이 있는가?
- [ ] 유사한 함수들이 통합될 수 있는가?
- [ ] 공통 로직이 유틸리티 함수로 추출되었는가?
- [ ] 복사-붙여넣기한 코드가 있는가?
- [ ] 같은 정규식이나 로직이 여러 곳에 있는가?

### 나쁜 예
```typescript
// 반복되는 검증 로직
function createUser(email: string, name: string) {
  if (!email || email.length === 0) {
    throw new Error("Email is required");
  }
  if (!name || name.length === 0) {
    throw new Error("Name is required");
  }
  // 사용자 생성...
}

function createPost(title: string, content: string) {
  if (!title || title.length === 0) {
    throw new Error("Title is required");
  }
  if (!content || content.length === 0) {
    throw new Error("Content is required");
  }
  // 포스트 생성...
}
```

### 좋은 예
```typescript
// 검증 로직을 한 곳에서 관리
function validateRequired(value: string, fieldName: string): void {
  if (!value || value.length === 0) {
    throw new Error(`${fieldName} is required`);
  }
}

function createUser(email: string, name: string) {
  validateRequired(email, "Email");
  validateRequired(name, "Name");
  // 사용자 생성...
}

function createPost(title: string, content: string) {
  validateRequired(title, "Title");
  validateRequired(content, "Content");
  // 포스트 생성...
}
```

---

## 3. 단순화 우선 (Simplicity First)

### 개념
"복잡한 추상화보다는 이해하기 쉬운 단순한 코드를 우선한다"

### 왜 중요한가?
- 새로운 팀원이 빨리 코드를 이해합니다
- 버그가 적어집니다
- 유지보수가 쉬워집니다
- 과도한 설계를 피합니다

### 체크리스트
- [ ] 코드를 읽고 쉽게 이해할 수 있는가?
- [ ] 불필요한 추상화가 있는가?
- [ ] 깊은 중첩이 있는가? (3단계 이상)
- [ ] 과도하게 우아한(clever) 코드가 있는가?
- [ ] 한 줄의 코드로 너무 많은 작업을 하는가?

### 나쁜 예
```typescript
// 불필요한 추상화와 복잡성
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

// 깊은 중첩
if (user) {
  if (user.isActive) {
    if (user.permissions) {
      if (user.permissions.includes('admin')) {
        // 실제 작업
      }
    }
  }
}
```

### 좋은 예
```typescript
// 단순하고 명확한 구현
function doubleNumbers(obj: Record<string, any>): Record<string, any> {
  return Object.entries(obj).reduce((acc, [key, value]) => {
    acc[key] = typeof value === 'number' ? value * 2 : value;
    return acc;
  }, {} as Record<string, any>);
}

// Early return으로 중첩 제거
function checkAdminPermission(user: User): boolean {
  if (!user) return false;
  if (!user.isActive) return false;
  if (!user.permissions) return false;
  return user.permissions.includes('admin');
}

// 더 나은 방식
function isAdmin(user: User): boolean {
  return user?.isActive && user?.permissions?.includes('admin') ?? false;
}
```

---

## 4. YAGNI (You Aren't Gonna Need It)

### 개념
"현재 필요하지 않은 기능은 구현하지 않는다"

### 왜 중요한가?
- 코드 복잡도를 낮춥니다
- 유지보수해야 할 코드의 양을 줄입니다
- 미래 변경에 더 유연하게 대응합니다
- 불필요한 버그의 원인을 제거합니다

### 체크리스트
- [ ] 사용되지 않는 코드가 있는가?
- [ ] 사용되지 않는 매개변수가 있는가?
- [ ] "나중에 필요할 것 같아서" 추가한 기능이 있는가?
- [ ] 테스트되지 않는 코드가 있는가?
- [ ] 주석 처리된 코드가 있는가?

### 나쁜 예
```typescript
// 사용되지 않는 기능과 매개변수
interface UserService {
  // 현재는 사용하지 않지만, 나중에 필요할 것 같아서 추가
  createUser(email: string, name: string, preferredLanguage?: string): User;
  updateUser(id: string, data: Partial<User>): User;
  deleteUser(id: string): void;
  // 나중에 필요할 것 같아서 추가
  suspendUser(id: string, reason: string): User;
  archiveUser(id: string): User;
}

function getUserFullInfo(userId: string, includeAnalytics?: boolean, includeHistory?: boolean, includeFuturePredictions?: boolean) {
  // 현재는 includeAnalytics와 includeFuturePredictions를 사용하지 않음
  const user = getUser(userId);
  // ...
}
```

### 좋은 예
```typescript
// 필요한 기능만 구현
interface UserService {
  createUser(email: string, name: string): User;
  updateUser(id: string, data: Partial<User>): User;
  deleteUser(id: string): void;
  // 필요해지면 그때 추가
}

function getUserFullInfo(userId: string) {
  const user = getUser(userId);
  // 필요한 정보만 반환
  return {
    id: user.id,
    email: user.email,
    name: user.name
  };
}

// 미래에 필요하면 그때 추가
function getUserWithAnalytics(userId: string) {
  const user = getUser(userId);
  const analytics = getAnalytics(userId);
  return { ...user, analytics };
}
```

---

## 5. 타입 안전성 (Type Safety)

### 개념
"`any` 타입을 피하고, 명확한 타입 정의를 사용한다" (TypeScript)

### 왜 중요한가?
- 런타임 에러를 개발 단계에서 발견합니다
- IDE의 자동완성이 정확해집니다
- 코드 리팩토링이 안전합니다
- 의도가 명확해집니다

### 체크리스트
- [ ] `any` 타입이 사용되었는가?
- [ ] 함수의 매개변수에 타입이 모두 정의되었는가?
- [ ] 함수의 반환 타입이 명시되었는가?
- [ ] 객체의 모양이 `interface`로 정의되었는가?
- [ ] `unknown` 타입을 사용할 때 타입 가드가 있는가?

### 나쁜 예
```typescript
// any 타입 남용
function processData(data: any): any {
  return data.map((item: any) => {
    return {
      ...item,
      value: item.value * 2
    };
  });
}

// 타입이 없는 반환값
function getUserData(id) {
  // ...
  return user;
}

// 암묵적 any
function filterItems(items, predicate) {
  return items.filter(predicate);
}
```

### 좋은 예
```typescript
// 명확한 타입 정의
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

// 명시적 반환 타입
interface User {
  id: string;
  email: string;
  name: string;
}

function getUserData(id: string): User {
  // ...
  return user;
}

// 제네릭으로 유연성 유지
function filterItems<T>(items: T[], predicate: (item: T) => boolean): T[] {
  return items.filter(predicate);
}

// unknown을 사용할 때는 타입 가드 필수
function process(data: unknown): void {
  if (typeof data === 'string') {
    console.log(data.toUpperCase());
  } else if (Array.isArray(data)) {
    console.log(data.length);
  }
}
```

---

## 6. 명명규칙 (Naming Conventions)

### 개념
"코드는 인간을 위해 작성되며, 명확한 이름이 코드의 의도를 전달한다"

### 체크리스트
- [ ] 변수명이 의미있고 명확한가?
- [ ] 함수명이 동사로 시작하는가?
- [ ] 클래스명이 명사이고 PascalCase인가?
- [ ] 상수가 UPPER_SNAKE_CASE인가?
- [ ] 명명규칙이 일관성 있는가?

### 나쁜 예
```typescript
// 의미없는 이름
const x = 10;
const temp = userData;
const fn = (a) => a * 2;

// 일관성 없는 명명
const max_count = 100;
const itemTotal = 50;
const MaxValue = 200;

// 너무 긴 이름
const userDataForProcessingAndStorageButNotForDeletionOrModification = user;
```

### 좋은 예
```typescript
// 명확한 이름
const maxRetries = 10;
const userProfile = userData;
const doubleNumber = (value: number) => value * 2;

// 일관성 있는 명명 (camelCase for variables/functions)
const maxCount = 100;
const itemTotal = 50;
const maxValue = 200;

// 적절한 길이
const userForProcessing = user;
```

### 명명 규칙 요약

| 대상 | 규칙 | 예시 |
|------|------|------|
| 변수 | camelCase | `userName`, `isActive`, `itemCount` |
| 함수 | camelCase + 동사 | `getUserData`, `validateEmail`, `calculateTotal` |
| 클래스 | PascalCase | `UserService`, `ValidationHelper`, `ApiClient` |
| 상수 | UPPER_SNAKE_CASE | `MAX_RETRY`, `DEFAULT_TIMEOUT`, `API_KEY` |
| 파일 | lowercase + kebab-case | `user-service.ts`, `api-client.ts` |
| 인터페이스 | PascalCase + I prefix (선택) | `IUser` 또는 `User` |
| Enum | PascalCase | `UserStatus`, `PaymentMethod` |

---

## 종합 체크리스트

코드 리뷰 시 확인할 항목들:

### 구조 (Structure)
- [ ] 함수/클래스가 하나의 책임만 가지는가? (SRP)
- [ ] 반복되는 코드가 추출되었는가? (DRY)
- [ ] 코드가 간단하고 이해하기 쉬운가? (Simplicity)

### 기능 (Functionality)
- [ ] 필요한 기능만 구현되었는가? (YAGNI)
- [ ] 사용되지 않는 코드가 없는가?
- [ ] 타입이 안전하게 정의되었는가? (Type Safety)

### 스타일 (Style)
- [ ] 명명규칙이 일관성 있는가?
- [ ] 코드 형식이 일관성 있는가?
- [ ] 주석이 적절히 작성되었는가?

### 테스트 (Testing)
- [ ] 함수가 테스트 가능한 크기인가?
- [ ] 엣지 케이스가 처리되었는가?
- [ ] 에러 처리가 적절한가?
