<template>
  <nav class="w-screen h-12">
    <div
      class="w-screen h-full flex items-center justify-between px-8 bg-red-500"
    >
      <div class="flex space-x-2">
        <router-link v-if="user" to="/home" class="nav-link">
          <img class="nav-icon" src="../assets/home.svg" alt="" />
        </router-link>
        <button v-if="user" @click="toggleSearchModal" class="nav-link">
          <img class="nav-icon" src="../assets/search.svg" alt="" />
        </button>
      </div>

      <router-link to="/" class="">
        <img class="h-12" src="../assets/logo.svg" alt="" />
      </router-link>

      <div class="flex space-x-2">
        <button v-if="user" @click="toggleGroupchatModal" class="nav-link">
          <img class="nav-icon" src="../assets/chat.svg" alt="" />
        </button>
        <router-link v-if="user" to="/settings" class="nav-link">
          <img class="nav-icon" src="../assets/settings.svg" alt="" />
        </router-link>
      </div>
    </div>

    <SearchModal v-if="showSearchModal" @close="toggleSearchModal" />
    <GroupchatModal v-if="showGroupchatModal" @close="toggleGroupchatModal" />
  </nav>
</template>

<script>
import { ref, computed } from "vue";
import { useStore } from "vuex";
import SearchModal from "./SearchModal.vue";
import GroupchatModal from "./GroupchatModal.vue";
export default {
  components: {
    SearchModal,
    GroupchatModal,
  },
  setup() {
    const showSearchModal = ref(false);
    const showGroupchatModal = ref(false);

    const store = useStore();
    const user = computed(() => store.state.user);
    const isAdmin = user.value ? user.value.role == "admin" : false;

    const toggleSearchModal = function () {
      showSearchModal.value = !showSearchModal.value;
    };

    const toggleGroupchatModal = function () {
      showGroupchatModal.value = !showGroupchatModal.value;
    };

    return {
      isAdmin,
      user,
      showSearchModal,
      showGroupchatModal,
      toggleSearchModal,
      toggleGroupchatModal,
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