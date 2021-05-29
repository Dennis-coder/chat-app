<template>
  <div class="w-full center-me flex-col">
    <h1 class="text-3xl font-bold text-center mt-4">Create an account</h1>
    <h2 class="text-lg text-red-500 h-7" :class="{ invisible: !error }">
      {{ error }}
    </h2>
    <form class="mt-2 center-me flex-col space-y-4">
      <input
        class="border border-gray-500 p-1"
        type="text"
        placeholder="Username"
        v-model="username"
      />
      <input
        class="border border-gray-500 p-1"
        type="password"
        placeholder="Password"
        v-model="password"
      />
      <input
        class="border border-gray-500 p-1"
        type="password"
        placeholder="Confirm password"
        v-model="confirmPassword"
      />
      <button
        type="submit"
        @click.prevent="register"
        :disabled="!buttonStateActive"
        class="button1 mt-4"
        :class="{
          'opacity-50': !buttonStateActive,
          'cursor-pointer': buttonStateActive,
        }"
      >
        Register
      </button>
    </form>

    <span class="mt-4"
      >Already have an account?
      <router-link class="text-blue-500 hover:underline" to="/login"
        >Login here</router-link
      ></span
    >
  </div>
</template>

<script>
import axios from "axios";
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  setup() {
    const store = useStore();
    const router = useRouter();

    const username = ref("");
    const password = ref("");
    const confirmPassword = ref("");
    const error = ref("");

    const buttonStateActive = computed(
      () => this.username && this.password && this.confirmPassword
    );

    const register = async function () {
      if (password.value != confirmPassword.value) {
        error.value = "Passwords don't match";
        return;
      }
      let response = (
        await axios.post("/api/v1/user/register", {
          username: username.value,
          password: password.value,
        })
      ).data;
      if (response.status === "error") {
        error.value = response.error;
      } else {
        store.dispatch("setUser", response.user);
        router.push("/home");
      }
    };

    return {
      username,
      password,
      confirmPassword,
      error,
      buttonStateActive,
      register,
    };
  },
};
</script>