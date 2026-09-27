<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const props = defineProps({ id: String })
const w = ref(null); const runs = ref([])
onMounted(async () => {
  w.value = await getJSON(`/api/windows/${props.id}`)
  runs.value = (await getJSON(`/api/runs?window_id=${props.id}&limit=10`)).items
})
</script>
<template><div class="page" v-if="w">
  <h1>{{ w.name }}</h1>
  <p v-if="w.data_quality==='dirty'" class="bad">{{ w.note }}</p>
  <p>宽 {{ w.width }} 高 {{ w.height }} 褶倍 {{ w.fullness }}</p>
  <h2>算料记录</h2>
  <p v-if="!runs.length" class="muted">暂无算料记录</p>
  <div v-for="r in runs" :key="r.id" class="run-card">
    <p class="nowrap">{{ r.created_at?.slice(0,16).replace('T',' ') }} <span v-if="r.note">｜{{ r.note }}</span></p>
    <p>主帘（{{ r.fabric_name }}）：门幅 {{ r.result?.fabric_width }}m ｜ 成品宽 {{ r.result?.finished_width }}m ｜ {{ r.result?.panels }}幅 × {{ r.result?.cut_height }}m = {{ r.result?.meters }}m</p>
    <p v-if="r.result?.sheer">纱帘（{{ r.result.sheer.fabric_name }}，褶倍 {{ r.result.sheer.fullness }}）：门幅 {{ r.result.sheer.fabric_width }}m ｜ 成品宽 {{ r.result.sheer.finished_width }}m ｜ {{ r.result.sheer.panels }}幅 × {{ r.result.sheer.cut_height }}m = {{ r.result.sheer.meters }}m</p>
    <p v-else class="muted">纱帘未开 · 0m</p>
  </div>
</div></template>
