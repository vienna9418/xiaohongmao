<template>
  <div class="api-center">
    <section class="hero-card ai-hero">
      <div>
        <p class="eyebrow">Open API</p>
        <h1>开放 API 中心</h1>
        <p>管理 API Key、签名认证和外部系统集成入口。</p>
      </div>
      <el-button type="primary" size="large" @click="drawerVisible = true">创建 API Key</el-button>
    </section>

    <section class="panel-card">
      <div class="panel-header">
        <div>
          <h2>API Key</h2>
          <p>Secret 仅创建时显示，请立即保存。</p>
        </div>
        <el-button @click="loadKeys">刷新</el-button>
      </div>
      <el-table :data="apiKeys" class="data-table">
        <el-table-column prop="name" label="名称" min-width="160" />
        <el-table-column prop="key_id" label="Key ID" min-width="220" />
        <el-table-column label="Scopes" min-width="260">
          <template #default="scope">
            <el-tag v-for="item in scope.row.scopes" :key="item" class="tag-item">{{ item }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="启用" width="90" />
        <el-table-column prop="last_used_at" label="最后使用" min-width="180" />
      </el-table>
    </section>

    <section class="panel-card">
      <h2>签名规则</h2>
      <p>外部系统请求 `/api/public/v1/*` 时需要传入签名 Header。</p>
      <pre class="code-box">X-XHM-Key: &lt;key_id&gt;
X-XHM-Secret: &lt;secret&gt;
X-XHM-Timestamp: &lt;unix seconds&gt;
X-XHM-Signature: HMAC_SHA256(secret, METHOD + "\n" + PATH + "\n" + TIMESTAMP + "\n" + BODY)</pre>
    </section>

    <el-drawer v-model="drawerVisible" title="创建 API Key" size="420px">
      <el-form label-position="top">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="ERP 集成" />
        </el-form-item>
        <el-form-item label="Scopes">
          <el-select v-model="form.scopes" multiple>
            <el-option label="contents:write" value="contents:write" />
            <el-option label="ai:run" value="ai:run" />
            <el-option label="publish:write" value="publish:write" />
            <el-option label="collect:write" value="collect:write" />
            <el-option label="metrics:read" value="metrics:read" />
          </el-select>
        </el-form-item>
        <el-button type="primary" :loading="creating" @click="createKey">创建</el-button>
      </el-form>

      <el-alert v-if="createdSecret" type="success" show-icon :closable="false" class="secret-alert">
        <template #title>API Secret 已生成，请立即保存</template>
        <pre>{{ createdSecret }}</pre>
      </el-alert>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { ElMessage } from "element-plus";

import { apiRequest } from "@/api/http";

interface APIKeyRow {
  id: string;
  name: string;
  key_id: string;
  scopes: string[];
  is_active: boolean;
  last_used_at: string | null;
  expires_at: string | null;
}

interface APIKeyCreated extends APIKeyRow {
  secret: string;
}

const apiKeys = ref<APIKeyRow[]>([]);
const drawerVisible = ref(false);
const creating = ref(false);
const createdSecret = ref("");
const form = reactive({
  name: "外部系统集成",
  scopes: ["contents:write", "ai:run", "publish:write", "collect:write", "metrics:read"],
});

async function loadKeys() {
  try {
    apiKeys.value = await apiRequest<APIKeyRow[]>("/api/v1/api-keys");
  } catch {
    apiKeys.value = [];
  }
}

async function createKey() {
  creating.value = true;
  try {
    const result = await apiRequest<APIKeyCreated>("/api/v1/api-keys", {
      method: "POST",
      body: JSON.stringify(form),
    });
    createdSecret.value = `key_id=${result.key_id}\nsecret=${result.secret}`;
    ElMessage.success("API Key 已创建");
    await loadKeys();
  } finally {
    creating.value = false;
  }
}

onMounted(loadKeys);
</script>
