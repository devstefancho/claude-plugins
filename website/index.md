---
layout: page
head:
  - - meta
    - http-equiv: refresh
      content: "0;url=/plugins/"
---

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vitepress'
const router = useRouter()
onMounted(() => { router.go('/plugins/') })
</script>
