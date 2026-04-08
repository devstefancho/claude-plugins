<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ChevronRight, Sparkles } from 'lucide-vue-next'
import pluginData from '../../../data/plugins.json'

const props = defineProps<{
  lang?: 'ko' | 'en'
}>()

const pluginCount = pluginData.plugins.length
const categoryCount = pluginData.categories.length

const isVisible = ref(false)
onMounted(() => {
  requestAnimationFrame(() => { isVisible.value = true })
})

const labels = {
  en: {
    title: 'Claude Plugins',
    tagline: 'Extend Claude Code with community-built plugins',
    stats: `${pluginCount} plugins across ${categoryCount} categories`,
    browse: '> Browse Plugins',
    getStarted: 'Get Started',
    terminalTitle: 'Terminal',
    terminalComment: '# Install a plugin in seconds',
  },
  ko: {
    title: 'Claude Plugins',
    tagline: '커뮤니티가 만든 플러그인으로 Claude Code를 확장하세요',
    stats: `${categoryCount}개 카테고리에 ${pluginCount}개 플러그인`,
    browse: '> 플러그인 둘러보기',
    getStarted: '시작하기',
    terminalTitle: '터미널',
    terminalComment: '# 몇 초 만에 플러그인 설치',
  }
}

const t = labels[props.lang || 'en']
</script>

<template>
  <section :class="['hero-section', { visible: isVisible }]">
    <div class="hero-bg">
      <div class="dot-grid"></div>
    </div>

    <div class="hero-content">
      <div class="hero-left">
        <div class="hero-badge">
          <Sparkles :size="14" />
          <span>{{ t.stats }}</span>
        </div>

        <h1 class="hero-title">{{ t.title }}</h1>
        <p class="hero-tagline">{{ t.tagline }}</p>

        <div class="hero-actions">
          <a :href="lang === 'ko' ? '/ko/plugins/' : '/en/plugins/'" class="btn-terminal">
            <span class="btn-terminal-text">{{ t.browse }}</span>
            <span class="cursor-blink">_</span>
          </a>
          <a :href="lang === 'ko' ? '/ko/guide/getting-started' : '/en/guide/getting-started'" class="btn-secondary-hero">
            {{ t.getStarted }}
            <ChevronRight :size="16" />
          </a>
        </div>
      </div>

      <div class="hero-right">
        <div class="terminal-window">
          <div class="terminal-header">
            <div class="terminal-dots">
              <span class="dot red"></span>
              <span class="dot yellow"></span>
              <span class="dot green"></span>
            </div>
            <span class="terminal-title">{{ t.terminalTitle }}</span>
          </div>
          <div class="terminal-body">
            <div class="terminal-line comment">{{ t.terminalComment }}</div>
            <div class="terminal-line">
              <span class="prompt">$</span>
              <span class="command">/plugin marketplace add</span>
              <span class="arg">devstefancho/claude-plugins</span>
            </div>
            <div class="terminal-line success">
              <span class="prompt">&check;</span>
              <span>Marketplace registered</span>
            </div>
            <div class="terminal-line mt">
              <span class="prompt">$</span>
              <span class="command">/plugin install</span>
              <span class="arg">code-style-plugin</span>
              <span class="cursor-blink">_</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero-section {
  position: relative;
  padding: 5rem 2rem 4rem;
  max-width: 1200px;
  margin: 0 auto;
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.hero-section.visible {
  opacity: 1;
  transform: translateY(0);
}

.hero-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  z-index: 0;
  pointer-events: none;
}

.dot-grid {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, var(--vp-c-text-3) 0.5px, transparent 0.5px);
  background-size: 28px 28px;
  opacity: 0.15;
}

.hero-content {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 1rem;
  background: var(--cat-amber-soft, rgba(212, 165, 116, 0.1));
  border: 1px solid var(--cat-amber-border, rgba(212, 165, 116, 0.25));
  border-radius: 100px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: var(--vp-c-brand-1);
  margin-bottom: 1.5rem;
}

.hero-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 3.5rem;
  font-weight: 700;
  letter-spacing: -0.04em;
  line-height: 1.1;
  color: var(--vp-c-text-1);
  margin: 0 0 1rem 0;
}

.hero-tagline {
  font-size: 1.2rem;
  color: var(--vp-c-text-2);
  line-height: 1.6;
  margin: 0 0 2rem 0;
  max-width: 480px;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.btn-terminal {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.75rem 1.75rem;
  background: var(--vp-c-text-1);
  color: var(--vp-c-bg);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.95rem;
  font-weight: 500;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-terminal:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.btn-secondary-hero {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.75rem 1.5rem;
  color: var(--vp-c-text-1);
  font-size: 0.95rem;
  font-weight: 500;
  border: 1px solid var(--vp-c-border);
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-secondary-hero:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.cursor-blink {
  animation: blink 1s step-end infinite;
  color: var(--vp-c-brand-1);
  font-weight: 700;
}

/* Terminal Window */
.terminal-window {
  background: #1a1a2e;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2), 0 0 0 1px rgba(255, 255, 255, 0.05);
}

.dark .terminal-window {
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.08);
}

.terminal-header {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.terminal-dots {
  display: flex;
  gap: 6px;
  margin-right: 1rem;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.dot.red { background: #ff5f57; }
.dot.yellow { background: #febc2e; }
.dot.green { background: #28c840; }

.terminal-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
}

.terminal-body {
  padding: 1.25rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  line-height: 1.8;
}

.terminal-line {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.terminal-line.mt {
  margin-top: 0.5rem;
}

.terminal-line.comment {
  color: rgba(255, 255, 255, 0.3);
  font-style: italic;
}

.terminal-line.success {
  color: #4ade80;
  margin-bottom: 0.25rem;
}

.prompt {
  color: #d4a574;
  flex-shrink: 0;
}

.command {
  color: #e8e4df;
}

.arg {
  color: #818cf8;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-content {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-tagline {
    font-size: 1.05rem;
  }

  .hero-actions {
    flex-direction: column;
    align-items: flex-start;
  }

  .hero-right {
    order: -1;
  }
}
</style>
