---
layout: home
hero:
  name: Claude Plugins
  text: Claude Code 플러그인 마켓플레이스
  tagline: Skills, Commands, Hooks, MCP Servers를 통해 Claude Code를 확장하세요
  actions:
    - theme: brand
      text: 플러그인 둘러보기
      link: /ko/plugins/
    - theme: alt
      text: 시작하기
      link: /ko/guide/getting-started
---

<HomeFeatures lang="ko" />

<div class="quick-start-section">

## 빠른 시작

<div class="quick-start-steps">
  <div class="step">
    <span class="step-number">1</span>
    <span class="step-text">마켓플레이스 등록</span>
  </div>
  <div class="step">
    <span class="step-number">2</span>
    <span class="step-text">플러그인 설치</span>
  </div>
  <div class="step">
    <span class="step-number">3</span>
    <span class="step-text">Claude Code 재시작</span>
  </div>
</div>

```bash
# Claude Code CLI 사용
/plugin marketplace add devstefancho/claude-plugins
/plugin install code-style-plugin@devstefancho-claude-plugins
```

```bash
# 또는 npx 사용 (일반 터미널에서)
npx skills add devstefancho/claude-plugins
```

[모든 플러그인 보기 →](/ko/plugins/)

</div>
