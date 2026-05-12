<template>
  <section class="panel-card">
    <div class="panel-header">
      <div>
        <p class="eyebrow">Account Matrix</p>
        <h1>账号矩阵</h1>
        <p>统一查看账号定位、负责人、健康分和登录状态。</p>
      </div>
      <el-button type="primary">新增账号</el-button>
    </div>

    <el-table :data="accounts" class="data-table">
      <el-table-column prop="display_name" label="账号" min-width="160" />
      <el-table-column prop="persona" label="定位" min-width="180" />
      <el-table-column prop="owner_name" label="负责人" width="120" />
      <el-table-column prop="health_score" label="健康分" width="100" />
      <el-table-column prop="login_status" label="登录状态" width="120" />
      <el-table-column prop="status" label="运营状态" width="120" />
    </el-table>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

import { apiRequest } from "@/api/http";

interface AccountRow {
  id: string;
  display_name: string;
  persona: string;
  owner_name: string;
  health_score: number;
  login_status: string;
  status: string;
}

const accounts = ref<AccountRow[]>([]);

onMounted(async () => {
  try {
    accounts.value = await apiRequest<AccountRow[]>("/api/v1/accounts");
  } catch {
    accounts.value = [];
  }
});
</script>
