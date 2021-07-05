<template>
  <div class="w-full center-me flex-col">
    <Navbar />
    <h1 class="text-3xl font-bold text-center mt-4">Log in to your account</h1>
    <h2 class="text-lg text-red-500 h-7" :class="{ invisible: !error }">
      {{ error }}
    </h2>
    <form class="mt-2 center-me flex-col space-y-4">
      <input
        class="input-field"
        type="text"
        placeholder="Username"
        v-model="username"
      />
      <input
        class="input-field"
        type="password"
        placeholder="Password"
        v-model="password"
      />
      <button
        type="submit"
        @click.prevent="login"
        :disabled="!buttonStateActive"
        class="button1 mt-4"
      >
        Login
      </button>
    </form>

    <span class="mt-4"
      >Don't have an account?
      <router-link class="text-blue-400 hover:underline" to="/register"
        >Register here</router-link
      ></span
    >
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import axios from "axios";
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  components: {
    Navbar,
  },
  setup() {
    const store = useStore();
    const router = useRouter();

    const username = ref("");
    const password = ref("");
    const error = ref("");

    const buttonStateActive = computed(() => username.value && password.value);

    const login = async function () {
      let response = (
        await axios.post("/api/v1/user/login", {
          username: username.value,
          password: password.value,
        })
      ).data;
      if (response.status === "error") {
        error.value = response.error;
      } else {
        store.dispatch("login", response.token);
        router.push("/home");
      }
    };

    return {
      username,
      password,
      error,
      buttonStateActive,
      login,
    };
  },
};
</script>