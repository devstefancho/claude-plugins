<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { Package, Layers, Brain, Terminal, Webhook, Plug } from 'lucide-vue-next'
import pluginData from '../../../data/plugins.json'

const props = defineProps<{
  lang?: 'ko' | 'en'
}>()

const plugins = pluginData.plugins

const stats = computed(() => {
  const totalSkills = plugins.reduce((sum, p) => sum + p.components.skills.length, 0)
  const totalCommands = plugins.reduce((sum, p) => sum + p.components.commands.length, 0)
  const totalHooks = plugins.filter(p => p.components.hooks).length
  const totalMcp = plugins.reduce((sum, p) => sum + p.components.mcpServers.length, 0)

  return [
    { icon: Package, value: plugins.length, label: 'Plugins', labelKo: '플러그인' },
    { icon: Layers, value: pluginData.categories.length, label: 'Categories', labelKo: '카테고리' },
    { icon: Brain, value: totalSkills, label: 'Skills', labelKo: '스킬' },
    { icon: Terminal, value: totalCommands, label: 'Commands', labelKo: '커맨드' },
    { icon: Webhook, value: totalHooks, label: 'Hooks', labelKo: '훅' },
    { icon: Plug, value: totalMcp, label: 'MCP Servers', labelKo: 'MCP 서버' },
  ]
})

const isVisible = ref(false)
onMounted(() => {
  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        isVisible.value = true
        observer.disconnect()
      }
    },
    { threshold: 0.3 }
  )
  const el = document.querySelector('.stats-bar')
  if (el) observer.observe(el)
})
</script>

<template>
  <div :class="['stats-bar', { visible: isVisible }]">
    <div class="stats-container">
      <div v-for="(stat, i) in stats" :key="stat.label" class="stat-item" :style="{ animationDelay: `${i * 80}ms` }">
        <component :is="stat.icon" :size="16" class="stat-icon" />
        <span class="stat-value">{{ stat.value }}</span>
        <span class="stat-label">{{ lang === 'ko' ? stat.labelKo : stat.label }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-bar {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem 3rem;
}

.stats-container {
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding: 1.25rem 2rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-border-soft);
  border-radius: 12px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.stats-bar.visible .stat-item {
  opacity: 1;
  transform: translateY(0);
  transition-delay: var(--delay, 0ms);
}

.stats-bar.visible .stat-item:nth-child(1) { transition-delay: 0ms; }
.stats-bar.visible .stat-item:nth-child(2) { transition-delay: 80ms; }
.stats-bar.visible .stat-item:nth-child(3) { transition-delay: 160ms; }
.stats-bar.visible .stat-item:nth-child(4) { transition-delay: 240ms; }
.stats-bar.visible .stat-item:nth-child(5) { transition-delay: 320ms; }
.stats-bar.visible .stat-item:nth-child(6) { transition-delay: 400ms; }

.stat-icon {
  color: var(--vp-c-brand-1);
  flex-shrink: 0;
}

.stat-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
}

.stat-label {
  font-size: 0.8rem;
  color: var(--vp-c-text-3);
  letter-spacing: 0.02em;
}

@media (max-width: 768px) {
  .stats-container {
    gap: 1rem;
    padding: 1rem;
  }

  .stat-item {
    gap: 0.375rem;
  }

  .stat-value {
    font-size: 0.95rem;
  }

  .stat-label {
    font-size: 0.7rem;
  }
}
</style>
