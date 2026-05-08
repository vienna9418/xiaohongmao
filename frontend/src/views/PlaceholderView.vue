<template>
  <section class="panel-card">
    <p class="eyebrow">{{ title }}</p>
    <h1>{{ title }}建设中</h1>
    <p>该模块将在后续 Phase 中接入真实数据与操作流程。</p>
  </section>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const title = computed(() => String(route.meta.title ?? "模块"));
</script>
