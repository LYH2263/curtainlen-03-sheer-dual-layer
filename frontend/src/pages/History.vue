<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page"><h1>记录</h1><ul><li v-for="r in items" :key="r.id">{{ r.window_name }} 主 {{ r.result?.meters }}m<template v-if="r.result?.sheer?.enabled"> / 纱 {{ r.result.sheer.meters }}m（{{ r.result.sheer.fabric_name }}）</template></li></ul></div></template>
