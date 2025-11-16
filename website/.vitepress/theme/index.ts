import DefaultTheme from 'vitepress/theme'
import PluginCard from './components/PluginCard.vue'
import PluginList from './components/PluginList.vue'
import HomeFeatures from './components/HomeFeatures.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('PluginCard', PluginCard)
    app.component('PluginList', PluginList)
    app.component('HomeFeatures', HomeFeatures)
  }
}
