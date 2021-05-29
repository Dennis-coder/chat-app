<template>
  <div class="center-me flex-col pt-4">
    <div class="center-me flex-col">
      <button
        @click="togglePassword"
        class="focus:outline-none mb-2 text-xl center-me"
      >
        Change password
        <img
          src="../assets/arrow.svg"
          class="h-3 transition-all duration-300 transform ml-2"
          :class="{ 'rotate-90': showPassword }"
        />
      </button>
      <form
        class="transition-all duration-300 overflow-hidden h-0 flex items-center flex-col space-y-2"
        :class="{ 'h-36': showPassword }"
      >
        <input
          type="password"
          class="border border-black focus:outline-none px-1 w-48"
          placeholder="Current password"
          v-model="password.current"
        />
        <input
          type="password"
          class="border border-black focus:outline-none px-1 w-48"
          placeholder="New password"
          v-model="password.new"
        />
        <input
          type="password"
          class="border border-black focus:outline-none px-1 w-48"
          placeholder="Confirm new password"
          v-model="password.confirm"
        />
        <button @click.prevent="changePassword" class="button2">Change</button>
      </form>
    </div>

    <div class="center-me flex-col">
      <button
        @click="toggleReport"
        class="focus:outline-none mb-2 text-xl center-me"
      >
        Report a user
        <img
          src="../assets/arrow.svg"
          class="h-3 transition-all duration-300 transform ml-2"
          :class="{ 'rotate-90': showReport }"
        />
      </button>
      <form
        class="transition-all duration-300 overflow-hidden h-0 flex items-center flex-col space-y-2"
        :class="{ 'h-48': showReport }"
      >
        <input
          type="text"
          class="border border-black focus:outline-none px-1 w-48"
          placeholder="Their username"
          v-model="report.defendant"
        />
        <textarea
          type="text"
          class="border border-black focus:outline-none px-1 w-48"
          rows="4"
          placeholder="Reason"
          v-model="report.reason"
        />
        <button @click.prevent="sendReport" class="button2">Send</button>
      </form>
    </div>

    <button @click.prevent="logout" class="button2">Logout</button>
    <button @click.prevent="logout" class="button2">Delete account</button>
  </div>
</template>

<script>
import { ref } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  setup() {
    const store = useStore();
    const router = useRouter();

    const password = ref({
      current: "",
      new: "",
      confirm: "",
    });
    const report = ref({
      reason: "",
      defendant: null,
    });
    const showPassword = ref(false);
    const showReport = ref(false);

    const togglePassword = function () {
      showPassword.value = !showPassword.value;
    };

    const toggleReport = function () {
      showReport.value = !showReport.value;
    };

    const changePassword = function () {
      console.log(password.value);
    };

    const sendReport = function () {
      console.log(report.value);
    };

    const logout = function () {
      store.dispatch("removeUser");
      router.push("/");
    };

    return {
      password,
      report,
      showPassword,
      showReport,
      togglePassword,
      toggleReport,
      changePassword,
      sendReport,
      logout,
    };
  },
};
</script>

<style>
</style>