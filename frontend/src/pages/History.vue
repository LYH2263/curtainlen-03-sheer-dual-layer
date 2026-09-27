<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page">
  <h1>记录</h1>
  <table class="runs">
    <tr><th>时间</th><th>窗户</th><th>主帘</th><th>纱帘</th><th>备注</th></tr>
    <tr v-for="r in items" :key="r.id">
      <td class="nowrap">{{ r.created_at?.slice(0,16).replace('T',' ') }}</td>
      <td>{{ r.window_name }}</td>
      <td>{{ r.fabric_name }}：{{ r.result?.panels }}幅 × {{ r.result?.cut_height }}m = {{ r.result?.meters }}m</td>
      <td v-if="r.result?.sheer">{{ r.result.sheer.fabric_name }}：{{ r.result.sheer.panels }}幅 × {{ r.result.sheer.cut_height }}m = {{ r.result.sheer.meters }}m</td>
      <td v-else class="muted">未开</td>
      <td>{{ r.note }}</td>
    </tr>
  </table>
</div></template>
