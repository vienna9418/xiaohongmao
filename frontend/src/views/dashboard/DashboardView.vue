<template>
  <div class="dashboard-grid">
    <section class="hero-card">
      <div>
        <p class="eyebrow">今日运营</p>
        <h1>把内容生产、自动发布、自动采集放在一条动线上</h1>
        <p>小红贸 V1 将优先打通账号矩阵、AI 内容工厂、发布队列和数据回流。</p>
      </div>
      <el-button type="primary" size="large">创建发布任务</el-button>
    </section>

    <section v-for="metric in metrics" :key="metric.label" class="metric-card">
      <span>{{ metric.label }}</span>
      <strong>{{ metric.value }}</strong>
      <small>{{ metric.hint }}</small>
    </section>

    <section class="panel-card wide">
      <div class="panel-header">
        <div>
          <h2>任务动线</h2>
          <p>账号 -> AI -> 审核 -> 发布 -> 采集 -> 回流</p>
        </div>
      </div>
      <div class="flow-line">
        <div v-for="step in flow" :key="step" class="flow-step">{{ step }}</div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const metrics = [
  { label: "待发布", value: "12", hint: "今日排期" },
  { label: "采集中", value: "28", hint: "近 24 小时" },
  { label: "账号健康", value: "91%", hint: "矩阵均值" },
  { label: "AI 任务", value: "36", hint: "本周生成" },
];

const flow = ["账号矩阵", "AI 选题", "内容审核", "自动发布", "自动采集", "数据回流"];
</script>
