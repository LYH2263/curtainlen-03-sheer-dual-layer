<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const windows = ref([]); const fabrics = ref([])
const wid = ref(1); const fid = ref(1)
const sheerOn = ref(false); const sfid = ref(null); const sfull = ref(2.0)
const out = ref(null); const err = ref('')
onMounted(async () => {
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  fabrics.value = (await getJSON('/api/fabrics')).items.filter(x=>x.data_quality==='clean')
  if (windows.value.length) wid.value = windows.value[0].id
  if (fabrics.value.length) fid.value = fabrics.value[0].id
  const sheer = fabrics.value.find(x=>x.name.includes('纱'))
  sfid.value = sheer ? sheer.id : (fabrics.value[0]?.id ?? null)
  try { sfull.value = Number((await getJSON('/api/settings')).default_fullness) || 2.0 } catch { sfull.value = 2.0 }
})
async function go(save){
  err.value = ''
  const body = { window_id: wid.value, fabric_id: fid.value, save }
  if (sheerOn.value) Object.assign(body, { sheer_on: true, sheer_fabric_id: sfid.value, sheer_fullness: Number(sfull.value) })
  try { out.value = await postJSON('/api/estimate', body) } catch (e) { out.value = null; err.value = e.message }
}
</script>
<template><div class="page">
  <h1>算料</h1>
  <select v-model.number="wid"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select>
  <select v-model.number="fid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
  <label class="switch"><input type="checkbox" v-model="sheerOn"> 加纱帘</label>
  <span v-if="sheerOn" class="sheer-inputs">
    <select v-model.number="sfid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
    <label>纱帘褶倍 <input type="number" step="0.1" min="0.1" v-model.number="sfull"></label>
  </span>
  <button @click="go(false)">试算</button><button @click="go(true)">保存</button>
  <p v-if="err" class="bad">{{ err }}</p>
  <PanelCut v-if="out" title="主帘" tone="main" :panels="out.panels" :cut-height="out.cut_height" :meters="out.meters" :fabric-width="out.fabric_width" :finished-width="out.finished_width" />
  <PanelCut v-if="out && out.sheer" title="纱帘" tone="sheer" :panels="out.sheer.panels" :cut-height="out.sheer.cut_height" :meters="out.sheer.meters" :fabric-width="out.sheer.fabric_width" :finished-width="out.sheer.finished_width" />
  <p v-else-if="out" class="muted">纱帘未开 · 0m</p>
</div></template>
