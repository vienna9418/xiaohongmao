<template>
  <div class="publish-console">
    <section class="hero-card ai-hero">
      <div>
        <p class="eyebrow">Publish Console</p>
        <h1>自动发布控制台</h1>
        <p>管理发布任务、状态流转、失败原因和重试入口。后续接入 Playwright 执行器。</p>
      </div>
      <el-button type="primary" size="large" @click="drawerVisible = true">创建任务</el-button>
    </section>

    <section class="panel-card">
      <div class="panel-header">
        <div>
          <h2>发布任务队列</h2>
          <p>当前展示任务状态机基础能力。</p>
        </div>
        <el-button @click="loadTasks">刷新</el-button>
      </div>
      <el-table :data="tasks" class="data-table">
        <el-table-column prop="id" label="任务 ID" min-width="260" />
        <el-table-column prop="status" label="状态" width="130">
          <template #default="scope">
            <el-tag :type="statusTag(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="retry_count" label="重试" width="90" />
        <el-table-column prop="last_error" label="错误" min-width="180" />
        <el-table-column label="操作" width="260">
          <template #default="scope">
            <el-button size="small" @click="transition(scope.row.id, 'running')">运行</el-button>
            <el-button size="small" @click="transition(scope.row.id, 'failed')">失败</el-button>
            <el-button size="small" @click="transition(scope.row.id, 'cancelled')">取消</el-button>
          </template>
        </el-table-column>
      </el-table>
    </section>

    <el-drawer v-model="drawerVisible" title="创建发布任务" size="420px">
      <el-form label-position="top">
        <el-form-item label="账号 ID">
          <el-input v-model="form.account_id" placeholder="platform account uuid" />
        </el-form-item>
        <el-form-item label="内容 ID">
          <el-input v-model="form.content_id" placeholder="content uuid" />
        </el-form-item>
        <el-form-item label="最大重试次数">
          <el-input-number v-model="form.max_retries" :min="0" :max="10" />
        </el-form-item>
        <el-button type="primary" :loading="creating" @click="createTask">创建</el-button>
      </el-form>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { ElMessage } from "element-plus";

import { apiRequest } from "@/api/http";

interface PublishTask {
  id: string;
  account_id: string;
  content_id: string;
  status: string;
  retry_count: number;
  max_retries: number;
  last_error: string;
}

const tasks = ref<PublishTask[]>([]);
const drawerVisible = ref(false);
const creating = ref(false);
const form = reactive({ account_id: "", content_id: "", max_retries: 3 });

function statusTag(status: string) {
  if (status === "success") return "success";
  if (status === "failed") return "danger";
  if (status === "running" || status === "uploading" || status === "submitting") return "warning";
  return "info";
}

async function loadTasks() {
  try {
    tasks.value = await apiRequest<PublishTask[]>("/api/v1/publish-tasks");
  } catch {
    tasks.value = [];
  }
}

async function createTask() {
  creating.value = true;
  try {
    await apiRequest<PublishTask>("/api/v1/publish-tasks", {
      method: "POST",
      body: JSON.stringify(form),
    });
    ElMessage.success("发布任务已创建");
    drawerVisible.value = false;
    await loadTasks();
  } finally {
    creating.value = false;
  }
}

async function transition(id: string, to_status: string) {
  try {
    await apiRequest<PublishTask>(`/api/v1/publish-tasks/${id}/transition`, {
      method: "POST",
      body: JSON.stringify({ to_status, message: `manual transition to ${to_status}` }),
    });
    await loadTasks();
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : "状态变更失败");
  }
}

onMounted(loadTasks);
</script>
