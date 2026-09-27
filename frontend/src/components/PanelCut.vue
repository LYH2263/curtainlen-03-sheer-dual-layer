<script setup>
defineProps({
  panels: Number,
  cutHeight: Number,
  meters: Number,
  title: String,
  tone: { type: String, default: 'main' },
  fabricWidth: Number,
  finishedWidth: Number,
})
</script>
<template>
  <div class="layer">
    <h3 v-if="title">{{ title }}</h3>
    <div class="panel-cut">
      <div v-for="n in Math.min(panels||0,8)" :key="n" class="panel" :class="{ sheer: tone==='sheer' }" :style="{height: `${(cutHeight||1)*40}px`}"></div>
    </div>
    <p>{{ panels }} 幅 × {{ cutHeight }} m = {{ meters }} m</p>
    <table v-if="fabricWidth != null" class="detail">
      <tr><th>门幅</th><td>{{ fabricWidth }} m</td><th>成品宽</th><td>{{ finishedWidth }} m</td></tr>
      <tr><th>幅数</th><td>{{ panels }}</td><th>裁剪高</th><td>{{ cutHeight }} m</td></tr>
      <tr><th>米数</th><td>{{ meters }} m</td><td></td><td></td></tr>
    </table>
  </div>
</template>
