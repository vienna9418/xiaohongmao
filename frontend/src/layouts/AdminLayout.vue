<template>
  <el-container class="admin-shell">
    <el-aside class="admin-sidebar" width="232px">
      <div class="brand">
        <div class="brand-mark">贸</div>
        <div>
          <div class="brand-title">小红贸</div>
          <div class="brand-subtitle">矩阵运营后台</div>
        </div>
      </div>
      <el-menu router :default-active="$route.path" class="side-menu">
        <el-menu-item index="/">工作台</el-menu-item>
        <el-menu-item index="/accounts">账号矩阵</el-menu-item>
        <el-menu-item index="/contents">内容工厂</el-menu-item>
        <el-menu-item index="/ai">AI 中心</el-menu-item>
        <el-menu-item index="/publish">自动发布</el-menu-item>
        <el-menu-item index="/collect">自动采集</el-menu-item>
        <el-menu-item index="/api-center">开放 API</el-menu-item>
        <el-menu-item index="/risk">风控审计</el-menu-item>
        <el-menu-item index="/settings">系统设置</el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="admin-header">
        <div>
          <div class="page-title">{{ pageTitle }}</div>
          <div class="page-subtitle">现代化、简洁、高效的企业矩阵运营工作台</div>
        </div>
        <div class="header-actions">
          <el-input placeholder="搜索账号 / 内容 / 任务" class="global-search" />
          <el-button type="primary">新建内容</el-button>
          <el-button @click="logout">退出</el-button>
        </div>
      </el-header>
      <el-main class="admin-main">
        <RouterView />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useAuthStore } from "@/stores/auth";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const pageTitle = computed(() => String(route.meta.title ?? "工作台"));

async function logout() {
  auth.logout();
  await router.push({ name: "login" });
}
</script>
