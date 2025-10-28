# Code Style Plugin - 빠른 시작 가이드

## 5분 안에 시작하기

### Step 1: 마켓플레이스 추가 (1분)

```bash
cd /Users/stefancho/works/claude-plugins
claude

# Claude Code 내에서
/plugin marketplace add ./dev-marketplace
```

### Step 2: 플러그인 설치 (2분)

```bash
/plugin install code-style-plugin@dev-marketplace
```

"Install now" 선택 후 Claude Code 재시작

### Step 3: 테스트 (2분)

코드 파일을 생성하거나 기존 파일에 대해:

```
@src/example.ts 를 코드 스타일 관점에서 분석해줄래?
```

또는

```
이 코드를 리뷰해줘. @src/services/user.ts
```

---

## 사용 예제

### 예제 1: 파일 리뷰

```
@src/controllers/userController.ts 파일의 코드 스타일을 분석해줘
```

**결과**: 5가지 원칙(SRP, DRY, 단순화, YAGNI, 타입 안전성)에 따른 상세 리뷰

### 예제 2: 함수 리뷰

```typescript
// 이 함수를 검토해줄래?
async function handleUserData(data: any) {
  if (data) {
    if (data.user) {
      if (data.user.id) {
        const userId = data.user.id;
        const user = await getUser(userId);
        if (user) {
          const posts = await getPosts(userId);
          const comments = await getComments(userId);
          const followers = await getFollowers(userId);
          return {
            user,
            posts,
            comments,
            followers,
            timestamp: new Date()
          };
        }
      }
    }
  }
  return null;
}
```

**받을 수 있는 피드백**:
- ⚠️ Deep nesting (단순화 우선)
- ⚠️ Multiple responsibilities (SRP)
- ⚠️ `any` type 사용 (타입 안전성)

---

## 주요 기능

### ✅ 자동 검사 항목

| 원칙 | 검사 내용 |
|------|---------|
| **SRP** | 함수/클래스의 책임이 하나인가? 함수 길이는 적절한가? |
| **DRY** | 반복되는 코드가 있는가? 공통 로직이 추출되어야 하는가? |
| **단순화** | 불필요한 복잡도가 있는가? 중첩이 깊은가? |
| **YAGNI** | 사용되지 않는 코드가 있는가? 불필요한 기능이 있는가? |
| **타입** | `any` 사용은? 타입이 명확히 정의되었는가? |

### 📋 추가 검사

- 명명규칙 (camelCase, PascalCase, UPPER_SNAKE_CASE)
- 함수 크기 및 복잡도
- 주석과 문서화 품질
- 에러 처리

---

## 리뷰 리포트 읽는 법

### Critical Issues (⚠️)
반드시 수정해야 할 문제
- 명확한 버그 가능성
- 심각한 코드 냄새

### Warnings (📢)
개선이 권장되는 항목
- 유지보수성 감소
- 잠재적 문제

### Suggestions (💡)
고려할 만한 제안
- 코드 개선 아이디어
- 더 나은 패턴 제안

---

## 예상 개선 전후

### Before (나쁜 코드)

```typescript
function processOrder(data: any) {
  if (!data) throw new Error("Data required");
  if (!data.items) throw new Error("Items required");

  let total = 0;
  for (let i = 0; i < data.items.length; i++) {
    const item = data.items[i];
    if (!item.price) throw new Error("Price required");
    total += item.price;
  }

  const db = require('./db');
  db.save('orders', { items: data.items, total });

  console.log(`Order: ${total}`);
  return { orderId: Math.random(), total };
}
```

### After (좋은 코드)

```typescript
interface OrderItem {
  id: string;
  price: number;
  quantity: number;
}

interface CreateOrderRequest {
  items: OrderItem[];
}

class OrderValidator {
  validateRequest(req: CreateOrderRequest): void {
    if (!req?.items?.length) throw new Error("Items required");
    req.items.forEach(item => {
      if (!item.price || item.price <= 0) throw new Error("Invalid price");
    });
  }
}

class OrderPricingService {
  calculateTotal(items: OrderItem[]): number {
    return items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  }
}

class OrderService {
  constructor(
    private validator: OrderValidator,
    private pricing: OrderPricingService,
    private repository: OrderRepository
  ) {}

  async createOrder(req: CreateOrderRequest) {
    this.validator.validateRequest(req);
    const total = this.pricing.calculateTotal(req.items);
    const order = { items: req.items, total };
    await this.repository.save(order);
    return { orderId: generateId(), total };
  }
}
```

**개선 사항**:
- ✅ 타입 안전성 강화 (any 제거)
- ✅ SRP 준수 (각 클래스 한 책임)
- ✅ 코드 단순화 (중첩 제거)
- ✅ DRY (공통 로직 추출)

---

## 자주 묻는 질문 (FAQ)

### Q: Plugin이 설치되지 않습니다
A:
1. `/plugin marketplace add ./dev-marketplace` 다시 실행
2. Claude Code 재시작
3. `/plugin install code-style-plugin@dev-marketplace` 재실행

### Q: Skill이 자동으로 활성화되지 않습니다
A:
1. Claude Code 재시작
2. "코드 리뷰", "분석", "개선" 같은 키워드 포함 요청
3. 명시적으로: "code-style-reviewer Skill을 사용해줄래?"

### Q: 특정 원칙만 검사하고 싶습니다
A:
요청 시 명시하세요:
```
SRP와 타입 안전성만 중점적으로 분석해줄래? @file.ts
```

### Q: 팀과 공유하려면?
A:
1. 플러그인 디렉토리를 Git 저장소에 커밋
2. 팀원들이 다음 명령 실행:
   ```bash
   /plugin install code-style-plugin@your-org/claude-plugins
   ```

### Q: 프로젝트별로 다른 규칙을 적용하고 싶습니다
A:
`.claude/skills/code-style-reviewer/SKILL.md`를 프로젝트별로 커스터마이징:
```bash
mkdir -p .claude/skills/code-style-reviewer
cp ~/.claude/skills/code-style-reviewer/SKILL.md .claude/skills/code-style-reviewer/
# 수정
```

---

## 다음 단계

1. **기본 사용** - 이 가이드의 예제로 시작
2. **상세 학습** - `code-style-plugin/PRINCIPLES.md` 읽기
3. **예제 분석** - `code-style-plugin/EXAMPLES.md`의 사례 학습
4. **팀 적용** - 프로젝트에 적용하고 팀과 공유
5. **커스터마이징** - SKILL.md 수정하여 팀 규칙 반영

---

## 도움말 명령어

Claude Code 내에서:

```bash
# 플러그인 확인
/plugin

# 설치된 skill 확인
/help

# 설정 열기
/config
```

---

**Happy Coding! 🚀**
