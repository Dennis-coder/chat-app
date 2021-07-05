<template>
  <nav class="w-screen h-12">
    <div
      class="w-screen h-full flex items-center px-4 bg-red-500"
      :class="{ 'justify-between': !!user, 'justify-center': !user }"
    >
      <router-link to="/" class="">
        <img class="h-12" src="../assets/logo.svg" alt="" />
      </router-link>

      <div v-if="loggedIn" class="flex space-x-2">
        <button @click="toggleSearchModal" class="nav-link relative">
          <img class="nav-icon" src="../assets/search.svg" alt="" />
          <div
            v-if="pendingRequests"
            class="
              absolute
              -top-0
              -right-0
              bg-gray-200
              w-3
              h-3
              rounded-full
              center-me
            "
          ></div>
        </button>
        <button @click="toggleGroupchatModal" class="nav-link">
          <img class="nav-icon" src="../assets/chat.svg" alt="" />
        </button>
        <button @click="toggleSettings" class="nav-link">
          <img class="nav-icon" src="../assets/settings.svg" alt="" />
        </button>
        <button
          v-if="user.role == 'admin'"
          @click="toggleAdmin"
          class="nav-link"
        >
          <img class="nav-icon" src="../assets/admin.svg" alt="" />
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
export default {
  setup(_, { emit }) {
    const store = useStore();
    const user = computed(() => store.state.user);
    const loggedIn = computed(() =>
      user.value ? user.value.exp * 1000 > Date.now() : false
    );
    const isAdmin = user.value != null ? user.value.role == "admin" : false;
    const pendingRequests = computed(
      () => store.state.requestsModule.requests.length > 0
    );

    const toggleSearchModal = function () {
      emit("toggleSearchModal");
    };

    const toggleGroupchatModal = function () {
      emit("toggleGroupchatModal");
    };

    const toggleSettings = function () {
      emit("toggleSettings");
    };

    const toggleAdmin = function () {
      emit("toggleAdmin");
    };

    return {
      isAdmin,
      user,
      toggleSearchModal,
      toggleGroupchatModal,
      toggleSettings,
      toggleAdmin,
      loggedIn,
      pendingRequests,
    };
  },
};
</script>
<style>
.nav-link {
  @apply w-9 h-9 flex items-center justify-center bg-black rounded-full bg-opacity-10 focus:outline-none;
}

.nav-icon {
  filter: brightness(0) saturate(100%);
  @apply w-5 h-5;
}
</style>