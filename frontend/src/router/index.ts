import { createRouter, createWebHistory } from "vue-router";

import { useAuthStore } from "@/stores/auth";
import AdminLayout from "@/layouts/AdminLayout.vue";
import LoginView from "@/views/auth/LoginView.vue";
import AccountsView from "@/views/accounts/AccountsView.vue";
import ApiCenterView from "@/views/api-center/ApiCenterView.vue";
import AiCenterView from "@/views/ai/AiCenterView.vue";
import CollectConsoleView from "@/views/collect/CollectConsoleView.vue";
import ContentsView from "@/views/contents/ContentsView.vue";
import DashboardView from "@/views/dashboard/DashboardView.vue";
import PlaceholderView from "@/views/PlaceholderView.vue";
import PublishConsoleView from "@/views/publish/PublishConsoleView.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/login", name: "login", component: LoginView, meta: { public: true } },
    {
      path: "/",
      component: AdminLayout,
      children: [
        { path: "", name: "dashboard", component: DashboardView },
        { path: "accounts", name: "accounts", component: AccountsView, meta: { title: "账号矩阵" } },
        { path: "contents", name: "contents", component: ContentsView, meta: { title: "内容工厂" } },
        { path: "ai", name: "ai", component: AiCenterView, meta: { title: "AI 中心" } },
        { path: "publish", name: "publish", component: PublishConsoleView, meta: { title: "自动发布" } },
        { path: "collect", name: "collect", component: CollectConsoleView, meta: { title: "自动采集" } },
        { path: "api-center", name: "api-center", component: ApiCenterView, meta: { title: "开放 API" } },
        { path: "risk", name: "risk", component: PlaceholderView, meta: { title: "风控审计" } },
        { path: "settings", name: "settings", component: PlaceholderView, meta: { title: "系统设置" } },
      ],
    },
  ],
});

router.beforeEach((to) => {
  const auth = useAuthStore();
  if (!to.meta.public && !auth.isAuthenticated) {
    return { name: "login", query: { redirect: to.fullPath } };
  }
  if (to.name === "login" && auth.isAuthenticated) {
    return { name: "dashboard" };
  }
  return true;
});
