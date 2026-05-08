import { createRouter, createWebHistory } from "vue-router";

import AdminLayout from "@/layouts/AdminLayout.vue";
import DashboardView from "@/views/dashboard/DashboardView.vue";
import PlaceholderView from "@/views/PlaceholderView.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: AdminLayout,
      children: [
        { path: "", name: "dashboard", component: DashboardView },
        { path: "accounts", name: "accounts", component: PlaceholderView, meta: { title: "账号矩阵" } },
        { path: "contents", name: "contents", component: PlaceholderView, meta: { title: "内容工厂" } },
        { path: "ai", name: "ai", component: PlaceholderView, meta: { title: "AI 中心" } },
        { path: "publish", name: "publish", component: PlaceholderView, meta: { title: "自动发布" } },
        { path: "collect", name: "collect", component: PlaceholderView, meta: { title: "自动采集" } },
        { path: "risk", name: "risk", component: PlaceholderView, meta: { title: "风控审计" } },
        { path: "settings", name: "settings", component: PlaceholderView, meta: { title: "系统设置" } },
      ],
    },
  ],
});
