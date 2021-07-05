<template>
  <div class="center-me flex-col h-full">
    <NavbarLite :text="'Settings'" :settings="false" @back="back" />
    <div class="center-me flex-col mt-4">
      <button @click="togglePassword" class="form-button">
        Change password
        <img
          src="../assets/arrow.svg"
          class="h-3 transition-all duration-300 transform ml-2"
          :class="{ 'rotate-90': showPassword }"
        />
      </button>
      <form class="form h-0" :class="{ 'h-32': showPassword }">
        <input
          type="password"
          class="input-field w-48"
          placeholder="New password"
          v-model="password.new"
        />
        <input
          type="password"
          class="input-field w-48"
          placeholder="Confirm new password"
          v-model="password.confirm"
        />
        <button @click.prevent="changePassword" class="button2">Change</button>
      </form>
    </div>

    <div class="center-me flex-col">
      <button @click="toggleReport" class="form-button">
        Report a user
        <img
          src="../assets/arrow.svg"
          class="h-3 transition-all duration-300 transform ml-2"
          :class="{ 'rotate-90': showReport }"
        />
      </button>
      <form class="form h-0" :class="{ 'h-52': showReport }">
        <input
          type="text"
          class="input-field w-48"
          placeholder="Their username"
          v-model="report.defendant"
        />
        <textarea
          type="text"
          class="input-field w-48"
          rows="4"
          placeholder="Reason"
          v-model="report.reason"
        />
        <button @click.prevent="sendReport" class="button2">Send</button>
      </form>
    </div>

    <div class="mt-auto mb-4 space-x-2">
      <button @click.prevent="logout" class="button2">Logout</button>
      <button @click.prevent="deleteAccount" class="button2">
        Delete account
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import NavbarLite from "../components/NavbarLite.vue";
import { ref } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  components: {
    NavbarLite,
  },
  setup() {
    const store = useStore();
    const router = useRouter();

    const password = ref({
      new: "",
      confirm: "",
    });
    const report = ref({
      reason: "",
      defendant: "",
    });
    const showPassword = ref(false);
    const showReport = ref(false);

    const togglePassword = function () {
      showPassword.value = !showPassword.value;
    };

    const toggleReport = function () {
      showReport.value = !showReport.value;
    };

    const changePassword = async function () {
      if (password.value.new === password.value.confirm) {
        await axios.put("/api/v1/user/password", {
          password: password.value.new,
        });
        password.value.new = "";
        password.value.confirm = "";
      }
    };

    const sendReport = async function () {
      let response = (await axios.post("/api/v1/report", report.value)).data;
      if (typeof response === "string") {
        alert("No user with that username exists!");
      } else {
        report.value.reason = "";
        report.value.defendant = "";
      }
    };

    const logout = function () {
      store.dispatch("logout");
      router.push("/");
    };

    const deleteAccount = async function () {
      if (confirm("Are you sure you want to delete your account?")) {
        await axios.delete("/api/v1/user");
        logout();
      }
    };

    const back = async function () {
      router.push("/home");
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
      deleteAccount,
      back,
    };
  },
};
</script>

<style>
.form {
  @apply transition-all duration-300 overflow-hidden flex items-center flex-col space-y-2;
}
.form-button {
  @apply focus:outline-none mb-2 text-xl flex items-center justify-center;
}
.form-button img {
  filter: invert(100%) sepia(70%) saturate(546%) hue-rotate(178deg)
    brightness(101%) contrast(84%);
}
</style>