import { defineStore } from "pinia";

import { apiRequest } from "@/api/http";

interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("xhm_access_token") ?? "",
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
  },
  actions: {
    async login(email: string, password: string) {
      const response = await apiRequest<LoginResponse>("/api/v1/auth/login", {
        method: "POST",
        auth: false,
        body: JSON.stringify({ email, password }),
      });
      this.token = response.access_token;
      localStorage.setItem("xhm_access_token", response.access_token);
    },
    logout() {
      this.token = "";
      localStorage.removeItem("xhm_access_token");
    },
  },
});
