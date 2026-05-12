<template>
  <main class="login-page">
    <section class="login-hero">
      <div class="brand large">
        <div class="brand-mark">贸</div>
        <div>
          <div class="brand-title">小红贸</div>
          <div class="brand-subtitle">企业小红书矩阵自动化运营后台</div>
        </div>
      </div>
      <h1>用一条清晰动线管理账号、内容、发布和数据回流</h1>
      <p>现代化、简洁、高效，面向企业矩阵团队的生产稳定版后台。</p>
    </section>

    <section class="login-card">
      <h2>登录工作台</h2>
      <p>进入账号矩阵与内容工厂。</p>
      <el-form label-position="top" @submit.prevent="handleLogin">
        <el-form-item label="邮箱">
          <el-input v-model="form.email" placeholder="admin@example.com" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" placeholder="请输入密码" type="password" show-password />
        </el-form-item>
        <el-button type="primary" size="large" class="full-button" :loading="loading" @click="handleLogin">
          登录
        </el-button>
      </el-form>
    </section>
  </main>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import { useRoute, useRouter } from "vue-router";

import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();
const loading = ref(false);
const form = reactive({ email: "", password: "" });

async function handleLogin() {
  loading.value = true;
  try {
    await auth.login(form.email, form.password);
    await router.push(String(route.query.redirect ?? "/"));
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : "登录失败");
  } finally {
    loading.value = false;
  }
}
</script>
