<template>
  <section class="panel-card">
    <div class="panel-header">
      <div>
        <p class="eyebrow">Content Factory</p>
        <h1>内容工厂</h1>
        <p>围绕草稿、AI 生成、审核、排期、发布、采集形成流水线。</p>
      </div>
      <el-button type="primary">新建内容</el-button>
    </div>

    <el-table :data="contents" class="data-table">
      <el-table-column prop="title" label="标题" min-width="220" />
      <el-table-column prop="status" label="状态" width="120" />
      <el-table-column prop="source" label="来源" width="120" />
      <el-table-column label="标签" min-width="180">
        <template #default="scope">
          <el-tag v-for="tag in scope.row.tags" :key="tag" class="tag-item">{{ tag }}</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

import { apiRequest } from "@/api/http";

interface ContentRow {
  id: string;
  title: string;
  status: string;
  source: string;
  tags: string[];
}

const contents = ref<ContentRow[]>([]);

onMounted(async () => {
  try {
    contents.value = await apiRequest<ContentRow[]>("/api/v1/contents");
  } catch {
    contents.value = [];
  }
});
</script>
