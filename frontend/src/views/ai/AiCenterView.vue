<template>
  <div class="ai-center">
    <section class="hero-card ai-hero">
      <div>
        <p class="eyebrow">AI Center</p>
        <h1>AI 中心：选题、Prompt、Skill 和内容生成</h1>
        <p>先把 Prompt/Skill 的管理动线跑通，后续接入真实模型供应商和内容工厂。</p>
      </div>
      <el-button type="primary" size="large">新建 Skill</el-button>
    </section>

    <section class="ai-grid">
      <div class="panel-card">
        <div class="panel-header compact">
          <div>
            <h2>Prompt 设置</h2>
            <p>配置可复用的变量化 Prompt 模板。</p>
          </div>
        </div>
        <el-form label-position="top" class="stack-form">
          <el-form-item label="模板名称">
            <el-input v-model="promptForm.name" placeholder="小红书种草文案" />
          </el-form-item>
          <el-form-item label="模板编码">
            <el-input v-model="promptForm.code" placeholder="rednote_seed_copy" />
          </el-form-item>
          <el-form-item label="用户 Prompt">
            <el-input
              v-model="promptForm.user_prompt"
              type="textarea"
              :rows="5"
              placeholder="请基于 {account_persona} 为 {target_audience} 生成内容"
            />
          </el-form-item>
          <el-button type="primary" :loading="promptLoading" @click="createPrompt">保存 Prompt</el-button>
        </el-form>
      </div>

      <div class="panel-card">
        <div class="panel-header compact">
          <div>
            <h2>Skill 库</h2>
            <p>把 Prompt 包装成可执行的 AI 工作流。</p>
          </div>
        </div>
        <el-form label-position="top" class="stack-form">
          <el-form-item label="Skill 名称">
            <el-input v-model="skillForm.name" placeholder="多账号差异化改写" />
          </el-form-item>
          <el-form-item label="Skill 编码">
            <el-input v-model="skillForm.code" placeholder="multi_account_rewrite" />
          </el-form-item>
          <el-form-item label="绑定 Prompt">
            <el-select v-model="skillForm.prompt_template_id" clearable placeholder="选择 Prompt 模板">
              <el-option v-for="prompt in prompts" :key="prompt.id" :label="prompt.name" :value="prompt.id" />
            </el-select>
          </el-form-item>
          <el-button type="primary" :loading="skillLoading" @click="createSkill">保存 Skill</el-button>
        </el-form>
      </div>
    </section>

    <section class="panel-card">
      <div class="panel-header">
        <div>
          <h2>Skill 执行测试</h2>
          <p>使用变量输入 dry-run，验证 Prompt 渲染和 AI Adapter 输出。</p>
        </div>
      </div>
      <div class="run-grid">
        <el-form label-position="top">
          <el-form-item label="选择 Skill">
            <el-select v-model="selectedSkillId" placeholder="选择 Skill">
              <el-option v-for="skill in skills" :key="skill.id" :label="skill.name" :value="skill.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="输入变量 JSON">
            <el-input v-model="runInput" type="textarea" :rows="8" />
          </el-form-item>
          <el-button type="primary" :loading="runLoading" @click="runSkill">运行 dry-run</el-button>
        </el-form>
        <div class="result-box">
          <pre>{{ runResult || "暂无结果" }}</pre>
        </div>
      </div>
    </section>

    <section class="ai-grid">
      <div class="panel-card">
        <h2>Prompt 模板</h2>
        <el-table :data="prompts" class="data-table">
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="code" label="编码" />
          <el-table-column prop="category" label="分类" width="120" />
        </el-table>
      </div>
      <div class="panel-card">
        <h2>Skill 列表</h2>
        <el-table :data="skills" class="data-table">
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="code" label="编码" />
          <el-table-column prop="category" label="分类" width="120" />
        </el-table>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { ElMessage } from "element-plus";

import { apiRequest } from "@/api/http";

interface PromptTemplate {
  id: string;
  name: string;
  code: string;
  category: string;
  variables: string[];
}

interface Skill {
  id: string;
  name: string;
  code: string;
  category: string;
  prompt_template_id: string | null;
}

const prompts = ref<PromptTemplate[]>([]);
const skills = ref<Skill[]>([]);
const promptLoading = ref(false);
const skillLoading = ref(false);
const runLoading = ref(false);
const selectedSkillId = ref("");
const runResult = ref("");
const runInput = ref(JSON.stringify({
  account_persona: "精致生活方式账号",
  target_audience: "25-35 岁职场女性",
  product_name: "春季通勤包",
}, null, 2));

const promptForm = reactive({
  name: "小红书种草文案",
  code: "rednote_seed_copy",
  description: "生成适合小红书的种草文案",
  category: "copywriting",
  variables: ["account_persona", "target_audience", "product_name"],
  system_prompt: "你是企业小红书矩阵运营专家，输出简洁、真实、有转化力。",
  user_prompt: "请基于账号定位 {account_persona}，为 {target_audience} 推广 {product_name}，生成标题、正文和标签。",
  output_schema: {},
  temperature: 70,
});

const skillForm = reactive({
  name: "种草文案生成",
  code: "seed_copy_generation",
  description: "基于 Prompt 生成小红书种草文案",
  category: "copywriting",
  prompt_template_id: "",
  input_schema: {},
  output_schema: {},
});

async function loadData() {
  prompts.value = await apiRequest<PromptTemplate[]>("/api/v1/ai/prompts");
  skills.value = await apiRequest<Skill[]>("/api/v1/ai/skills");
}

async function createPrompt() {
  promptLoading.value = true;
  try {
    await apiRequest<PromptTemplate>("/api/v1/ai/prompts", {
      method: "POST",
      body: JSON.stringify(promptForm),
    });
    ElMessage.success("Prompt 已保存");
    await loadData();
  } finally {
    promptLoading.value = false;
  }
}

async function createSkill() {
  skillLoading.value = true;
  try {
    await apiRequest<Skill>("/api/v1/ai/skills", {
      method: "POST",
      body: JSON.stringify({
        ...skillForm,
        prompt_template_id: skillForm.prompt_template_id || null,
      }),
    });
    ElMessage.success("Skill 已保存");
    await loadData();
  } finally {
    skillLoading.value = false;
  }
}

async function runSkill() {
  if (!selectedSkillId.value) {
    ElMessage.warning("请先选择 Skill");
    return;
  }
  runLoading.value = true;
  try {
    const inputs = JSON.parse(runInput.value) as Record<string, unknown>;
    const result = await apiRequest<unknown>(`/api/v1/ai/skills/${selectedSkillId.value}/run`, {
      method: "POST",
      body: JSON.stringify({ inputs, dry_run: true }),
    });
    runResult.value = JSON.stringify(result, null, 2);
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : "运行失败");
  } finally {
    runLoading.value = false;
  }
}

onMounted(async () => {
  try {
    await loadData();
  } catch {
    prompts.value = [];
    skills.value = [];
  }
});
</script>
