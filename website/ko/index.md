---
layout: page
head:
  - - meta
    - http-equiv: refresh
      content: "0;url=/ko/plugins/"
---

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vitepress'
const router = useRouter()
onMounted(() => { router.go('/ko/plugins/') })
</script>
