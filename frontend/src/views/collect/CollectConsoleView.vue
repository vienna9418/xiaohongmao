<template>
  <div class="collect-console">
    <section class="hero-card ai-hero">
      <div>
        <p class="eyebrow">Collect Console</p>
        <h1>自动采集控制台</h1>
        <p>管理账号/内容采集任务、周期计划、状态流转和失败重试。</p>
      </div>
      <el-button type="primary" size="large" @click="drawerVisible = true">创建采集任务</el-button>
    </section>

    <section class="panel-card">
      <div class="panel-header">
        <div>
          <h2>采集任务队列</h2>
          <p>内容发布后可自动生成 1h、6h、24h、72h、7d 采集计划。</p>
        </div>
        <el-button @click="loadTasks">刷新</el-button>
      </div>
      <el-table :data="tasks" class="data-table">
        <el-table-column prop="id" label="任务 ID" min-width="260" />
        <el-table-column prop="collect_type" label="类型" width="100" />
        <el-table-column prop="status" label="状态" width="130">
          <template #default="scope">
            <el-tag :type="statusTag(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="scheduled_at" label="计划时间" min-width="180" />
        <el-table-column prop="retry_count" label="重试" width="90" />
        <el-table-column prop="last_error" label="错误" min-width="180" />
        <el-table-column label="操作" width="240">
          <template #default="scope">
            <el-button size="small" @click="transition(scope.row.id, 'running')">运行</el-button>
            <el-button size="small" @click="transition(scope.row.id, 'success')">成功</el-button>
            <el-button size="small" @click="transition(scope.row.id, 'failed')">失败</el-button>
          </template>
        </el-table-column>
      </el-table>
    </section>

    <el-drawer v-model="drawerVisible" title="创建采集任务" size="420px">
      <el-form label-position="top">
        <el-form-item label="采集类型">
          <el-select v-model="form.collect_type">
            <el-option label="账号采集" value="account" />
            <el-option label="内容采集" value="content" />
          </el-select>
        </el-form-item>
        <el-form-item label="账号 ID">
          <el-input v-model="form.account_id" placeholder="account uuid" />
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

interface CollectTask {
  id: string;
  account_id: string | null;
  content_id: string | null;
  collect_type: string;
  status: string;
  scheduled_at: string | null;
  retry_count: number;
  max_retries: number;
  last_error: string;
}

const tasks = ref<CollectTask[]>([]);
const drawerVisible = ref(false);
const creating = ref(false);
const form = reactive({ account_id: "", content_id: "", collect_type: "account", max_retries: 3 });

function statusTag(status: string) {
  if (status === "success") return "success";
  if (status === "failed") return "danger";
  if (status === "running") return "warning";
  return "info";
}

async function loadTasks() {
  try {
    tasks.value = await apiRequest<CollectTask[]>("/api/v1/collect-tasks");
  } catch {
    tasks.value = [];
  }
}

async function createTask() {
  creating.value = true;
  try {
    await apiRequest<CollectTask>("/api/v1/collect-tasks", {
      method: "POST",
      body: JSON.stringify({
        collect_type: form.collect_type,
        account_id: form.account_id || null,
        content_id: form.content_id || null,
        max_retries: form.max_retries,
      }),
    });
    ElMessage.success("采集任务已创建");
    drawerVisible.value = false;
    await loadTasks();
  } finally {
    creating.value = false;
  }
}

async function transition(id: string, to_status: string) {
  try {
    await apiRequest<CollectTask>(`/api/v1/collect-tasks/${id}/transition`, {
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
