# Component Design Examples

## 리뷰 출력 형식 (필수)

이 형식을 따라 리포트를 작성할 것:

```
# Component Design Review Report

## 파일: src/components/Example.tsx

### 좋은 점
- TypeScript를 사용하여 타입 안전성 확보
- 컴포넌트 명명이 명확함

### Critical Issues
**문제 1: [원칙명] 위반**
- 위치: 컴포넌트/함수명
- 설명: 구체적인 문제 설명
- 개선 방법: 해결 방안 제시

### Warnings
- 경고 내용 (개선이 필요함)

### Suggestions
- 제안 내용 (고려해볼 만함)

## 종합 평가
- 전체 컴포넌트 설계 점수: X/10
- 가장 중요한 개선 사항:
  1. 첫 번째 개선점
  2. 두 번째 개선점
```

---

## 1. 단일 책임 원칙 위반

### Bad: 모든 것을 하는 컴포넌트

```tsx
function UserDashboard() {
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [notifications, setNotifications] = useState([]);
  // 문제: 3개 API 호출, 3개 핸들러, 복잡한 조건부 렌더링이 한 컴포넌트에

  useEffect(() => {
    fetch('/api/user').then(/*...*/);
    fetch('/api/posts').then(/*...*/);
    fetch('/api/notifications').then(/*...*/);
  }, []);

  return (
    <div>
      {/* 헤더, 탭, 게시물 목록, 알림 목록 모두 여기서 렌더링 */}
    </div>
  );
}
```

### Good: 역할별 컴포넌트 분리

```tsx
// hooks/useUser.ts - 데이터 로직 분리
function useUser() {
  const [user, setUser] = useState(null);
  useEffect(() => { fetch('/api/user').then(/*...*/) }, []);
  return { user };
}

// components/UserDashboard.tsx - UI 조합만 담당
function UserDashboard() {
  const { user } = useUser();
  const { posts, deletePost } = usePosts();

  return (
    <div>
      <UserHeader user={user} />
      <PostList posts={posts} onDelete={deletePost} />
    </div>
  );
}
```

---

## 2. Props Drilling 문제

### Bad: 3단계 이상 Props 전달

```tsx
function App() {
  const [theme, setTheme] = useState('light');
  return (
    <Layout theme={theme}>
      <Sidebar theme={theme}>
        <Navigation theme={theme}>
          <NavItem theme={theme} /> {/* 4단계 drilling */}
        </Navigation>
      </Sidebar>
    </Layout>
  );
}
```

### Good: Context 활용

```tsx
const ThemeContext = createContext({ theme: 'light', setTheme: () => {} });

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// 어디서든 직접 접근
function NavItem() {
  const { theme } = useContext(ThemeContext);
  return <div className={theme}>Nav Item</div>;
}
```

---

## 3. 합성(Composition) 패턴

### Bad: Props로 모든 것을 전달

```tsx
function Modal({
  title, description, showFooter,
  primaryButtonText, secondaryButtonText,
  onPrimaryClick, onSecondaryClick, children
}) {
  // Props가 8개 이상, 유연성 부족
}
```

### Good: Compound Components 패턴

```tsx
function Modal({ children, isOpen, onClose }) {
  if (!isOpen) return null;
  return (
    <ModalContext.Provider value={{ onClose }}>
      <div className="modal">{children}</div>
    </ModalContext.Provider>
  );
}

Modal.Header = ({ children }) => <div className="modal-header">{children}</div>;
Modal.Body = ({ children }) => <div className="modal-body">{children}</div>;
Modal.Footer = ({ children }) => <div className="modal-footer">{children}</div>;

// 사용: 유연한 구조
<Modal isOpen={open} onClose={close}>
  <Modal.Header>제목</Modal.Header>
  <Modal.Body>내용</Modal.Body>
  <Modal.Footer><Button>확인</Button></Modal.Footer>
</Modal>
```

---

## 4. 재사용성 개선

### Bad: 하드코딩된 스타일

```tsx
function ProductCard({ product }) {
  return (
    <div style={{ padding: '16px', backgroundColor: '#ffffff' }}>
      <h3 style={{ fontSize: '18px', color: '#333333' }}>{product.name}</h3>
      <button style={{ backgroundColor: '#3b82f6' }}>Add to Cart</button>
    </div>
  );
}
```

### Good: 범용 컴포넌트 활용

```tsx
// 범용 Card 컴포넌트
function Card({ children, className }) {
  return <div className={cn('card', className)}>{children}</div>;
}
Card.Title = ({ children }) => <h3 className="card-title">{children}</h3>;

// 특화 컴포넌트
function ProductCard({ product, onAddToCart }) {
  return (
    <Card>
      <Card.Title>{product.name}</Card.Title>
      <Button variant="primary" onClick={() => onAddToCart(product)}>
        Add to Cart
      </Button>
    </Card>
  );
}
```

---

## 5. Custom Hooks 분리

### Bad: 컴포넌트 내 복잡한 로직

```tsx
function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  const loadMore = useCallback(async () => {
    // 페이지네이션 로직 30줄...
  }, [page]);

  // UI와 로직이 뒤섞임
}
```

### Good: Custom Hook으로 분리

```tsx
// hooks/useInfiniteProducts.ts
function useInfiniteProducts() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [hasMore, setHasMore] = useState(true);

  const loadMore = useCallback(async () => { /* 로직 */ }, []);

  return { products, loading, hasMore, loadMore };
}

// components/ProductList.tsx - UI만 담당
function ProductList() {
  const { products, loading, hasMore, loadMore } = useInfiniteProducts();

  return (
    <div>
      {products.map(p => <ProductCard key={p.id} product={p} />)}
      {loading && <Spinner />}
      {hasMore && <button onClick={loadMore}>Load More</button>}
    </div>
  );
}
```

