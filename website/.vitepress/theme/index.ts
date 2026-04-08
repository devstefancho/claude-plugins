import DefaultTheme from 'vitepress/theme'
import PluginCard from './components/PluginCard.vue'
import PluginList from './components/PluginList.vue'
import HomeFeatures from './components/HomeFeatures.vue'
import HeroSection from './components/HeroSection.vue'
import StatsBar from './components/StatsBar.vue'
import InstallBanner from './components/InstallBanner.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('PluginCard', PluginCard)
    app.component('PluginList', PluginList)
    app.component('HomeFeatures', HomeFeatures)
    app.component('HeroSection', HeroSection)
    app.component('StatsBar', StatsBar)
    app.component('InstallBanner', InstallBanner)
  }
}
